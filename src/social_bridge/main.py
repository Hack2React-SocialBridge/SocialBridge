from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from social_bridge.routers import users, ngo
from social_bridge.dependencies import get_settings


settings = get_settings()


app = FastAPI(
    title="social_bridge",
    description="Let's clean up your neighbourhood together",
    version="0.0.1",
    contact={"name": "Roland Sobczak", "email": "rolandsobczak@icloud.com"},
)
app.include_router(users.router)
app.include_router(ngo.router)
app.mount(settings.MEDIA_BASE_URL, StaticFiles(directory=settings.MEDIA_FOLDER), name="media")