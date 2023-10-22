import time

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate

router = APIRouter(
    prefix='/operations',
    tags=['Operation']
)


@router.get('/long_operation')
@cache(expire=10)
def get_long_op():
    time.sleep(2)
    return 'Много данных которые долго вычисляются'


@router.get('/')
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    result = await session.execute(query)
    return [dict(r._mapping) for r in result]


@router.post('/')
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmnt = insert(operation).values(**new_operation.dict())  # чтобы развернуть Pydantic модель в kwargs юзаем dict и **
    await session.execute(stmnt)  # задействуем сессию. Здесь мы находимся внутри транзакции
    await session.commit()  # говорим что транзакции нужно завершиться
    return {'status': 'success'}
