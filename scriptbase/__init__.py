import logging
import os

SCRIPTBASE_DIRECTORY = os.path.dirname(__file__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
