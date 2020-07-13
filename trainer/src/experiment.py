import argparse
import logging
import os

from azureml.train.dnn import TensorFlow
from azureml.core import Experiment

from compute import get_or_create_workspace
from config import (
    SUBSCRIPTION_ID,
    RESOURCE_GROUP,
    WORKSPACE_NAME,
    WORKSPACE_REGION,
    LOGGING_LEVEL,
    GPU_CLUSTER_NAME,
)
from data import get_or_create_dataset
from ml_storage import AzureBlobCloudStorage

logger = logging.getLogger(__name__)
logger.setLevel(LOGGING_LEVEL)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a training experiment in AzureML")
    parser.add_argument("experiment_id", type=str, help="""The experiment id""")
    args = parser.parse_args()
    if args.experiment_id:
        experiment_id = args.experiment_id
    else:
        exit(-1)

    ws = get_or_create_workspace(
        SUBSCRIPTION_ID, RESOURCE_GROUP, WORKSPACE_NAME, WORKSPACE_REGION
    )

    # Get the list of files from the blob
    ab = AzureBlobCloudStorage()
    files = ab.list_files(experiment_id)

    # Make sure training dataset exists
    dataset_name = f"a_{experiment_id}"
    dataset = get_or_create_dataset(ws, files, dataset_name)

    # Create the experiment
    experiment_name = experiment_id
    experiment = Experiment(ws, name=experiment_name)

    script_params = {
        "-d": dataset.as_named_input(dataset_name).as_download(),
        "--extra_path": os.path.join(
            f"https/{ab.storage_account}.blob.core.windows.net/pub", f"{experiment_id}/"
        ),
        "-e": f"{experiment_id}",
    }

    # Estimator help: https://github.com/Azure/MachineLearningNotebooks/tree/master/how-to-use-azureml/training-with-deep-learning
    script_folder = "./"
    estimator = TensorFlow(
        source_directory=script_folder,
        compute_target=GPU_CLUSTER_NAME,
        script_params=script_params,
        entry_script="train_tensorflow.py",
        use_gpu=True,
        pip_packages=[
            "azureml-dataprep[fuse]",
            "tensorflow-gpu==2.2.0",
            "pyyaml",
            "git+https://github.com/qubvel/efficientnet@e9fdd43857785fe5ccf3863915dcaf618b86849f#egg=efficientnet",
        ],
    )

    run = experiment.submit(estimator)
    print(run)

    # Tensorboard for the training
    # https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/training-with-deep-learning/export-run-history-to-tensorboard/export-run-history-to-tensorboard.ipynb

    # Configure native distributed training
    # https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-train-tensorflow#distributed-training
