import yaml
import kubrain.configure.validation


def load_bytes(raw_data: bytes, data_schema: str) -> kubrain.configure.validation.ValidationResults:
    try:
        loaded_yaml = yaml.safe_load(raw_data)
        return kubrain.configure.validation.against_schema(
            data=loaded_yaml, schema=data_schema
        )
    except yaml.YAMLError as yaml_error:
        raise ValueError(f'Error parsing file: {yaml_error}') from yaml_error


def load_kubrain_config(config_data: bytes) -> kubrain.configure.validation.ValidationResults:
    return load_bytes(config_data, 'KUBRAIN')
