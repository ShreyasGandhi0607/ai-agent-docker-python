from fastapi import APIRouter

router = APIRouter()

# /api/chat
@router.get("/")
def heath_check():
    return {
        "Status" : "OK"
    }