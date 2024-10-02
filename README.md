# Data Preparation 
simple project to prepare data for mlops project
This is my hands-on project when learning [this course](https://www.udemy.com/course/sustainable-and-scalable-machine-learning-project-development) 
and the code if from [this repo](https://github.com/emkademy/cybulde-data-preparation)

## Steps to modify the template
- docker-compose.yaml
    - image: mlproject-data-preparation
    - container_name: mlproject-data-preparation-container
- Makefile
    - CONTAINER_NAME = mlproject-data-preparation-container
    - prepare-dataset: up
	    
        $(DOCKER_COMPOSE_EXEC) python ./src/prepare_dataset.py
- pyproject.toml
    - [tool.poetry.dependencies]
    - pandas = "~=2.2.3"
    -  nltk = "~=3.9"
    - symspellpy = "~=6.7"
    - fsspec = {version = "~=2024.9", extras = ["gcs"]}
    - gcsfs = "~=2024.9"
    - google-cloud-secret-manager = "~=2.20"
    - fastparquet = "~=2024.5"
    - dvc = {version = "~=3.55.2", extras = ["gdrive", "gs"]}
    - dask = {version = "~=2024.9.1", extras = ["complete"]}
    - distributed = "~=2024.9.1"
    - dask-cloudprovider = {version = "2024.9.1", extras=["gcp"]}
    - dask-ml = "~=2024.4"

- run make lock-dependencies

## 