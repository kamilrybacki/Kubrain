import abc
import pydantic


# pylint: disable=too-few-public-methods
class BaseKubrainDataModel(pydantic.BaseModel, abc.ABC):
    @property
    @abc.abstractmethod
    def __tag__(self) -> str:
        pass

    model_config = {
        'from_attributes': True,
        'populate_by_name': True,
    }
