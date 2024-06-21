import pydantic

from kubrain.types.schema import BaseSchemaModel


class GeneralConfig(BaseSchemaModel):
    __tag__ = 'GENERAL'

    name: str = pydantic.Field(
        description='Name of the project',
    )


class BuildConfig(BaseSchemaModel):
    __tag__ = 'BUILD'


class EngineConfig(BaseSchemaModel):
    __tag__ = 'ENGINE'


class DeployConfig(BaseSchemaModel):
    __tag__ = 'DEPLOY'


class Schema(BaseSchemaModel):
    __tag__ = 'KUBRAIN'

    general: GeneralConfig = pydantic.Field(
        description='General configuration for the project',
        title='General Configuration'
    )
    build: BuildConfig = pydantic.Field(
        description='Build configuration for the project',
        title='Build Configuration'
    )
    engine: EngineConfig = pydantic.Field(
        description='Engine configuration for the project',
        title='Engine Configuration'
    )
    deploy: DeployConfig = pydantic.Field(
        description='Deploy configuration for the project',
        title='Deploy Configuration'
    )
