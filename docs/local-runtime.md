# Local use

Use Python 3.11 and install this package in a separate virtual environment as
shown in the root README. This setup covers CPU utilities, configuration parsing,
plain tensor checkpoints, basic CLI use and local chat transports. Blender 90M,
GPU/FP16 training, distributed execution, MTurk and Messenger/Heroku deployment
are outside this setup.

## Input formats

Checkpoints must contain dictionaries, tensors and primitive values. Loading uses
`weights_only=True` on the CPU. Custom Opt/APEX/agent-class checkpoints are not
accepted. Obtain a plain state dict from the trusted model producer. Use only
trusted files of reasonable size; tensor loading can exhaust memory.

Options must be JSON objects. Chat configuration uses YAML mappings. Module and
model paths in configuration select application code, so use trusted configuration.

NLTK sentence tokenization uses `punkt_tab`. Install the tables explicitly into
a trusted data directory before using `--dict-tokenizer nltk`:

```bash
python -m nltk.downloader punkt_tab
```

## Local transports

Python browser and websocket transports bind to `127.0.0.1`. Browser clients
accept `--host localhost` or `--host 127.0.0.1`. They do not provide authentication,
TLS or multi-user isolation. Do not port-forward them or expose them through a
public reverse proxy.

```bash
python -m parlai.chat_service.services.websocket.run --help
python -m parlai.chat_service.services.browser_chat_test.client --help
```

The separate Node transport requires Node 24.x, version 24.5 or later. It accepts
local non-browser websocket clients and does not serve Messenger webhooks. It
is not needed by the Python browser client.

```bash
cd parlai/chat_service/core/server
npm ci --ignore-scripts
npm start
```
