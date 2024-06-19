from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from Database.models import User, Work_group, Work_object


async def get_user_by_id(session:AsyncSession, user_id:int):
    q = select(User).where(User.id == user_id)
    r = await session.execute(q)
    return r.scalar()

async def get_group_by_id(session:AsyncSession, group_id:int):
    q = select(Work_group).where(Work_group.id == group_id)
    r = await session.execute(q)
    return r.scalar()

async def get_users_in_group(session:AsyncSession, group_id:int):
    q = select(User).join(User.work_groups).where(Work_group.id == group_id)
    r = await session.execute(q)
    return r.scalars().all()




async def user_add_group(session:AsyncSession, user_id:int, group_id:int):
    group = await get_group_by_id(session = session, group_id = group_id)
    user = await get_user_by_id(session = session, user_id = user_id)

    if group is None:
        raise ValueError(f"Group with id {group_id} does not exist")
    
    if user is None:
        raise ValueError(f"Group with id {user_id} does not exist")

    user.work_groups.append(group)
    await session.commit()
    return user





async def add_user(session:AsyncSession, user_id:int, name:int, phone_number:int, start_group_id:str):
    q = select(Work_group).where(Work_group.id == start_group_id)
    r = await session.execute(q)
    group = r.scalar_one_or_none()

    if group is None:
        raise ValueError(f"Group with id {start_group_id} does not exist")
   
    obj = User(
        id = user_id,
        name = name,
        phone_number = phone_number,
        work_groups = [group]

    )

    session.add(obj)
    await session.commit()
    return obj

async def add_group(session:AsyncSession, title:str, is_public:bool):
    obj = Work_group(
        title = title,
        is_public = is_public,
    )




    







