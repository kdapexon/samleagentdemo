import pandas as pd
from .config import Config

class DataProcessor:
    """Process data files and generate statistics."""
    
    def __init__(self, config=None):
        self.config = config if config else Config()
    
    def read_file(self, filename):
        """Read and parse a CSV data file."""
        return pd.read_csv(filename)
    
    def get_stats(self, data):
        """Calculate basic statistics from the data."""
        return {
            'count': len(data),
            'sum': data['value'].sum(),
            'mean': data['value'].mean()
        }
