import yaml


def load_bytes(raw_data: bytes) -> bytes:
    try:
        return yaml.safe_load(raw_data)
    except yaml.YAMLError as yaml_error:
        raise ValueError(f'Error parsing file: {yaml_error}') from yaml_error
