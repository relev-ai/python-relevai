# RelevAI Python SDK

**Helper SDK to simplify access and integration with RelevAI's AI services.**

This library offers a lightweight, developer-friendly interface for authenticating and interacting with RelevAI’s API endpoints.  
It includes automatic token management (`ClientKey` / `ServiceKey`), sync/async client support, and flexible serialization strategies.

While not required to use RelevAI’s APIs, this SDK is designed to reduce boilerplate and speed up development.

---

## Features

- Secure authentication with RelevAI services using OAuth2 tokens
- Automatic token renewal in the background
- Synchronous and asynchronous clients
- Built-in support for RelevAI AI-Lang services (`chat`, `embed`)
- Pluggable serialization system (`JSON`, `LZ4`, `MsgPack`)

---

## Installation

```bash
pip install relevai
````

> Requires Python **3.9+**

---

## Authentication

You can authenticate with RelevAI using either a `ClientKey` (API key) or `ServiceKey` (client credentials).

### Example using `ClientKey`:

```python
from relevai.key import ClientKey
from relevai.ai import AILangClient

key = ClientKey(
    api_key="your_refresh_token",
    client_id="your_client_id",
    auth_url="https://auth.relev.ai/token"
)

client = AILangClient(key)
response = client.chat(model="llm-model", messages=[{"role": "user", "content": "Hello!"}])
```

---

## Async Client

For asynchronous use:

```python
import asyncio
from relevai.key import ClientKey
from relevai.ai import AILangAsyncClient

async def main():
    key = ClientKey(
        api_key="your_refresh_token",
        client_id="your_client_id",
        auth_url="https://auth.relev.ai/token"
    )

    client = AILangAsyncClient(key)
    response = await client.chat(model="relevai/ai-lang", messages=[{"role": "user", "content": "Hi!"}])

asyncio.run(main())
```

---

## Serialization

This SDK includes a simple serialization interface with multiple backends:

* JSONSerializer (default)
* LZ4Serializer (requires joblib)
* MsgPackSerializer (requires msgpack)

Each serializer supports:

* dumps() / loads() — base64 string encoding
* dump() / load() — raw bytes

### Example: 

```python
from relevai.serializers import JSONSerializer

serializer = JSONSerializer()
data = {"key": "value"}

encoded = await serializer.dumps(data)
decoded = await serializer.loads(encoded)
```

---

## License

© 2025 RelevAI S.L. — Licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)

---

## Links

* [RelevAI official webpage](https://relev.ai)
