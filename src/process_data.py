from hydra.utils import instantiate
from pathlib import Path
from dask.distributed import Client
from src.config_schemas.data_processing_config_schema import DataProcessingConfig
from src.utils.config_utils import custom_instantiate, get_pickle_config
from src.utils.data_utils import get_raw_data_with_version
from src.utils.gcp_utils import access_secret_version
from src.utils.utils import get_logger
import dask.dataframe as dd
from src.data_processing.dataset_cleaners import DatasetCleanerManager
import os

def process_raw_data(
    df_partition: dd.core.DataFrame, dataset_cleaner_manager: DatasetCleanerManager
) -> dd.core.Series:
    processed_partition: dd.core.Series = df_partition["text"].apply(dataset_cleaner_manager)
    return processed_partition


@get_pickle_config(config_path="src/configs/auto_generated", config_name="data_processing_config")
def process_data(config: DataProcessingConfig) -> None:
    # from omegaconf import OmegaConf

    # print(60 * "=")
    # print(OmegaConf.to_yaml(config))
    # print(60 * "=")
    # return

    logger = get_logger(name=Path(__file__).name)
    logger.info("Processing raw data ...")
    
    processed_data_save_dir = config.processed_data_save_dir
    
    cluster = custom_instantiate(config.dask_cluster)
    client = Client(cluster)
    
    try:
        # github_access_token = access_secret_version(config.infrastructure.project_id, config.github_access_token_secret_id)

        # get_raw_data_with_version(
        #     version=config.version,
        #     data_local_save_dir=config.data_local_save_dir,
        #     dvc_remote_repo=config.dvc_remote_repo,
        #     dvc_data_folder=config.dvc_data_folder,
        #     github_user_name=config.github_user_name,
        #     github_access_token=github_access_token,
        # )

        dataset_reader_manager = instantiate(config=config.dataset_reader_manager)
        dataset_cleaner_manager = instantiate(config=config.dataset_cleaner_manager)

        df = dataset_reader_manager.read_data(config.dask_cluster.n_workers)
        
        print(df.compute().head())
        return
        
        logger.info("Cleaning data ...")
        df = df.assign(
            cleaned_text = df.map_partitions(
                process_raw_data, dataset_cleaner_manager=dataset_cleaner_manager, meta=("text", "object")
                )
            )
        df =  df.compute()
                
        train_parquet_path = os.path.join(processed_data_save_dir, "train.parquet")
        dev_parquet_path = os.path.join(processed_data_save_dir, "dev.parquet")
        test_parquet_path = os.path.join(processed_data_save_dir, "test.parquet")

        train_df = df[df["split"] == "train"]
        dev_df = df[df["split"] == "dev"]
        test_df = df[df["split"] == "test"]
        
        train_df.to_parquet(train_parquet_path)
        dev_df.to_parquet(dev_parquet_path)
        test_df.to_parquet(test_parquet_path)
        
        logger.info("======> Data processing finished! <======")
        
    finally:
        logger.info("Closing dask client and cluster ...")
        client.close()
        cluster.close()


if __name__ == "__main__":
    os.environ["HYDRA_FULL_ERROR"] = "1"
    process_data()
