"""
Quantization, KV cache, and inference optimization.

Level: Advanced.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Quantize a weight array and estimate cache memory
# Separate numerical error, payload bytes, and runtime claims.
# Step 1: Choose a symmetric scale from maximum absolute weight.
# Step 2: Round and clip to int8.
# Step 3: Dequantize and bound reconstruction error.
# Step 4: Compute a transparent KV memory estimate with explicit units.
if __name__ == "__main__":
    import numpy as np

    weights = np.random.default_rng(42).normal(0, 0.2, (32, 32)).astype(np.float32)
    scale = float(np.abs(weights).max()) / 127
    quantized = np.clip(np.rint(weights / scale), -127, 127).astype(np.int8)
    restored = quantized.astype(np.float32) * scale
    error = float(np.max(np.abs(weights - restored)))
    assert error <= scale / 2 + 1e-7
    assert quantized.nbytes == weights.nbytes // 4
    layers, batch, tokens, kv_heads, head_dim, bytes_per_value = 12, 1, 2048, 4, 64, 2
    cache_bytes = 2 * layers * batch * tokens * kv_heads * head_dim * bytes_per_value
    assert cache_bytes > 0
    print("float/int8 payload bytes:", weights.nbytes, quantized.nbytes, "(scale metadata additional)")
    print("maximum weight error:", round(error, 6))
    print("example KV estimate MiB:", round(cache_bytes / 1024**2, 2))
