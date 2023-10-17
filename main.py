from datetime import datetime
from enum import Enum
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title='Trading App'  # add name for our app
)

fake_users = [
    {'id': 1, 'role': 'admin', 'name': 'Bob'},
    {'id': 2, 'role': 'investor', 'name': 'John'},
    {'id': 3, 'role': 'trader', 'name': 'Matt'},
    {'id': 4, 'role': 'investor', 'name': 'Homer', 'degree': [
        {'id': 1, 'created_at': '2020-01-01T00:00:00', 'type_degree': 'expert'},
        {'id': 2, 'created_at': '2020-10-01T00:00:00', 'type_degree': 'master'},
    ]},
]


class DegreeType(Enum):
    newbie = 'newbie'
    expert = 'expert'
    master = 'master'


class Degree(BaseModel):  # если не указать BaseModel ничего не будет работать
    id: int
    created_at: datetime
    type_degree: DegreeType
    # для более строгой валидации определяем класс DegreeType. Определив его мы говорим, что
    # в type_degree мы будем ожидать только 2 значения - 'newbie' и 'expert'


class User(BaseModel):  # создаем сложную структуру данных (
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = 'AAA'
    # Не у всех может быть звание. Чтобы не возникала ошибка internal server, которую видит клиент, используем Optional
    # и задаем пустой список по умолчанию, который будет возвращен если звания нет. Если не указать дефолтное значение
    # по умолчанию, то вернется null


@app.get('/users/{user_id}', response_model=List[User])  # Используем response_model для валидации данных
def get_user(user_id: int):
    return [user for user in fake_users if user.get('id') == user_id]


fake_trades = [
    {'id': 1, 'user_id': 1, 'currency': 'BTC', 'side': 'buy', 'price': 123, 'amount': 2.12},
    {'id': 2, 'user_id': 1, 'currency': 'BTC', 'side': 'sell', 'price': 125, 'amount': 2.12},
    {'id': 3, 'user_id': 1, 'currency': 'BTC', 'side': 'buy', 'price': 124, 'amount': 2.10},
]


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str
    side: str
    price: float = Field(ge=0)  # создаем более строгое правило. Возникнет ошибка при отриц значении
    amount: float


@app.post('/trades')
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {'status': 200, 'data': fake_trades}


'''
Если в swagger изменить значение для ключа amount на "amount" то получим ошибку.
'''
