from typing import Optional
from uuid import uuid4
from app.security.jwttype import JWTType
from app.security.hasher import hash_password, verify_password
from app.utils.result import Result, err, success
from ..abstract.abc_repository import AbstractRepository
from app.database.models.models import Profile, User
from sqlalchemy import CursorResult, delete, select, update, insert

class UserRepository(AbstractRepository):
    model = User

    async def create(self, **kwargs):
        query = insert(self.model).values(**kwargs).returning(self.model)
        result = await self._session.execute(query)
        return result.scalars().first()

    async def user_exists(self, email: str, username: str) -> dict:
        query_email = select(User).where(User.email == email)
        query_username = select(User).where(User.username == username)

        result_email = await self._session.execute(query_email)
        result_username = await self._session.execute(query_username)

        return {
            "email_exists": result_email.scalar() is not None,
            "username_exists": result_username.scalar() is not None
        }

    async def update_by_id(self, userId: str, **kwargs):
        query = update(self.model).where(self.model.userId == userId).values(**kwargs).returning(self.model)
        result = await self._session.execute(query)
        await self._session.commit()
        return result.scalars().first()

    async def authenticate_user(self, email: str, password: str) -> Result:
        user = await UserRepository(self._session).get_by_filter_one(email=email)
        if not user or not verify_password(password, user.password):
            return err("Неверные данные для входа или пароль")
        # if not user:
        #     return err("Пользователь не найден")
        # if not verify_password(password, user.password):
        #     return err("Некорректный пароль")
        return success(user)

    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self._session.execute(select(self.model).where(self.model.username == username))
        user = result.scalars().first()
        if not user:
            return None

        return user
    
    async def get_by_id(self, iduser: str) -> Optional[User]:
        result = await self._session.execute(select(self.model).where(self.model.userId == iduser))
        user = result.scalars().first()
        if not user:
            return None

        return user

    async def get_by_email(self, email) -> Optional[User]:
        result = await self._session.execute(select(self.model).where(self.model.email == email))
        user = result.scalars().first()
        if not user:
            return None

        return user

    async def delete_user_and_profile(self, userId: str) -> Result[None]:
        try:
            # Удаляем профиль
            profile_delete_query = delete(Profile).where(Profile.iduser == userId)
            await self._session.execute(profile_delete_query)

            # Удаляем пользователя
            user_delete_query = delete(User).where(User.userId == userId)
            await self._session.execute(user_delete_query)

            # Коммитим транзакцию
            await self._session.commit()

            return success(None)
        except Exception as e:
            await self._session.rollback()
            return err(f"Ошибка при удалении пользователя и профиля: {str(e)}")
        
    async def update_username(self, userId: uuid4, new_username: str) -> Result[None]:
        query = (
            update(self.model)
            .where(self.model.userId == userId)
            .values(username=new_username)
            .returning(self.model)
        )
        result = await self._session.execute(query)
        await self._session.commit()
        return success(result.scalars().first())

    async def update_email(self, userId: uuid4, new_email: str) -> Result[None]:
        query = (
            update(self.model)
            .where(self.model.userId == userId)
            .values(email=new_email)
            .returning(self.model)
        )
        result = await self._session.execute(query)
        await self._session.commit()
        return success(result.scalars().first())

    async def update_password(self, userId: uuid4, new_password: str) -> Result[None]:
        hashed_password = hash_password(new_password)
        query = (
            update(self.model)
            .where(self.model.userId == userId)
            .values(password=hashed_password)
            .returning(self.model)
        )
        result = await self._session.execute(query)
        await self._session.commit()
        return success(result.scalars().first())