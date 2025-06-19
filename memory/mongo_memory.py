from logger_config.logger_config import logger
from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import traceback


load_dotenv()

try:
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("MONGO_URI not found in environment variables.")

    client = MongoClient(mongo_uri)
    memory_checkpointer = MongoDBSaver(client)

    logger.info("MongoDB checkpointer initialized successfully.")

except Exception as e:
    logger.error(f"Failed to initialize MongoDB checkpointer: {e}")
    logger.debug(traceback.format_exc())
    checkpointer = None  