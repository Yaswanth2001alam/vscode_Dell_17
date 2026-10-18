"""
Structured output, JSON, and safe tool calling.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Validate and execute one allowlisted local tool
# Make the application, not generated text, control execution.
# Step 1: Declare a strict schema with extra fields forbidden.
# Step 2: Validate a mock tool request.
# Step 3: Dispatch through a dictionary of known callables.
# Step 4: Reject a malformed port count and verify the valid result.
if __name__ == "__main__":
    from typing import Literal
    from pydantic import BaseModel, ConfigDict, Field, ValidationError

    class CapacityArguments(BaseModel):
        model_config = ConfigDict(extra="forbid", strict=True)
        total: int = Field(ge=0, le=10000)
        used: int = Field(ge=0, le=10000)

    class ToolCall(BaseModel):
        model_config = ConfigDict(extra="forbid", strict=True)
        name: Literal["free_ports"]
        arguments: CapacityArguments

    def free_ports(total, used):
        if used > total:
            raise ValueError("used exceeds total")
        return {"free": total - used}

    registry = {"free_ports": free_ports}
    call = ToolCall.model_validate_json('{"name":"free_ports","arguments":{"total":48,"used":12}}')
    result = registry[call.name](**call.arguments.model_dump())
    assert result == {"free": 36}
    try:
        ToolCall.model_validate_json('{"name":"free_ports","arguments":{"total":"48","used":12}}')
    except ValidationError:
        print("wrong argument type rejected")
    else:
        raise AssertionError("wrong type accepted")
    print(result)

# %% Worked example: Reject unknown tool names and cross-field inconsistency
# Show that syntax and schema checks do not replace semantic tool invariants.
# Step 1: Restrict tool names with Literal and forbid extra fields.
# Step 2: Reject an unsupported operation.
# Step 3: Check a cross-field total/used relationship explicitly.
# Step 4: Verify no action occurs for rejected requests.
if __name__ == "__main__":
    from typing import Literal
    from pydantic import BaseModel, ConfigDict, ValidationError, model_validator

    class Request(BaseModel):
        model_config = ConfigDict(extra="forbid", strict=True)
        tool: Literal["free_ports"]
        total: int
        used: int

        @model_validator(mode="after")
        def valid_capacity(self):
            if not 0 <= self.used <= self.total <= 10000:
                raise ValueError("inconsistent capacity")
            return self

    bad_inputs = [{"tool": "run_command", "total": 48, "used": 12},
                  {"tool": "free_ports", "total": 10, "used": 12}]
    rejected = 0
    for payload in bad_inputs:
        try:
            Request.model_validate(payload)
        except ValidationError:
            rejected += 1
        else:
            raise AssertionError("invalid request accepted")
    assert rejected == 2
    print("requests rejected before execution:", rejected)
