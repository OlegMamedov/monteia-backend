import datetime
import random
import json
import uuid

from datetime import timedelta, datetime
from starlette.background import BackgroundTasks

from fastapi import APIRouter, Depends, Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import aiohttp

from database.models import User, Token, Journals, Cards, Auth, Orders, Tags, Reviews
from routers.main.schemas import RegisterSchema, LoginSchema, AuthSchema, ReviewSchema
from database.utils import (
    get_user_by_login,
    get_auth_by_login_and_code,
    get_user_by_id_and_login,
    count_entry_by_user_id,
    delete_journal_by_entry_number,
    get_journal_by_entry_number_and_userid,
    get_card_by_id,
    get_div_by_id,
    get_order_by_user_id,
    delete_tag_by_id,
    get_reviews
    )
from database.db import async_session
from routers.main.utils import (get_zodiac_sign,
                                create_access_token,
                                decode_token,
                                generate_verify_code,
                                send_verify_code, lucky_num,
                                get_response_from_gigachat,
                                send_request,
                                get_order_status,
                                text_in_audio
                                )

from config import MERCHANT_ID, API_URL, SECRET_KEY


router = APIRouter(prefix = "", tags=["Main"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/")


@router.get('/user/me')
async def get_user(token: str):

    payload = decode_token(token)

    try:
        id = payload.get("user_id")
        number = payload.get("number")
    except:
        JSONResponse({'error': 'You don\'t authenticated'})


    user = await get_user_by_id_and_login(id, number)

    if not user:
        return JSONResponse({'error': 'User not found'}, 404)

    current_time = datetime.utcnow()

    if current_time - user.lucky_rait_time >= timedelta(hours=24):
        user.lucky_rait = lucky_num()
        user.lucky_rait_time = current_time
        async with async_session() as session:
            await session.commit()


    return {
        'first_name': user.f_name,
        'last_name': user.l_name,
        'bithday_date': user.birthday_date,
        'zodiac_sign': user.zodiac_sign,
        'lucky_raiting': user.lucky_rait
    }



@router.post('/register/')
async def verificate_user(data: RegisterSchema):
    user = await get_user_by_login(data.number)

    if user:
        return JSONResponse({'error': 'Phone number already exists.'}, 401)


    user = User(number=data.number,
                f_name=data.f_name,
                l_name=data.l_name,
                birthday_date = data.birthday_date,
                lucky_rait_time = datetime.utcnow(),
                lucky_rait = lucky_num(),
                created_at = datetime.utcnow(),
                zodiac_sign = get_zodiac_sign(str(data.birthday_date)),
                referal_link = uuid.uuid4()
                )


    try:
        async with async_session() as session:
            session.add(user)
            await session.commit()
        return {'message': 'User registered successfully'}
    except Exception as e:
        return JSONResponse({'error': str(e)}, 500)



@router.post('/login/')
async def verificate_number(data: LoginSchema):
    user = await get_user_by_login(data.number)

    if not user:
        return JSONResponse({'error': 'Phone number not found.'},401)

    exp_time = datetime.utcnow() + timedelta(minutes=2)
    code = generate_verify_code()

    auth = Auth(user_id = user.id,
                number=data.number,
                code=code,
                expiration_time=exp_time)

    async with async_session() as session:
        session.add(auth)
        await session.commit()

    sms_sent = send_verify_code(data.number, code)
    if sms_sent:
        return JSONResponse({'message': 'Check code in your phone'})
    else:
        return JSONResponse({'error': 'Check your phone number'},401)




@router.post('/auth/')
async def auth(data: AuthSchema):
    auth = await get_auth_by_login_and_code(data.number, data.code)
    user = await get_user_by_login(data.number)

    if not auth:
        return JSONResponse({'error': 'Invalid phone number'}, 401)

    if not auth.is_code_valid():
        return JSONResponse({'error': 'Code has expired'}, 401)

    if auth.code != data.code:
        return JSONResponse({'error': 'Invalid code'}, 401)

    token = create_access_token(data={"sub": 'monteia',
                                      "user_id": user.id,
                                      "number": user.number
                                      })

    new_token = Token(token = token,
                        auth_id = auth.id)

    async with async_session() as session:
        session.add(new_token)
        await session.commit()

    return {"access_token": token,
            "token_type": "Bearer"}



@router.post("/journal/add/entry")
async def add_entry(text_for_entry: str, token: str):
    payload = decode_token(token)

    try:
        id = payload.get("user_id")
        number = payload.get("number")
    except:
        JSONResponse({'error': 'You don\'t authenticated'})


    user = await get_user_by_id_and_login(id, number)

    nums_entry = await count_entry_by_user_id(user.id)

    entry = Journals(user_id=user.id,
                     entry_number=nums_entry + 1,
                     content = text_for_entry
                     )

    async with async_session() as session:
        session.add(entry)
        await session.commit()

    return JSONResponse({'message': 'The entry was successfully added'}, 200)


@router.get("/journal/get/entry")
async def get_journal(entry_number: int, token: str):
    payload = decode_token(token)

    try:
        id = payload.get("user_id")
        number = payload.get("number")
    except:
        JSONResponse({'error': 'You don\'t authenticated'})


    user = await get_user_by_id_and_login(id, number)

    if not user:
        return JSONResponse({'error': 'User not found'}, 404)

    journal = await get_journal_by_entry_number_and_userid(entry_number, user.id)

    return {"entry_number": journal.entry_number,
            "content": journal.content}

@router.delete("/journal/delete/entry")
async def del_entry(entry_number: int, token: str):
    payload = decode_token(token)

    try:
        id = payload.get("user_id")
        number = payload.get("number")
    except:
        JSONResponse({'error': 'You don\'t authenticated'})


    user = await get_user_by_id_and_login(id, number)

    if not user:
        return JSONResponse({'error': 'User not found'}, 404)


    journal = await get_journal_by_entry_number_and_userid(entry_number, user.id)

    if not journal:
        return JSONResponse({'error': 'User not found'}, 404)

    await delete_journal_by_entry_number(entry_number, user.id)

    return JSONResponse({'message': 'Entry was deleted success'}, 201)

@router.post("/journal/edit/entry")
async def edit_entry(entry_number: int, content: str, token: str):
    payload = decode_token(token)

    try:
        id = payload.get("user_id")
        number = payload.get("number")
    except:
        JSONResponse({'error': 'You don\'t authenticated'})


    user = await get_user_by_id_and_login(id, number)

    get_entry = await get_journal_by_entry_number_and_userid(entry_number, user.id)

    get_entry.content = content

    async with async_session() as session:
        session.add(get_entry)
        await session.commit()

    return JSONResponse({'message': 'Entry was edited'}, 201)


@router.post("/chat/")
async def chat(query: str, id: int):


        return "All good"




@router.get('/buy/')
async def get_status(buy_id: int, token: str):
    payload = decode_token(token)

    try:
        id = payload.get("user_id")
        number = payload.get("number")
    except:
        JSONResponse({'error': 'You don\'t authenticated'})

    user = await get_user_by_id_and_login(id, number)
    div = await get_div_by_id(buy_id)

    buy_order = API_URL.create_order(
        type_ = 'buy',  # Тип ордера
        amount = div.price * 100,  # Сумма платежа в минорных единицах
        currency = 'RUB',  # Валюта
        method_type = 'card_number',  # Тип: phone_number, card_number
        customer_id = user.id,  # Customer ID
        invoice_id = 'invoice1'  # Invoice ID
    )

    order_id = buy_order["order_id"]

    new_order = Orders(user_id=user.id,
                       div_id =div.id,
                       order_id=order_id)
    async with async_session() as session:
        session.add(new_order)
        await session.commit()

    return JSONResponse({'link': f'https://secure.legitpay.io/payment/{order_id}'})

@router.get('/get/divination')
async def get_div(token: str, div_id: int, query: str):
    payload = decode_token(token)

    forbidden_words = ['Смерть',
                       'Умереть',
                       'Самоубийство',
                       'Убить'
                       ]

    try:
        id = payload.get("user_id")
        number = payload.get("number")
    except:
        JSONResponse({'error': 'You don\'t authenticated'})

    user = await get_user_by_id_and_login(id, number)
    order = await get_order_by_user_id(user.id)

    # if get_order_status(order.id) == 'wait pay':
    #     JSONResponse({'error': 'wait pay'})

    div = await get_div_by_id(div_id)

    randomId_cards = []
    randomName_card = []
    while len(randomId_cards) < div.count_cards:
        randomId_cards.append(random.randint(1, 78))

    for i in randomId_cards:
        card = await get_card_by_id(i)
        randomName_card.append(card.name)

    try:
        chat_response = get_response_from_gigachat(query, randomName_card)
        # chat_response = {"cards": [{"id": "старуха", "text": "В прошлой жизни вы были мудрой и уважаемой женщиной."},
        #                            {"id": "сиды", "text": "Вы были связаны с магией и тайными знаниями."},
        #                            {"id": "дикая охота", "text": "Ваша жизнь была полна приключений и опасностей."}],
        #                 "sum": "В прошлой жизни вы были мудрой женщиной, связанной с магией и тайными знаниями, и ваша жизнь была полна приключений и опасностей."}
        audio_response = []
        for i in chat_response["cards"]:
            audio_response.append(i["id"])
            for j in i["text"]:
                if j in forbidden_words:
                    return JSONResponse({'error': 'The answer has forbidden words'})
            audio_response.append(i["text"])
            print(audio_response)
            text_in_audio(audio_response)
            audio_response = []

        audio_response.append(chat_response["sum"])
        print(str(audio_response))
        text_in_audio(audio_response)

        return {'gigaChat_response': chat_response,
                'audio_response': ''}

    except:
        JSONResponse({'error': 'bot was not responses'}, 401)


@router.post('/create/tags/')
async def tags_save(tags: str, token: str):
    payload = decode_token(token)

    try:
        id = payload.get("user_id")
        number = payload.get("number")
    except:
        JSONResponse({'error': 'You don\'t authenticated'})

    user = await get_user_by_id_and_login(id, number)

    tag = Tags(user_id=user.id,
               tag = tags
               )

    async with async_session() as session:
        session.add(tag)
        await session.commit()

    return JSONResponse({'message': 'Tag was added to base'})

@router.delete('/delete/tags')
async def delete_tags(tag_id: int, token: str):
    payload = decode_token(token)

    try:
        id = payload.get("user_id")
        number = payload.get("number")
    except:
        JSONResponse({'error': 'You don\'t authenticated'})

    user = await get_user_by_id_and_login(id, number)

    try:
        await delete_tag_by_id(tag_id, user.id)
        return JSONResponse({'message': 'Tag was deleted success'}, 201)
    except:
        return JSONResponse({'error': 'There is no tag with that id'}, 403)


@router.post('/created/review')
async def created_review(data: ReviewSchema):
    payload = decode_token(data.token)

    try:
        id = payload.get("user_id")
        number = payload.get("number")
    except:
        JSONResponse({'error': 'You don\'t authenticated'})

    user = await get_user_by_id_and_login(id, number)
    created_at = datetime.utcnow()
    review = Reviews(user_id = user.id,
                     name = user.f_name + " " + user.l_name[0] + ".",
                     review = data.text,
                     rating = data.rating,
                     created_at = created_at.date()
                     )

    async with async_session() as session:
        session.add(review)
        await session.commit()


@router.post('/get/review')
async def created_review(token: str):
    payload = decode_token(token)

    try:
        id = payload.get("user_id")
        number = payload.get("number")
    except:
        JSONResponse({'error': 'You don\'t authenticated'})

    user = await get_user_by_id_and_login(id, number)
    reviews = await get_reviews()

    return reviews
