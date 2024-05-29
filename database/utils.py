from database.db import async_session
from database.models import User, Journals
from sqlalchemy import select, func, delete

# async def get_user_by_token(token: str):
#     query = (select(User).where(User.token == token))
#     async with async_session() as session:
#         result = await session.execute(query)
    
#     return result.scalar()

async def get_user_by_login(username: str):
    query = (select(User).where(User.username == username))
    async with async_session() as session:
        result = await session.execute(query)

    return result.scalar()

async def get_user_by_id_and_number(id: int, username: str):
    query = (select(User).where((User.id == id) & (User.username == username)))
    async with async_session() as session:
        result = await session.execute(query)

    return result.scalar()

async def get_journal_by_entry_number_and_userid(entry_number: int, user_id: int):
    query = select(Journals).where((Journals.user_id == user_id) & (Journals.entry_number == entry_number))
    async with async_session() as session:
        result = await session.execute(query)

    return result.scalar()

async def count_entry_by_user_id(id: int):
    query = select(func.count()).where(Journals.user_id == id)
    async with async_session() as session:
        result = await session.execute(query)

    return result.scalar()

async def delete_journal_by_entry_number(entry_number: int, user_id: int):
    query = delete(Journals).where((Journals.entry_number == entry_number) & (Journals.user_id  == user_id))
    async with async_session() as session:
        await session.execute(query)
        await session.commit()

