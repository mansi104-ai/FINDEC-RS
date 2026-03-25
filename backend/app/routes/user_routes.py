from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserSchema

router = APIRouter()

@router.get("/{user_id}")
async def get_user(user_id: int):
    """Get user by ID"""
    return {"id": user_id, "username": "user", "email": "user@example.com"}

@router.post("/")
async def create_user(user: UserSchema):
    """Create a new user"""
    return {"status": "created", "user": user}

@router.put("/{user_id}")
async def update_user(user_id: int, user: UserSchema):
    """Update user"""
    return {"status": "updated", "user": user}

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """Delete user"""
    return {"status": "deleted", "id": user_id}
