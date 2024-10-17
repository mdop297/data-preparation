from dataclasses import field
from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pydantic.dataclasses import dataclass
from src.config_schemas.data_processing import dataset_cleaner_schema, dataset_readers_schema
from src.config_schemas.dask_cluster import dask_cluster_schema
from src.config_schemas.infrastructure import gcp_schema


@dataclass
class DataProcessingConfig:
    version: str = MISSING
    data_local_save_dir: str = "./data/raw"
    dvc_remote_repo: str = "https://github.com/mdop297/data-versioning-with-DVC.git"
    dvc_data_folder: str = "data/raw"
    github_user_name: str = "mdop297"
    github_access_token_secret_id: str = "mdop-data-github-access-token"
    infrastructure: gcp_schema.GCPConfig = field(default_factory=gcp_schema.GCPConfig)
    # github_access_token = access_secret_version("cloud-server-435706", "mdop-data-github-access-token")
    dataset_reader_manager: dataset_readers_schema.DatasetReaderManagerConfig = MISSING
    dataset_cleaner_manager: dataset_cleaner_schema.DatasetCleanerManagerConfig = MISSING
    dask_cluster: dask_cluster_schema.DaskClusterConfig = MISSING
    processed_data_save_dir: str = MISSING
    docker_image_name:str = MISSING
    docker_image_tag:str = MISSING


def setup_config() -> None:
    gcp_schema.setup_config()
    dataset_readers_schema.setup_config()
    dataset_cleaner_schema.setup_config()
    dask_cluster_schema.setup_config()

    cs = ConfigStore.instance()
    cs.store(name="data_processing_config_schema", node=DataProcessingConfig)
