from typing import Optional, List
from starlette import status
from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from models import User
from schemas.user_schema import UserSchema, UserPostSchema, UpdateUserSchema
from services.user_service import UserService
from core.current_user_depends import get_current_user


async def is_superuser(current_user: User = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403,
                            detail="Operation not permitted")


user_router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(is_superuser)])


@user_router.post("", response_model=UserPostSchema)
async def create_user(
        user: UserSchema,
        user_service: UserService = Depends()
):
    return await user_service.create(user)


@user_router.get("", response_model=List[UserPostSchema])
async def get_all_users(
        page_size: Optional[int] = 10,
        start_index: Optional[int] = 0,
        user_service: UserService = Depends()
):

    return await user_service.list(page_size, start_index)


@user_router.get("/{user_id}", response_model=UserPostSchema)
async def get_user(
        user_id: int,
        user_service: UserService = Depends()
):
    return await user_service.get(user_id)


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        user_service: UserService = Depends()
):
    await user_service.delete(user_id)


@user_router.patch("/{user_id}", response_model=UserPostSchema)
async def update_user(
        user_id: int,
        user_body: UpdateUserSchema,
        user_service: UserService = Depends()
):
    return await user_service.update(user_id, user_body)
