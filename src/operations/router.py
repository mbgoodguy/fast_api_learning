from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.operations.models import operation

router = APIRouter(
    prefix='/operations',
    tags=['Operation']
)


@router.get('/')
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    result = await session.execute(query)
    return [dict(r._mapping) for r in result]
