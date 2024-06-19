from sqlalchemy import String, Integer, Boolean, DateTime, func, Table, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from sqlalchemy.ext.asyncio import AsyncSession



class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default = func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default = func.now())

    async def delete(self, session:AsyncSession):
        session.delete(self)
        await session.commit()


user_workgroup = Table(
    'user_workgroup', Base.metadata,
    mapped_column('user_id', ForeignKey('user.id'), primary_key=True),
    mapped_column('workgroup_id', ForeignKey('work_group.id'), primary_key=True)
)



class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String(40), nullable = False)
    phone_number: Mapped[str] = mapped_column(String(40), nullable = False)

    work_groups: Mapped[list["Work_group"]] = relationship(
        'Work_object',
        secondary=user_workgroup,
        back_populates='users'
    )

    

class Work_group(Base):
    __tablename__ = "work groups"
    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    title: Mapped[str] = mapped_column(String(40), nullable = False)
    is_public: Mapped[bool] = mapped_column(Boolean)

    sers: Mapped[list[User]] = relationship(
        'User',
        secondary=user_workgroup,
        back_populates='work_groups'
    )

class Work_object(Base):
    __tablename__ = "work objects"
    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    title: Mapped[str] = mapped_column(String(40), nullable = False)

    
