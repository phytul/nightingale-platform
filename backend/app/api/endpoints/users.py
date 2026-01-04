from fastapi import APIRouter
from app.schemas.user import Gender, UserSchema

router = APIRouter()


@router.get("/get-users", response_model=list[UserSchema])
async def get_users():
    return [
        {
            "id": 1,
            "sex": Gender.FEMALE,
            "username": "admin",
            "email": "admin@example.com",
        }
    ]
