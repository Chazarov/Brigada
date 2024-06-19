from sqlalchemy import String, Integer, Boolean, DateTime, func, Table, ForeignKey, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from sqlalchemy.ext.asyncio import AsyncSession



class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default = func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default = func.now())

    async def delete(self, session:AsyncSession):
        session.delete(self)
        await session.commit()


user_workgroup = Table(
    'user_workgroup', 
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('workgroup_id', ForeignKey('work_groups.id'), primary_key=True)
)



class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String(40), nullable = False)
    phone_number: Mapped[str] = mapped_column(String(40), nullable = False)

    work_groups: Mapped[list["Work_group"]] = relationship(
        'Work_group',
        secondary=user_workgroup,
        back_populates='users'
    )

    

class Work_group(Base):
    __tablename__ = "work_groups"
    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    title: Mapped[str] = mapped_column(String(40), nullable = False)
    is_public: Mapped[bool] = mapped_column(Boolean)

    users: Mapped[list[User]] = relationship(
        'User',
        secondary=user_workgroup,
        back_populates='work_groups'
    )

class Work_object(Base):
    __tablename__ = "work objects"
    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    title: Mapped[str] = mapped_column(String(40), nullable = False)

class Admin(Base):
    __tablename__ = "admin"
    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(40), nullable = False)

    
