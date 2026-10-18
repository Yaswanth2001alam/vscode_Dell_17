"""
Pydantic, FastAPI, and a tested inference endpoint.

Level: Intermediate to advanced.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Test both a valid request and rejected input
# Exercise a real local API contract without opening a port.
# Step 1: Define strict bounded request and response models.
# Step 2: Create a POST prediction route.
# Step 3: Call it with TestClient.
# Step 4: Assert the valid response and a 422 for an invalid feature.
if __name__ == "__main__":
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from pydantic import BaseModel, ConfigDict, Field

    class Features(BaseModel):
        model_config = ConfigDict(extra="forbid", strict=True)
        latency_ms: float = Field(ge=0, le=10000, allow_inf_nan=False)

    class Prediction(BaseModel):
        label: int
        model_version: str

    app = FastAPI()

    @app.post("/predict", response_model=Prediction)
    def predict(features: Features):
        return Prediction(label=int(features.latency_ms >= 20), model_version="teaching-rule-v1")

    with TestClient(app) as client:
        good = client.post("/predict", json={"latency_ms": 25.0})
        bad = client.post("/predict", json={"latency_ms": -1.0})
        assert good.status_code == 200
        assert good.json() == {"label": 1, "model_version": "teaching-rule-v1"}
        assert bad.status_code == 422
    print("valid:", good.json(), "invalid status:", bad.status_code)
