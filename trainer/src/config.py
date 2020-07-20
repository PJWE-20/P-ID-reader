import os
import logging

# ML Settings
SUBSCRIPTION_ID = os.getenv(
    "SUBSCRIPTION_ID", default="9bc2f845-5f0d-450d-bf32-82d81d9e8445"
)
RESOURCE_GROUP = os.getenv("RESOURCE_GROUP", default="jgazStudentRG")
WORKSPACE_NAME = os.getenv("WORKSPACE_NAME", default="mlvision")
WORKSPACE_REGION = os.getenv("WORKSPACE_REGION", default="westeurope")
GPU_CLUSTER_NAME = "gpu-cluster"


SRC_PATH = os.path.dirname(os.path.realpath(__file__))
MODELS_DIRECTORY = "model"
TRAINED_MODELS_PATH = os.path.join(SRC_PATH, MODELS_DIRECTORY)
GENERATOR_PATH = os.path.join(SRC_PATH, "../../generator/")
GENERATOR_TF_PATH = os.path.join(GENERATOR_PATH, "data/tf/")

MODEL_PATH = "outputs/model"  # AzureML puts its stuff there
TENSORBOARD_PATH = "outputs/tensorboard"

LOGGING_LEVEL = logging.INFO
