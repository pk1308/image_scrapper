import logging
import os

logging_str = "[%(asctime)s: %(levelname)s: %(module)s] %(message)s"
log_dir = "./logs"
log_path = os.path.join(log_dir, "running_logs.log")
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[logging.StreamHandler(), logging.FileHandler(log_path)],
)

logger = logging.getLogger("image_scrapper")
