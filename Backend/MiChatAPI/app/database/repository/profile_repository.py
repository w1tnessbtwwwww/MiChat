from sqlalchemy.ext.asyncio import AsyncSession

from app.security.hasher import verify_password
from app.utils.result import *
from ..abstract.abc_repository import AbstractRepository
from app.database.models.models import Profile
from datetime import date
from sqlalchemy import CursorResult, delete, select, update, insert
from typing import Optional
from uuid import uuid4

class ProfileRepository(AbstractRepository):
    model = Profile

    async def create_profile(self, user_id: uuid4, name: str):
        query = insert(self.model).values(iduser=user_id, name=name).returning(self.model)
        result = await self._session.execute(query)
        return result.scalars().first()
    
    async def update(self, userId: str, **kwargs):
        query = update(self.model).where(self.model.userId == userId).values(**kwargs).returning(self.model)
        result = await self._session.execute(query)
        await self._session.commit()
        return result.scalars().first()

    async def update_profile(self, 
                             userId: str,
                             name: Optional[str],
                             about_me: Optional[str],
                             birthday: Optional[date],
                             image: Optional[bytes],
                             ) -> Result[None]:        
        query = (
            select(self.model)
            .where(self.model.userId == userId)
        )

        result = await self._session.execute(query)
        profile = result.scalars().one_or_none()
        if not profile:
            creating = await self.create(userId=userId, name=name, about_me=about_me, birthday=birthday, image=image)
            return success(creating) if creating else err("Some error while attemping resource.")
        return success(await self.update(uuserId=userId, name=name, about_me=about_me, birthday=birthday, image=image))