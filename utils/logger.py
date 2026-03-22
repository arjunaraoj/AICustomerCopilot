import logging
import sys
from pathlib import Path

def setup_logging(log_level: str = "INFO"):
    Path("logs").mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/copilot.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
