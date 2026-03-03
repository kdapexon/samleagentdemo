import os
from dotenv import load_dotenv

class Config:
    """Handle application configuration."""
    
    def __init__(self):
        load_dotenv()
        self.data_dir = os.getenv('DATA_DIR', './data')
        self.output_format = os.getenv('OUTPUT_FORMAT', 'csv')
        self.debug = os.getenv('DEBUG', 'False').lower() == 'true'
