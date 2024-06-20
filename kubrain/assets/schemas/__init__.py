import importlib
import os

from kubrain.types.data import BaseKubrainDataModel

__models__: dict[str, type[BaseKubrainDataModel]] = {}

for schema in os.listdir(os.path.dirname(__file__)):
    schema = os.path.basename(schema).removesuffix('.py')
    if schema.startswith('_'):
        continue
    schema_camel_cased_name: str = ''.join(
        word.capitalize()
        for word in schema.split('_')
    )
    schema_module = importlib.import_module(
        f'kubrain.assets.schemas.{schema}'
    )
    __models__[schema_camel_cased_name] = getattr(schema_module, 'Schema')

__all__ = list(__models__.keys())
