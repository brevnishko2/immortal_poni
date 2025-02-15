from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.users import Users
from app.schemas.users import UserCreate, UserUpdate, UserResponse, UserList
from app.core.security import get_password_hash
from app.api.routes.auth import get_current_user
from typing import Dict
router = APIRouter()


@router.get("", response_model=UserList)
async def get_users(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> UserList:
    """
        Получение списка пользователей с пагинацией.

        Args:
            skip: Количество пропускаемых записей
            limit: Максимальное количество возвращаемых записей
            db: Сессия базы данных

        Returns:
            UserList: Список пользователей и общее количество
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Forbidden")
    result = await db.execute(select(Users).offset(skip).limit(limit))
    users = result.scalars().all()
    total_result = await db.execute(select(func.count()).select_from(Users))
    total = total_result.scalar()
    return {"total": total, "items": users}


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> UserResponse:
    """
        Получение данных конкретного пользователя.

        Args:
            user_id: UUID пользователя
            db: Сессия базы данных
            current_user: Текущий авторизованный пользователь

        Returns:
            UserResponse: Данные пользователя

        Raises:
            HTTPException: Если пользователь не найден
    """

    user = await db.execute(select(Users).where(Users.id == user_id))
    user = user.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> UserResponse:
    """
    Создание нового пользователя.

    Args:
        user: Данные для создания пользователя
        db: Сессия базы данных
        current_user: Текущий авторизованный пользователь

    Returns:
        UserResponse: Данные созданного пользователя

    Raises:
        HTTPException: Если email или username уже заняты, или если у текущего пользователя нет прав
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    result = await db.execute(select(Users).where(Users.email == user.email))
    db_user = result.scalars().first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    result = await db.execute(select(Users).where(Users.username == user.username))
    db_user = result.scalars().first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    hashed_password = get_password_hash(user.password)
    db_user = Users(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> UserResponse:
    """
    Обновление данных пользователя.

    Args:
        user_id: UUID пользователя
        user: Данные для обновления
        db: Сессия базы данных
        current_user: Текущий авторизованный пользователь

    Returns:
        UserResponse: Обновленные данные пользователя

    Raises:
        HTTPException: Если пользователь не найден
    """
    result = await db.execute(select(Users).where(Users.id == user_id))
    db_user = result.scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    update_data: Dict = user.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    for field, value in update_data.items():
        setattr(db_user, field, value)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user
