# Вариант 1
# from typing import Any
#
# from typing import List, Any
#
# # импорты
# import sqlalchemy as sq
# from sqlalchemy.orm import declarative_base
# from sqlalchemy import create_engine, MetaData
# from sqlalchemy.orm import Session
# from config import db_url_object
#
# # схема БД
# metadata = MetaData()
# Base = declarative_base()
#
# class Viewed(Base):
#     __tablename__ = 'viewed'
#     profile_id = sq.Column(sq.Integer, primary_key=True)
#     worksheet_id = sq.Column(sq.Integer, primary_key=True)
#
#
# # добавление записи в бд
#
# engine = create_engine(db_url_object)
# Base.metadata.create_all(engine)
# with Session(engine) as session:
#     to_bd = Viewed(profile_id=1, worksheet_id=1)
#     session.add(to_bd)
#     session.commit()
#
# # извлечение записей из БД
#
# engine = create_engine(db_url_object)
# with Session(engine) as session:
#     from_bd = session.query(Viewed).filter(Viewed.profile_id==1).all()
#     for item in from_bd:
#         print(item.worksheet_id)
#

# Вариант 2.
# импорты
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData, Column
from sqlalchemy.orm import Session

from config import db_url_object  #для инициации движка передаетс адрес (url)

metadata = MetaData()
Base = declarative_base()

# def create_tables(engine):
#     Base.metadata.create_all(engine)
#     Base.metadata.drop_all(engine)
# profile_id = not None
# worksheet_id = not None

# conn = {cursor, commit}
# cursor = cur()
# # 1. Удаление таблиц перед запуском
# def delete_db(conn):
#     with conn.cursor() as cur:
#         cur.execute("""
# 		DROP TABLE IF EXISTS viewed
# 		""")
#     conn.commit()

class Viewed(Base):
    __tablename__ = 'viewed'
    profile_id = sq.Column(sq.Integer, primary_key=True)  #это id_пользователя
    worksheet_id = sq.Column(sq.Integer, primary_key=True) #а это id_анкет, которые он просматривает


#добавление записи в БД
def add_user(engine, profile_id, worksheet_id):  #принимает движок и id анкет, которые уже просмотрел профиль id
    with Session(engine) as session:
        to_bd = Viewed(profile_id=profile_id, worksheet_id=worksheet_id)
        session.add(to_bd)
        session.commit()


#извлечение записи из БД
def check_user(engine, profile_id, worksheet_id):
    with Session(engine) as session:
        from_bd = session.query(Viewed).filter(
            Viewed.profile_id == profile_id,
            Viewed.worksheet_id == worksheet_id
        ).first()
        return True if from_bd else False


if __name__ == '__main__':
    engine = create_engine(db_url_object)  # создать движок
    Base.metadata.drop_all(engine) # удалить таблицу
    Base.metadata.create_all(engine)  # создать таблицу
    add_user(engine, 1234, 56789)  #добавить user
    res = check_user(engine, 1234, 56789)
    print(res)

