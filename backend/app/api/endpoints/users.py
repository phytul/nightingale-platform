from fastapi import APIRouter
from app.schemas.user_schema import User

router = APIRouter()


@router.get("/get-users", response_model=list[User])
async def get_users():
    return [{"id": 1, "sex": "male", "username": "admin", "email": "admin@example.com"}]
