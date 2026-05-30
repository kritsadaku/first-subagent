from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to Agent Studio"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
