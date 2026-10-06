import subprocess

from fastapi import FastAPI

app = FastAPI()


@app.get("/ping/{ip}")
def ping_device(ip: str):

    result = subprocess.run(
        ["ping", "-n", "1", ip],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        status = "reachable"
    else:
        status = "unreachable"

    return {
        "ip": ip,
        "status": status
    }