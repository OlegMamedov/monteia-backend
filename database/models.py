from sqlalchemy import Column, Integer, String, BigInteger, Float, DateTime, ForeignKey, Date, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base


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
    role = Column(String, default="user")

class Auth(Base):
    __tablename__ = 'auth'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    number = Column(String)
    code = Column(String)
    expiration_time = Column(DateTime)

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
    count_cards = Column(Integer)
    comment = Column(String)

class Positions(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    div_id = Column(Integer, ForeignKey('divinations.id'))
    position_x = Column(Integer)
    position_y = Column(Integer)

