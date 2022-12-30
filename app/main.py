from fastapi import FastAPI

from .routes import router


app = FastAPI()
app.include_router(router, prefix="/api")


# @app.get("/latest_devices")
# async def latest_devices():
#     pass


# @app.get("/in_stores_now")
# async def in_stores_now():
#     pass


# @app.get("/top")
# async def top():
#     pass


# @app.get("/search")
# async def search():
#     pass
