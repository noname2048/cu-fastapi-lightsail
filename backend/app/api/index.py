from fastapi import APIRouter

router = APIRouter()


@router.get("/v1/hello")
async def hello():
    return {"message": "hello"}
