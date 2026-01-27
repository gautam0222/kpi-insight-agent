# KPI Intelligence System

AI-powered KPI monitoring and analysis system for retail/ecommerce businesses.

## Features

- **Talk-to-Data**: Ask questions in natural language
- **KPI Monitoring**: Detect revenue changes and anomalies
- **Causal Analysis**: Identify why KPIs changed
- **Action Recommendations**: Get business-ready recommendations

## Setup

1. **Install dependencies**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Configure API Key**:
   - Get free API key from https://openrouter.ai/keys
   - Edit `.env` file and add your key:
```
OPENROUTER_API_KEY=your_actual_key_here
```

3. **Verify data**:
```bash
ls data/kpi_data.csv
```

## Usage

### 1. Talk-to-Data (Natural Language Queries)
```bash
python cli.py ask "What is the total revenue for the last 14 days?"
python cli.py ask "Show revenue trend for Home & Kitchen category"
python cli.py ask "Which products have the highest sales?"
python cli.py ask "What is the average discount percentage?"
```

### 2. KPI Monitoring
```bash
# Monitor all KPIs
python cli.py monitor

# Monitor specific date range
python cli.py monitor --start-date 2025-01-01 --end-date 2025-01-15

# Monitor specific category
python cli.py monitor --category "Electronics"

# Monitor specific product
python cli.py monitor --product "iPhone"
```

### 3. Causal Analysis
```bash
# Explain recent KPI changes
python cli.py explain

# Analyze last 14 days
python cli.py explain --days 14
```

### 4. Action Recommendations
```bash
# Get recommendations for recent changes
python cli.py recommend

# Get recommendations for last 14 days
python cli.py recommend --days 14
```

## Configuration

Edit `.env` to adjust:
- `ALERT_THRESHOLD`: Percentage change to trigger alerts (default: 15)
- `ROLLING_WINDOW`: Days for baseline calculation (default: 7)

## Logs

System logs are saved to `logs/kpi_system.log`

## Example Workflow
```bash
# 1. Check for recent KPI changes
python cli.py monitor

# 2. Analyze why changes occurred
python cli.py explain

# 3. Get actionable recommendations
python cli.py recommend

# 4. Ask specific questions
python cli.py ask "What caused revenue to drop on 2025-01-15?"
```

## Dataset

- **File**: `data/kpi_data.csv`
- **Records**: 500 products across 90 days
- **KPIs**: Revenue, Discount, Marketing Spend, Supply Chain Efficiency, Ratings

## Architecture
```
kpi_intel/
├── cli.py                 # Main CLI interface
├── app/
│   ├── services/
│   │   ├── talk_to_data.py   # NL query processing
│   │   ├── monitor.py        # KPI change detection
│   │   ├── causal.py         # Root cause analysis
│   │   └── recommend.py      # Action recommendations
│   └── core/
│       ├── config.py         # Configuration
│       ├── data_loader.py    # Data loading/filtering
│       └── logger.py         # Logging setup
└── data/
    └── kpi_data.csv          # Dataset
```

## Troubleshooting

**No data loaded**: Ensure `data/kpi_data.csv` exists

**API errors**: Verify OPENROUTER_API_KEY in `.env`

**Import errors**: Activate venv and reinstall requirements