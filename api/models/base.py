from abc import ABCMeta

from pydantic import BaseModel as PydanticBaseModel

from pydantic.main import ModelMetaclass


class BaseModelMetaABC(ModelMetaclass, ABCMeta):
    pass


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
