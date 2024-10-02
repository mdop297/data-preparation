from src.config_schemas.config_schema import Config
from src.utils.config_utils import get_config
from src.utils.gcp_utils import access_secret_version
from src.utils.data_utils import get_raw_data_with_version

@get_config(config_path="../configs", config_name="config")
def process_data(config: Config) -> None:
    # print(config)
    # my_secret = access_secret_version("cloud-server-435706", "mdop-data-github-access-token")
    # print(f"{my_secret}")
    version = "v1"
    data_local_save_dir = "./data/raw"
    dvc_remote_repo = "https://github.com/mdop297/data-versioning-with-DVC.git"
    dvc_data_folder = "data/raw"
    github_user_name = "mdop297"
    github_access_token = access_secret_version("cloud-server-435706", "mdop-data-github-access-token")
    
    get_raw_data_with_version(version=version,
                              data_local_save_dir=data_local_save_dir,
                              dvc_remote_repo=dvc_remote_repo,
                              dvc_data_folder=dvc_data_folder,
                              github_user_name=github_user_name,
                              github_access_token=github_access_token)

    


if __name__ == "__main__":
    process_data() 