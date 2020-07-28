from fastapi import FastAPI, Depends
from app.config import DEBUG
from app.routers import access, folders, images


app = FastAPI(
    debug=DEBUG,
    title='WebStorage',
    version='0.0.1',
    description='WebStorage description',
)


app.include_router(
    router=access.router,
    prefix='/access',
    tags=['access'],
    dependencies=[Depends(access.get_api_key)],
)

app.include_router(
    router=folders.router,
    prefix='/folders',
    tags=['folders'],
    dependencies=[Depends(access.get_api_key)],
)

app.include_router(
    router=images.router,
    prefix='/images',
    tags=['images'],
    dependencies=[Depends(access.get_api_key)],
)
