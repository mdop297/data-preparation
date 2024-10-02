from src.config_schemas.config_schema import Config
from src.utils.config_utils import get_config


@get_config(config_path="../configs", config_name="config")
def data_preparation(config: Config) -> None:
    print(config)


if __name__ == "__main__":
    data_preparation() 