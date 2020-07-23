from fastapi import FastAPI, Depends
from app.routers import apikey, browse, image


app = FastAPI()


app.include_router(
    router=apikey.router,
    prefix='/apikey',
    tags=['apikey'],
    dependencies=[Depends(apikey.get_api_key)],
)

app.include_router(
    router=browse.router,
    prefix='/browse',
    tags=['browse'],
    dependencies=[Depends(apikey.get_api_key)],
)

app.include_router(
    router=image.router,
    prefix='/image',
    tags=['image'],
    dependencies=[Depends(apikey.get_api_key)],
)