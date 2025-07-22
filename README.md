# RelevAI Python SDK

**Python SDK for accessing RelevAI's AI Lang services with secure token management.**

This library provides an easy-to-use interface for interacting with RelevAI's APIs, including automatic token renewal via `ClientKey` and `ServiceKey`, and flexible serialization strategies.

---

## Features

- Secure authentication with RelevAI services using OAuth2 tokens
- Automatic token renewal in the background
- Synchronous and asynchronous clients
- Built-in support for RelevAI AI-Lang features like `chat` and `embed`
- Pluggable serialization system (`JSON`, `LZ4`, `MsgPack`)

---

## Installation

```bash
pip install rundock
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
print(response)
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
    print(response)

asyncio.run(main())
```

---

## Serialization

Built-in serializers:

* `JSONSerializer`
* `LZ4Serializer` (requires `joblib`)
* `MsgPackSerializer` (requires `msgpack`)

All serializers support both `dumps()` (base64 string) and `dump()` (raw bytes):

```python
from relevai.serializers import JSONSerializer

serializer = JSONSerializer()
data = {"key": "value"}

s = await serializer.dumps(data)
obj = await serializer.loads(s)
```

---

## Testing

You can mock token behavior or run integration tests by injecting a fake token or using `ServiceKey` for automation:

```python
from relevai.key import ServiceKey

key = ServiceKey(
    client_id="your_client_id",
    client_secret="your_client_secret",
    auth_url="https://auth.relev.ai/token"
)
```

---

## License

© 2025 RelevAI S.L. — Licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)

---

## Links

* [Documentation](https://github.com/relev-ai/rundock-server)
* [RelevAI](https://relev.ai)
