# pylint: disable=protected-access, too-few-public-methods
import pydoc
import types

import pydantic
import yaml

from kubrain.types.schema import BaseSchemaModel


def _transpile_properties(properties: dict) -> dict[str, tuple]:
    transpiled_properties: dict[str, tuple] = {}
    for name, field in properties.items():
        if 'properties' in field.keys():
            class PropertySchema(BaseSchemaModel):
                __tag__ = name.upper()
            PropertySchema.__name__ = f'{name.capitalize()}Schema'
            nested_schema_model = pydantic.create_model(
                name,
                __base__=PropertySchema,
                **_transpile_properties(
                    field.get('properties', {})
                )
            )
            transpiled_properties[name] = (nested_schema_model, ...)
        else:
            transpiled_properties[name] = (
                pydoc.locate(
                    path=str(field['type'])
                ),
                field.get('default', ...)
            )
            if 'validator' in field.keys():
                validator_function = pydantic.validator(name)(
                    types.FunctionType(
                        code=compile(field.get('validator', ''), '', 'exec'),
                        globals=globals(),
                    )
                )
    return transpiled_properties


def transpile_schema(schema_file: str) -> type[BaseSchemaModel]:
    with open(schema_file, 'r', encoding='utf-8') as file:
        schema = yaml.safe_load(file)

        class RootSchema(BaseSchemaModel):
            __tag__ = schema['name'].upper()
            version: str = schema['version']
            description: str = schema['description']

            @classmethod
            def from_fields(cls, **fields):
                return pydantic.create_model(
                    schema['name'],
                    __base__=cls,
                    **fields
                )

        return RootSchema.from_fields(
            **_transpile_properties(schema['properties'])
        )
