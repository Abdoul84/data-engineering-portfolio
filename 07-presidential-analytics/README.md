# 📊 Senegal Presidential Analytics Pipeline

**A Modern Data Pipeline: API → S3 → Snowflake → Dashboard**

## 🎯 Project Overview

This project demonstrates a production-grade data pipeline that ingests, transforms, and visualizes **Senegalese presidential administration data** alongside economic and development metrics from international organizations. The pipeline enables historical comparison of Senegal's progress across different presidential terms using modern data infrastructure and reliable public APIs.

**Why Senegal?** This unique project showcases data engineering skills while analyzing a fascinating African democracy with 60+ years of peaceful transitions and economic development.

## 🏗️ Architecture

```
APIs (FRED, Census, etc.)
    ↓
Python Ingestion Scripts
    ↓
AWS S3 (Raw & Staged Data)
    ↓
Snowflake (Incremental Refresh)
    ↓
Interactive Web Dashboard
```

## 📈 Data Sources (All Free & Reliable!)

### Economic & Development Metrics
- **World Bank API** (Primary data source - comprehensive, reliable, free)
  - GDP Growth & GDP per capita
  - Population & Demographics
  - Poverty rates & Income inequality
  - Education indicators (literacy, enrollment)
  - Health metrics (life expectancy, mortality)
  - Infrastructure (electricity access, internet usage)
  - Trade & Investment flows
  - Agricultural production

- **REST Countries API** 
  - Country metadata (capital, languages, currency)
  - Geographic information

- **African Development Bank Open Data** (Optional)
  - Regional development indicators
  - Infrastructure projects

### Presidential Data (Manually curated)
- Senegalese presidents from independence (1960-present)
- Political party affiliations
- Terms and transition dates
- Major policy initiatives per administration

## 🎯 Key Features

### 1. **API Data Ingestion**
- Automated data collection from multiple APIs
- Error handling and retry logic
- Rate limiting compliance
- Data validation

### 2. **S3 Data Lake**
- Raw data storage (JSON/Parquet)
- Staged/processed data
- Partitioning by date and data type
- Cost-optimized storage tiers

### 3. **Snowflake Data Warehouse**
- Incremental table refresh (merge logic)
- Slowly Changing Dimensions (SCD Type 2)
- Fact tables for time-series metrics
- Optimized clustering and partitioning

### 4. **Interactive Dashboard**
- Presidential term comparisons
- Economic metrics over time
- Party performance analysis
- Interactive filters and drill-downs

## 🚀 Tech Stack

| Component | Technology |
|-----------|------------|
| **Ingestion** | Python, Requests, Pandas |
| **Storage** | AWS S3, Parquet |
| **Warehouse** | Snowflake |
| **Orchestration** | Apache Airflow (optional) |
| **Dashboard** | Streamlit / Plotly Dash |
| **IaC** | Terraform (optional) |

## 📁 Project Structure

```
07-presidential-analytics/
├── src/
│   ├── ingest/
│   │   ├── fred_api.py          # Economic data ingestion
│   │   ├── presidents_data.py   # Presidential info ingestion
│   │   └── s3_uploader.py       # S3 upload utilities
│   ├── transform/
│   │   ├── process_economic.py  # Economic data transformation
│   │   └── merge_datasets.py    # Combine president + economic data
│   └── utils/
│       ├── config.py             # Configuration management
│       └── logger.py             # Logging utilities
├── sql/
│   ├── ddl/
│   │   ├── presidents_dim.sql   # Presidents dimension table
│   │   ├── economic_facts.sql   # Economic metrics fact table
│   │   └── performance_view.sql # Aggregated performance view
│   └── dml/
│       ├── incremental_load.sql # Merge/upsert logic
│       └── data_quality.sql     # Quality checks
├── dashboard/
│   ├── app.py                   # Streamlit dashboard
│   ├── components/
│   │   ├── metrics.py           # Metric cards
│   │   ├── charts.py            # Visualization components
│   │   └── filters.py           # Filter components
│   └── assets/                  # CSS, images
├── config/
│   ├── config.yaml              # Configuration file
│   └── requirements.txt         # Python dependencies
├── tests/
│   └── test_ingestion.py        # Unit tests
└── README.md                    # This file
```

## 🔧 Setup Instructions

### Prerequisites
```bash
- Python 3.8+
- AWS Account with S3 access
- Snowflake account
- FRED API Key (free from https://fred.stlouisfed.org/)
```

### Installation

1. **Clone and navigate to project**
```bash
cd 07-presidential-analytics
```

2. **Install dependencies**
```bash
pip install -r config/requirements.txt
```

3. **Configure credentials** (Optional for World Bank API - it's free and open!)
```bash
cp config/config.yaml.example config/config.yaml
# Edit config.yaml with your credentials (only needed for AWS/Snowflake)
```

4. **Set environment variables** (Optional - only for cloud deployment)
```bash
# World Bank API is FREE and requires NO API key!

# Only needed for cloud deployment:
export AWS_ACCESS_KEY_ID="your-aws-key"
export AWS_SECRET_ACCESS_KEY="your-aws-secret"
export SNOWFLAKE_ACCOUNT="your-account"
export SNOWFLAKE_USER="your-user"
export SNOWFLAKE_PASSWORD="your-password"
```

## 🎮 Usage

### Step 1: Ingest Data from APIs
```bash
python src/ingest/fred_api.py
python src/ingest/presidents_data.py
```

### Step 2: Upload to S3
```bash
python src/ingest/s3_uploader.py
```

### Step 3: Load to Snowflake
```bash
# Run Snowflake scripts
snowsql -f sql/ddl/presidents_dim.sql
snowsql -f sql/ddl/economic_facts.sql
snowsql -f sql/dml/incremental_load.sql
```

### Step 4: Launch Dashboard
```bash
streamlit run dashboard/app.py
```

## 📊 Dashboard Features

### Presidential Comparison View
- Compare economic metrics across administrations
- Filter by party, time period, specific metrics
- Normalized and absolute value views

### Economic Timeline
- Interactive time-series charts
- Mark presidential transitions
- Overlay multiple metrics

### Performance Scorecard
- Key metrics summary per president
- Ranking and percentile views
- Year-over-year comparisons

## 🔄 Incremental Refresh Strategy

The pipeline uses **incremental merge logic** in Snowflake:

```sql
MERGE INTO economic_facts target
USING staged_economic_data source
ON target.date = source.date 
   AND target.metric_name = source.metric_name
WHEN MATCHED THEN UPDATE SET ...
WHEN NOT MATCHED THEN INSERT ...
```

Benefits:
- Only process new/changed data
- Maintain historical accuracy
- Optimize compute costs
- Enable backfilling

## 📈 Sample Metrics Tracked

| Category | Metrics |
|----------|---------|
| **Economic** | GDP Growth, Unemployment, Inflation |
| **Market** | S&P 500, Dow Jones, NASDAQ |
| **Fiscal** | Deficit, Debt, Government Spending |
| **Trade** | Imports, Exports, Trade Balance |
| **Social** | Poverty Rate, Median Income |

## 🎯 Key Learning Outcomes

### Data Engineering Skills
✅ API integration and data collection  
✅ AWS S3 data lake management  
✅ Snowflake data warehouse design  
✅ Incremental data loading patterns  
✅ Data quality and validation  
✅ Dashboard development  

### Business Value
✅ Historical trend analysis  
✅ Cross-administration comparisons  
✅ Data-driven policy insights  
✅ Accessible visualization  

## 🔐 Security & Best Practices

- ✅ Credentials managed via environment variables
- ✅ AWS IAM roles for S3 access
- ✅ Snowflake role-based access control
- ✅ API key rotation
- ✅ Data encryption at rest and in transit

## 📝 Future Enhancements

- [ ] Add Apache Airflow for orchestration
- [ ] Implement dbt for transformations
- [ ] Add more data sources (census, polling)
- [ ] ML predictions for economic trends
- [ ] Real-time data streaming
- [ ] Mobile-responsive dashboard
- [ ] Export to PDF reports

## 📚 References

- **FRED API Docs**: https://fred.stlouisfed.org/docs/api/
- **Snowflake Merge**: https://docs.snowflake.com/en/sql-reference/sql/merge
- **AWS S3 Best Practices**: https://docs.aws.amazon.com/s3/

## 🙏 Acknowledgments

Part of the Data Engineering Portfolio showcasing modern data pipeline development.

---

**Built with**: Python 🐍 | AWS S3 ☁️ | Snowflake ❄️ | Streamlit 📊

