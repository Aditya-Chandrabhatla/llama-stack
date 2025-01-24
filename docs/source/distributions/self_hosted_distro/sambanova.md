---
orphan: true
---
# SambaNova Distribution

```{toctree}
:maxdepth: 2
:hidden:

self
```

The `llamastack/distribution-sambanova` distribution consists of the following provider configurations.

| API | Provider(s) |
|-----|-------------|
| agents | `inline::meta-reference` |
| inference | `remote::sambanova` |
| safety | `inline::llama-guard` |
| telemetry | `inline::meta-reference` |
| tool_runtime | `remote::brave-search`, `remote::tavily-search`, `inline::code-interpreter`, `inline::rag-runtime` |
| vector_io | `inline::faiss`, `remote::chromadb`, `remote::pgvector` |


### Environment Variables

The following environment variables can be configured:

- `LLAMASTACK_PORT`: Port for the Llama Stack distribution server (default: `5001`)
- `SAMBANOVA_API_KEY`: SambaNova.AI API Key (default: ``)

### Models

The following models are available by default:

- `meta-llama/Llama-3.1-8B-Instruct (Meta-Llama-3.1-8B-Instruct)`
- `meta-llama/Llama-3.1-70B-Instruct (Meta-Llama-3.1-70B-Instruct)`
- `meta-llama/Llama-3.1-405B-Instruct-FP8 (Meta-Llama-3.1-405B-Instruct)`
- `meta-llama/Llama-3.2-1B-Instruct (Meta-Llama-3.2-1B-Instruct)`
- `meta-llama/Llama-3.2-3B-Instruct (Meta-Llama-3.2-3B-Instruct)`
- `meta-llama/Llama-3.2-11B-Vision-Instruct (Llama-3.2-11B-Vision-Instruct)`
- `meta-llama/Llama-3.2-90B-Vision-Instruct (Llama-3.2-90B-Vision-Instruct)`


### Prerequisite: API Keys

Make sure you have access to a SambaNova API Key. You can get one by visiting [SambaBova.ai](https://sambanova.ai/).


## Running Llama Stack with SambaNova

You can do this via Conda (build code) or Docker which has a pre-built image.

### Via Docker

This method allows you to get started quickly without having to build the distribution code.

```bash
LLAMA_STACK_PORT=5001
docker run \
  -it \
  -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  llamastack/distribution-sambanova \
  --port $LLAMA_STACK_PORT \
  --env SAMBANOVA_API_KEY=$SAMBANOVA_API_KEY
```

### Via Conda

```bash
llama stack build --template sambanova --image-type conda
llama stack run ./run.yaml \
  --port $LLAMA_STACK_PORT \
  --env SAMBANOVA_API_KEY=$SAMBANOVA_API_KEY
```