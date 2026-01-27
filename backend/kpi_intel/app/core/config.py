import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
)

class Config:
    # API Configuration
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
    OPENROUTER_MODEL = os.getenv(
        'OPENROUTER_MODEL',
        'nvidia/nemotron-3-nano-30b-a3b:free'
    )
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

    # Data Configuration (FIXED)
    DATA_PATH = os.path.join(BASE_DIR, "kpi_intel", "data", "kpi_data.csv")

    # KPI Monitoring
    ALERT_THRESHOLD = float(os.getenv('ALERT_THRESHOLD', 15))
    ROLLING_WINDOW = int(os.getenv('ROLLING_WINDOW', 7))

    # Logging
    LOG_FILE = os.path.join(BASE_DIR, "kpi_intel", "logs", "kpi_system.log")
    LOG_LEVEL = "INFO"

config = Config()
