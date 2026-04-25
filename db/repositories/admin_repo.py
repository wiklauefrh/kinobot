from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from db import models
from db.constants import AdminRole
from typing import Optional, List


class AdminRepository:
    """Repository for Admin operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, role: str = AdminRole.ADMIN.value) -> models.Admin:
        """Create a new admin."""
        admin = models.Admin(user_id=user_id, role=role)
        self.session.add(admin)
        await self.session.flush()
        return admin

    async def get_by_user_id(self, user_id: int) -> Optional[models.Admin]:
        """Get admin by user ID."""
        stmt = select(models.Admin).where(models.Admin.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def is_admin(self, user_id: int) -> bool:
        """Check if user is admin."""
        admin = await self.get_by_user_id(user_id)
        return admin is not None

    async def get_role(self, user_id: int) -> Optional[str]:
        """Get admin role."""
        admin = await self.get_by_user_id(user_id)
        return admin.role if admin else None

    async def has_permission(self, user_id: int, permission: str) -> bool:
        """Check if user has permission."""
        admin = await self.get_by_user_id(user_id)
        if not admin:
            return False
        
        role = AdminRole(admin.role)
        return permission in role.permissions or "all" in role.permissions

    async def get_all_admins(self, role: Optional[str] = None) -> List[models.Admin]:
        """Get all admins, optionally filtered by role."""
        if role:
            stmt = select(models.Admin).where(models.Admin.role == role)
        else:
            stmt = select(models.Admin)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_admins_by_role(self, role: str) -> List[models.Admin]:
        """Get admins by specific role."""
        stmt = select(models.Admin).where(models.Admin.role == role)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_admin_count(self) -> int:
        """Get total admin count."""
        stmt = select(func.count(models.Admin.id))
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def update_role(self, user_id: int, role: str) -> Optional[models.Admin]:
        """Update admin role."""
        admin = await self.get_by_user_id(user_id)
        if admin:
            admin.role = role
            await self.session.flush()
        return admin

    async def remove_admin(self, user_id: int) -> bool:
        """Remove admin status."""
        admin = await self.get_by_user_id(user_id)
        if admin:
            await self.session.delete(admin)
            await self.session.flush()
            return True
        return False

    async def get_owner_id(self) -> Optional[int]:
        """Get the owner user ID."""
        stmt = select(models.Admin).where(models.Admin.role == AdminRole.OWNER.value)
        result = await self.session.execute(stmt)
        admin = result.scalars().first()
        return admin.user_id if admin else None

    async def get_broadcasters(self) -> List[models.Admin]:
        """Get all broadcasters."""
        return await self.get_admins_by_role(AdminRole.BROADCASTER.value)

    async def get_content_managers(self) -> List[models.Admin]:
        """Get all content managers."""
        return await self.get_admins_by_role(AdminRole.CONTENT_MGR.value)
