from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from Database.models import Work_group





async def setup_base_objects(session:AsyncSession):
    await create_base_group(session)


async def create_base_group(session:AsyncSession):

    q = select(Work_group).where(Work_group.id == 0)
    r = await session.execute(q)
    base_group = r.scalar()

    if(base_group is None):
        obj = Work_group(
            id = 0,
            title = "Не определена",
            is_public  = False,
            not_delete = True
        )
        session.add(obj)
        await session.commit()
    else: return