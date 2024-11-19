import yaml
from datetime import datetime, timedelta

def load_config():
    with open('config/config.yml', 'r') as file:
        return yaml.safe_load(file)

def get_date_range(config):
    """Calculate date range based on config settings"""
    today = datetime.now()
    start_days = config['gmail']['fetch']['default_date_range']['start_days']
    end_days = config['gmail']['fetch']['default_date_range']['end_days']
    
    start_date = (today - timedelta(days=start_days)).strftime('%Y/%m/%d')
    end_date = (today - timedelta(days=end_days)).strftime('%Y/%m/%d')
    
    return start_date, end_date
