from database.db import async_session
from database.models import User, Journals, Cards, Divinations, Auth
from sqlalchemy import select, func, delete

# async def get_user_by_token(token: str):
#     query = (select(User).where(User.token == token))
#     async with async_session() as session:
#         result = await session.execute(query)

#     return result.scalar()

async def get_auth_by_login_and_code(number: str, code: str):
    query = (select(Auth).where((Auth.number == number) & (Auth.code == code)))
    async with async_session() as session:
        result = await session.execute(query)

    return result.scalar()

async def get_user_by_login(number: str):
    query = (select(User).where(User.number == number))
    async with async_session() as session:
        result = await session.execute(query)

    return result.scalar()

async def get_user_by_id_and_login(id: int, number: str):
    query = (select(User).where((User.id == id) & (User.number == number)))
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

async def get_card_by_id(id: int):
    query = (select(Cards).where(Cards.id == id))
    async with async_session() as session:
        result = await session.execute(query)

    return result.scalar()

async def get_div_by_id(id: str):
    query = (select(Divinations).where(Divinations.id == id))
    async with async_session() as session:
        result = await session.execute(query)

    return result.scalar()

