"""
HTTP, REST APIs, and async programming.

Level: Beginner to intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Async JSON requests entirely in memory
# Exercise the HTTP boundary without credentials or network access.
# Step 1: Implement a deterministic request handler.
# Step 2: Send through MockTransport with an explicit timeout.
# Step 3: Check status before reading JSON.
# Step 4: Gather two results and validate order and prediction values.
if __name__ == "__main__":
    import asyncio
    import json
    import httpx

    def handler(request):
        assert request.method == "POST" and request.url.path == "/predict"
        record = json.loads(request.content)
        return httpx.Response(200, json={"label": int(record["latency_ms"] >= 20)})

    async def main():
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transport, timeout=2.0) as client:
            async def predict(value):
                response = await client.post("https://model.test/predict", json={"latency_ms": value})
                response.raise_for_status()
                return response.json()["label"]
            labels = await asyncio.gather(predict(5), predict(25))
        assert labels == [0, 1]
        print("mock HTTP labels:", labels)

    asyncio.run(main())
