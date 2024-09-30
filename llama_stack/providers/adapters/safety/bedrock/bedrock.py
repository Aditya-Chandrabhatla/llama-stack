# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.


import traceback
from typing import Any, Dict, List

from .config import BedrockSafetyConfig
from llama_stack.apis.safety import *  # noqa
from llama_models.llama3.api.datatypes import *  # noqa: F403
import json
import logging

import boto3


logger = logging.getLogger(__name__)


class BedrockSafetyAdapter(Safety):
    def __init__(self, config: BedrockSafetyConfig) -> None:
        self.config = config

    async def initialize(self) -> None:
        if not self.config.aws_profile:
            raise RuntimeError(
                f"Missing boto_client aws_profile in model info::{self.config}"
            )

        try:
            print(f"initializing with profile --- > {self.config}::")
            self.boto_client_profile = self.config.aws_profile
            self.boto_client = boto3.Session(
                profile_name=self.boto_client_profile
            ).client("bedrock-runtime")
        except Exception as e:
            raise RuntimeError(f"Error initializing BedrockSafetyAdapter: {e}") from e

    async def shutdown(self) -> None:
        pass

    async def run_shield(
        self, shield_type: str, messages: List[Message], params: Dict[str, Any] = None
    ) -> RunShieldResponse:
        """This is the implementation for the bedrock guardrails. The input to the guardrails is to be of this format
        ```content = [
            {
                "text": {
                    "text": "Is the AB503 Product a better investment than the S&P 500?"
                }
            }
        ]```
        However the incoming messages are of this type UserMessage(content=....) coming from
        https://github.com/meta-llama/llama-models/blob/main/models/llama3/api/datatypes.py

        They contain content, role . For now we will extract the content and default the "qualifiers": ["query"]
        """
        try:
            logger.debug(f"run_shield::{params}::messages={messages}")
            if "guardrailIdentifier" not in params:
                raise RuntimeError(
                    "Error running request for BedrockGaurdrails:Missing GuardrailID in request"
                )

            if "guardrailVersion" not in params:
                raise RuntimeError(
                    "Error running request for BedrockGaurdrails:Missing guardrailVersion in request"
                )

            # - convert the messages into format Bedrock expects
            content_messages = []
            for message in messages:
                content_messages.append({"text": {"text": message.content}})
            logger.debug(
                f"run_shield::final:messages::{json.dumps(content_messages, indent=2)}:"
            )

            response = self.boto_client.apply_guardrail(
                guardrailIdentifier=params.get("guardrailIdentifier"),
                guardrailVersion=params.get("guardrailVersion"),
                source="OUTPUT",  # or 'INPUT' depending on your use case
                content=content_messages,
            )
            logger.debug(f"run_shield:: response: {response}::")
            if response["action"] == "GUARDRAIL_INTERVENED":
                user_message = ""
                metadata = {}
                for output in response["outputs"]:
                    # guardrails returns a list - however for this implementation we will leverage the last values
                    user_message = output["text"]
                for assessment in response["assessments"]:
                    # guardrails returns a list - however for this implementation we will leverage the last values
                    metadata = dict(assessment)
                return SafetyViolation(
                    user_message=user_message,
                    violation_level=ViolationLevel.ERROR,
                    metadata=metadata,
                )

        except Exception:
            error_str = traceback.format_exc()
            logger.error(
                f"Error in apply_guardrails:{error_str}:: RETURNING None !!!!!"
            )

        return None