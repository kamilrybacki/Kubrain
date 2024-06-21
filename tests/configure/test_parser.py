import yaml

import pytest

import kubrain.configure.parser
import kubrain.configure.validation


@pytest.mark.parametrize(
    'test_config, is_valid',
    [
        (
            {'name': 'test', 'version': '1.0.0'},
            False
        ),
        (
            {
                'general': {
                    'name': 'test'
                },
                'build': {},
                'engine': {},
                'deploy': {}
            },
            True
        )
    ]
)
def test_main_config_loading(test_config: dict, is_valid: bool):
    config_as_yaml_bytes = yaml.dump(test_config).encode('utf-8')
    assert kubrain.configure.parser.load_kubrain_config(
        config_data=config_as_yaml_bytes
    ).valid == is_valid
