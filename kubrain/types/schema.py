import abc
import typing

import pydantic


# pylint: disable=too-few-public-methods
class BaseSchemaModel(pydantic.BaseModel, abc.ABC):
    @property
    @abc.abstractmethod
    def __tag__(self) -> str:
        pass

    model_config = {
        'from_attributes': True,
        'populate_by_name': True,
    }


class TranspiledSchemaProperty(typing.TypedDict):
    type: typing.Type[BaseSchemaModel] | None | str
    value: pydantic.Field
