"""
Tokens, subword tokenization, and context windows.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: One BPE merge and a checked context budget
# Make token units and overflow explicit.
# Step 1: Count adjacent symbol pairs.
# Step 2: Merge the most frequent pair in a deterministic order.
# Step 3: Verify the merged symbols still reconstruct the text.
# Step 4: Reject an over-budget request rather than silently truncating.
if __name__ == "__main__":
    from collections import Counter

    corpus = [list("lower"), list("lowest"), list("lower")]
    counts = Counter(pair for symbols in corpus for pair in zip(symbols, symbols[1:]))
    chosen = sorted(counts, key=lambda pair: (-counts[pair], pair))[0]
    def merge(symbols, pair):
        output, index = [], 0
        while index < len(symbols):
            if index + 1 < len(symbols) and tuple(symbols[index:index+2]) == pair:
                output.append("".join(pair))
                index += 2
            else:
                output.append(symbols[index])
                index += 1
        return output
    merged = [merge(symbols, chosen) for symbols in corpus]
    assert ["".join(symbols) for symbols in merged] == ["lower", "lowest", "lower"]
    def check_budget(input_tokens, reserved_output, limit):
        if min(input_tokens, reserved_output) < 0 or input_tokens + reserved_output > limit:
            raise ValueError("request exceeds toy context budget")
        return limit - input_tokens - reserved_output
    assert check_budget(6, 3, 10) == 1
    try:
        check_budget(9, 3, 10)
    except ValueError:
        print("overflow rejected")
    else:
        raise AssertionError("overflow accepted")
    print("learned toy merge:", chosen, "tokens:", merged[0])
