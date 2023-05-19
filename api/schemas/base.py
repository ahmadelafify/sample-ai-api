from abc import abstractmethod
from enum import Enum
from typing import Union
from uuid import UUID, uuid4

from bson import ObjectId
from pymongo.collection import Collection
from pydantic import Field
import pymongo

from api.models.base import BaseModelMetaABC, BaseModel


def ends_in_mongo_operator(key: str):
    operators = ["eq", "gt", "lt", "in", "ne", "regex"]
    for operator in operators:
        if key.endswith(f"_{operator}"):
            return operator


class OrderType(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class BaseDBModel(BaseModel, metaclass=BaseModelMetaABC):
    id: UUID = Field(None, alias="_id", description="DB Object Id")

    def __init__(self, **kwargs):
        self.collection_name: str
        super().__init__(**kwargs)

    @classmethod
    def _key(cls, query: dict):
        key = {}
        default_op = 'eq'
        for k, v in query.items():
            op = ends_in_mongo_operator(k)
            k = k[:(len(op) + 1) * -1] if op else k
            op = op if op else default_op
            key[k] = {f'${op}': v}
        return key

    @classmethod
    def unique_id(cls):
        return uuid4()

    def _get_id(self):
        return self.id if self.id else self.unique_id()

    @classmethod
    @abstractmethod
    def _get_collection(cls) -> Collection:
        pass

    @classmethod
    def collection(cls) -> Collection:
        return cls._get_collection()

    @classmethod
    def get_one(cls, **kwargs) -> __qualname__:
        if kwargs:
            raw = cls.collection().find_one(cls._key(kwargs))
        else:
            raw = None
        return cls(**raw) if raw else None

    @classmethod
    def exists(cls, **kwargs) -> bool:
        return bool(cls.get_one(**kwargs))

    @classmethod
    def _get_many(cls, query: dict = None) -> __qualname__:
        if query is None:
            query = {}
        return cls.collection().find(cls._key(query))

    @classmethod
    def get_all(cls, skip: int = 0, limit: int = 0, order: tuple[str, OrderType] = None, **kwargs) -> Union[list[__qualname__], __qualname__]:
        raw = cls._get_many(kwargs)
        if limit is not None:
            raw = raw.limit(limit)
        if skip is not None:
            raw = raw.skip(skip)
        if isinstance(order, tuple):
            raw = raw.sort(key_or_list=order[0], direction=pymongo.DESCENDING if order[1] is OrderType.DESC else pymongo.ASCENDING)
        return ([cls(**r) for r in raw] if raw else []) if limit != 1 else cls(**raw[0]) if raw else None

    @classmethod
    def get_all_count(cls) -> int:
        return cls.collection().count_documents(filter={})

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        obj.persist()
        return obj

    def persist(self):
        self.id = self._get_id()
        data = self.dict()
        return self.collection().insert_one({'_id': str(data.pop("id")), **data})

    def save(self):
        data = self.dict()
        data.pop("id")
        return self.collection().replace_one({'_id': str(self._get_id())}, data)

    @classmethod
    def delete_id(cls, _id: str):
        cls.collection().delete_many({"_id": _id})

    def delete(self):
        return self.delete_id(_id=str(self.id))

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            UUID: str
        }
