from fastapi import FastAPI
import socket
import time

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Network TCP Testing API"
    }


@app.get("/tcp-ping/{host}/{port}")
def tcp_ping(host: str, port: int):

    start_time = time.time()

    try:
        connection = socket.create_connection(
            (host, port),
            timeout=3
        )

        connection.close()

        end_time = time.time()

        response_time = round(
            (end_time - start_time) * 1000,
            2
        )

        return {
            "host": host,
            "port": port,
            "status": "reachable",
            "response_time_ms": response_time
        }

    except socket.timeout:

        return {
            "host": host,
            "port": port,
            "status": "timeout"
        }

    except ConnectionRefusedError:

        return {
            "host": host,
            "port": port,
            "status": "connection refused"
        }

    except Exception as error:

        return {
            "host": host,
            "port": port,
            "status": "failed",
            "error": str(error)
        }