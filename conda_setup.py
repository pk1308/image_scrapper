import os
from re import sub
import subprocess
import sys
from pathlib import Path

from loguru import logger

_PYTHON_VERSION_ = "python==3.8"
ENV_NAME = "image_scrapper"

logger.add(
    sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>"
)


def conda_CreateEnv():
    try:
        subprocess.run(["conda", "deactivate"])
        env_path = os.path.join(os.getcwd(), "env")
        logger.info(f"env_path: {env_path}", features=["f-strings", "bold"])
        logger.info(
            f'{"#"*20} Creating a virtual environment {"#"*20}',
            color="green",
            features=["f-strings", "bold"],
        )
        subprocess.run(["conda", "create", "-n", ENV_NAME, _PYTHON_VERSION_, "-y"])
        logger.info(
            f'{"#"*20} Activating the virtual environment {"#"*20}',
            features=["f-strings", "bold"],
        )
        subprocess.run(["conda", "deactivate"])
        subprocess.run(["conda", "activate", ENV_NAME])
        logger.info(
            f'{"#"*20} Installing the dependencies {"#"*20}',
            features=["f-strings", "bold"],
        )
        if os.path.isfile("requirements_dev.txt"):
            subprocess.run(["pip3", "install", "-r", "requirements.txt"])
        elif os.path.isfile("requirements.txt"):
            subprocess.run(["pip3", "install", "-r", "requirements_dev.txt"])
        else:
            logger.info(
                "No requirements.txt or requirements_dev.txt file found",
                features=["f-strings", "bold"],
            )
    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    conda_CreateEnv()
