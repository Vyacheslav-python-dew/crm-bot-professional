from fastapi import APIRouter

router = APIRouter()

@router.get("/clients")
async def get_clients():
    return {"clients": []}