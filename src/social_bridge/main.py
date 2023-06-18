from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from social_bridge.routers import users, ngo, posts
from social_bridge.dependencies import get_settings


settings = get_settings()


app = FastAPI(
    title="SocialBridge",
    description="The best city community connector",
    version="0.0.1",
    contact={"name": "Roland Sobczak", "email": "rolandsobczak@icloud.com"},
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(ngo.router)
app.include_router(posts.router)
app.mount(settings.MEDIA_BASE_URL, StaticFiles(directory=settings.MEDIA_FOLDER), name="media")