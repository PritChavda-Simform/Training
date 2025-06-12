import logging

# ---------------------
# Logger Configuration
# ---------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler("agent_logs.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)