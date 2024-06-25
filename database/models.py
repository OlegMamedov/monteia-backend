from sqlalchemy import Column, Integer, String, BigInteger, Float, DateTime, ForeignKey, Date, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta


Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    f_name = Column(String)
    l_name = Column(String)
    number = Column(String)
    birthday_date = Column(Date)
    created_at = Column(DateTime)
    zodiac_sign = Column(String)
    lucky_rait = Column(Integer)
    lucky_rait_time = Column(DateTime)
    referal_link = Column(String)
    referal_parent = Column(String, default=0)
    balance = Column(Float)
    role = Column(String, default="user")

class Auth(Base):
    __tablename__ = 'auth'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    number = Column(String)
    code = Column(String)
    expiration_time = Column(DateTime)

    def is_code_valid(self):
        return datetime.utcnow() < self.expiration_time

class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True)
    auth_id = Column(Integer, ForeignKey('auth.id'))
    token = Column(String)

class Divination(Base):
    __tablename__ = 'divination'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    price = Column(Float)
    type = Column(String)
    language = Column(String)
    query = Column(String)

class DivinationHistory(Base):
    __tablename__ = 'divination_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    divination_id = Column(Integer, ForeignKey('divination.id'))
    created_at = Column(DateTime)

class DivinationInfo(Base):
    __tablename__ = 'divination_info'

    id = Column(Integer, primary_key=True)
    divinations_history_id = Column(Integer, ForeignKey('divination_history.id'))
    value = Column(String)
    type = Column(String)

class Journals(Base):
    __tablename__ = 'journals'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    entry_number = Column(Integer)
    content = Column(Text)

class Cards(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    category = Column(String)
    name = Column(String)
    link_on_image = Column(String)

class Divinations(Base):
    __tablename__ = 'divinations'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    questionForThe_cards = Column(Text)
    count_cards = Column(Integer)
    comment = Column(String)
    price = Column(Float)
    sale_price = Column(Float)


class Positions(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    div_id = Column(Integer, ForeignKey('divinations.id'))
    position_x = Column(Integer)
    position_y = Column(Integer)

class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    div_id = Column(Integer, ForeignKey('divinations.id'))
    order_id = Column(BigInteger)
    price = Column(Float)
    response_giga = Column(Text)


class Tags(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    tag = Column(String)


class Reviews(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String)
    review = Column(Text)
    rating = Column(Integer)
    created_at = Column(Date)