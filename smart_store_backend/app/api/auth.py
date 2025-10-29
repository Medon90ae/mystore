
from fastapi import APIRouter

from ..deps import CurrentUser

router = APIRouter()

@router.get("/me")
async def read_users_me(current_user: CurrentUser):
    """
    Endpoint to verify a token and return the user's decoded claims.
    Useful for the frontend to check authentication status and roles.
    """
    return current_user
