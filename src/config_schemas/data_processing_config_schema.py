from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass
from dataclasses import field
from omegaconf import MISSING

from src.config_schemas.infrastructure import gcp_schema
from src.config_schemas.data_processing import dataset_readers_schema


@dataclass
class DataProcessingConfig:
    version: str = MISSING
    data_local_save_dir : str = "./data/raw"
    dvc_remote_repo : str = "https://github.com/mdop297/data-versioning-with-DVC.git"
    dvc_data_folder : str = "data/raw"
    github_user_name : str = "mdop297"
    github_access_token_secret_id : str = "mdop-data-github-access-token"
    infrastructure: gcp_schema.GCPConfig = field(default_factory=gcp_schema.GCPConfig)
    # github_access_token = access_secret_version("cloud-server-435706", "mdop-data-github-access-token")
    dataset_reader_manager: dataset_readers_schema.DatasetReaderManagerConfig = MISSING

def setup_config() -> None:
    gcp_schema.setup_config()
    dataset_readers_schema.setup_config()
    
    cs = ConfigStore.instance()
    cs.store(name="data_processing_config_schema", node=DataProcessingConfig)
    