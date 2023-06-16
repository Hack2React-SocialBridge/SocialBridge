from fastapi import FastAPI


app = FastAPI(
    title="SocialBridge",
    description="",
    version="0.0.1",
    contact={"name": "Roland Sobczak", "email": "rolandsobczak@icloud.com"},
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
