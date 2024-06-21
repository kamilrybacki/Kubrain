import os

import kubrain.utils.transpile


MAIN_CONFIG_SCHEMA_PATH = os.path.join(
    os.path.dirname(__file__),
    '../../',
    'schemas/configs',
    'main.yaml'
)


def test_main_config_schema_transpilation():
    transpiled_schema = kubrain.utils.transpile.transpile_schema(
        MAIN_CONFIG_SCHEMA_PATH
    )
    print(transpiled_schema.schema_json())
