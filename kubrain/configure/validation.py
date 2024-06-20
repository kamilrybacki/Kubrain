from __future__ import annotations
import dataclasses
import enum

import pydantic

import kubrain.assets.schemas

from kubrain.types.data import BaseKubrainDataModel


def _get_available_schemas() -> enum.Enum:
    class _RegisteredSchemas(enum.Enum):
        pass

    for schema in kubrain.assets.schemas.__models__.values():
        setattr(
            _RegisteredSchemas,
            schema.__tag__,  # type: ignore
            schema
        )
    return _RegisteredSchemas  # type: ignore


AvailableSchemas = _get_available_schemas()


class SchemaParsingException(Exception):
    def __init__(self, message):
        super().__init__(message)


# pylint: disable=invalid-name
class _SchemaLoader:  # pylint: disable=too-few-public-methods
    cache: dict[str, ValidationSchema] = {}

    @classmethod
    def load(cls, name: str) -> type[BaseKubrainDataModel]:
        schema = getattr(
            AvailableSchemas,
            name
        )
        if not issubclass(schema, BaseKubrainDataModel):
            raise SchemaParsingException(
                f'Schema {name} is not a valid schema'
            )
        cls.cache[name] = schema
        return schema


@dataclasses.dataclass(frozen=True, kw_only=True)
class ValidationSchema:
    name: str

    _model: type[BaseKubrainDataModel]

    @classmethod
    def construct(cls, name: str) -> ValidationSchema:
        if name not in _SchemaLoader.cache:
            _SchemaLoader.cache[name] = ValidationSchema(
                name=name,
                _model=_SchemaLoader.load(name)  # type: ignore
            )
        return _SchemaLoader.cache[name]

    def validate(self, data: dict) -> ValidationResults:
        try:
            self._model(**data)
            return ValidationResults(
                valid=True,
                schema=self._model.model_json_schema(),
                errors=[],
                data=data
            )
        except pydantic.ValidationError as validation_error:
            return ValidationResults(
                valid=False,
                schema=self._model.model_json_schema(),
                errors=[
                    FieldValidationError(
                        name=str(error['loc'][0]),
                        message=error['msg']
                    )
                    for error in validation_error.errors()
                ],
                data=data
            )


@dataclasses.dataclass(frozen=True, kw_only=True)
class FieldValidationError:
    name: str
    message: str


@dataclasses.dataclass(frozen=True, kw_only=True)
class ValidationResults:
    valid: bool
    schema: dict
    errors: list[FieldValidationError]
    data: dict = dataclasses.field(default_factory=dict)


def against_schema(data: dict, schema: str) -> ValidationResults:
    return ValidationSchema.construct(schema).validate(data)
