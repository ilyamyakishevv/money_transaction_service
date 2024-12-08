from datetime import datetime
from abc import abstractmethod
from typing import Optional, Type, Any

from fastapi_filter.contrib.sqlalchemy import Filter
from fastapi import Query

from common.models import Transaction



class AsyncFilter(Filter):
    @abstractmethod
    async def filter(self, query: Query) -> Query:
        pass

class TransactionFilter(AsyncFilter):
    status: Optional[str] = None
    transaction_date__gte: Optional[datetime] = None
    sender_id: Optional[int] = None
    receiver_id: Optional[int] = None

    class Constants(Filter.Constants):
        model = Transaction

    async def filter(self, query: Query) -> Query:
        async def _apply_filter(q: Query, name: str, value: Any) -> Query:
            return filter_map[name](q, value)

        filter_map = {
            "status": lambda q, v: q.filter(Transaction.status == v),
            "transaction_date__gte": lambda q, v: q.filter(
                Transaction.transaction_date >= v
            ),
            "sender_id": lambda q, v: q.filter(
                Transaction.sender_id == v
            ),
            "receiver_id": lambda q, v: q.filter(
                Transaction.receiver_id == v
            ),
        }

        for field_name, field_value in self:
            if field_value is not None and field_name in filter_map:
                query = await _apply_filter(query, field_name, field_value)

        return query
