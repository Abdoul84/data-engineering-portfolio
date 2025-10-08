# 🚀 Quick Start Guide - Senegal Presidential Analytics

Get the Senegal Presidential Analytics Pipeline running in minutes!

## Prerequisites

1. **Python 3.8+** installed
2. **NO API KEYS NEEDED!** 🎉 World Bank API is completely free and open
3. **AWS Account** (for S3) - optional for local testing
4. **Snowflake Account** - optional for local testing

## 5-Minute Setup (Local Demo)

### Step 1: Install Dependencies

```bash
cd 07-presidential-analytics
pip install -r config/requirements.txt
```

### Step 2: Collect Data (No Configuration Needed!)

Run the data collection scripts - NO API KEY REQUIRED:

```bash
# Collect Senegal development data from World Bank API (FREE!)
python src/ingest/worldbank_api.py

# Collect Senegalese presidential data
python src/ingest/presidents_data.py
```

✨ **That's it!** The World Bank API is completely free and requires no authentication.

This will save data to `data/raw/` directory.

### Step 3: Launch Dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard will open in your browser at http://localhost:8501

🎉 **Done!** You now have a working Senegal presidential analytics dashboard!

### What You'll See

- 📊 60+ years of Senegal's development data
- 🇸🇳 5 presidents from independence to present
- 📈 Economic, social, and infrastructure metrics
- 🎯 Interactive filtering and comparisons

---

## Full Production Setup

For complete pipeline with S3 and Snowflake:

### 1. AWS S3 Setup

1. Create an S3 bucket:
```bash
aws s3 mb s3://your-presidential-analytics-bucket
```

2. Update `config/config.yaml` with your bucket details.

3. Upload data to S3:
```bash
python src/ingest/s3_uploader.py
```

### 2. Snowflake Setup

1. Create database and tables:
```bash
snowsql -f sql/ddl/presidents_dim.sql
snowsql -f sql/ddl/economic_facts.sql
snowsql -f sql/ddl/performance_view.sql
```

2. Load data from S3 to Snowflake (update paths in the script):
```bash
snowsql -f sql/dml/incremental_load.sql
```

3. Update dashboard to connect to Snowflake (uncomment section in `dashboard/app.py`)

---

## Testing the Pipeline

### Verify Data Collection

```bash
# Check collected data
ls -lh data/raw/

# Should see files like:
# - fred_economic_data_YYYYMMDD_HHMMSS.parquet
# - presidents_YYYYMMDD_HHMMSS.parquet
```

### Verify S3 Upload

```bash
aws s3 ls s3://your-bucket/presidential-data/raw/
```

### Query Snowflake

```sql
-- Check row counts
SELECT 'Presidents', COUNT(*) FROM presidents_dim WHERE is_active = TRUE
UNION ALL
SELECT 'Economic Facts', COUNT(*) FROM economic_facts;

-- Check date range
SELECT 
    MIN(observation_date) as earliest,
    MAX(observation_date) as latest,
    COUNT(DISTINCT series_id) as metrics_count
FROM economic_facts;
```

---

## Common Issues & Solutions

### Issue: "No module named 'requests'"

**Solution**: Install dependencies:
```bash
pip install -r config/requirements.txt
```

### Issue: "boto3.exceptions.NoCredentialsError"

**Solution**: Configure AWS credentials:
```bash
aws configure
# Or set environment variables:
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
```

### Issue: "Snowflake connection error"

**Solution**: Check your Snowflake credentials in `config.yaml` or environment variables:
```bash
export SNOWFLAKE_ACCOUNT="your-account"
export SNOWFLAKE_USER="your-user"
export SNOWFLAKE_PASSWORD="your-password"
```

---

## Next Steps

1. ✅ Explore the dashboard - filter by party, president, metrics
2. ✅ Customize metrics in `config/config.yaml`
3. ✅ Add more FRED series IDs
4. ✅ Schedule automated runs with cron or Airflow
5. ✅ Deploy dashboard to Streamlit Cloud

---

## Environment Variables Reference

For production deployment (cloud only):

```bash
# NO API KEYS NEEDED FOR DATA COLLECTION!
# World Bank API is completely free

# Only needed for cloud deployment:
# AWS
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_DEFAULT_REGION="us-east-1"

# Snowflake
export SNOWFLAKE_ACCOUNT="your-account.region"
export SNOWFLAKE_USER="your-user"
export SNOWFLAKE_PASSWORD="your-password"
export SNOWFLAKE_WAREHOUSE="COMPUTE_WH"
export SNOWFLAKE_DATABASE="SENEGAL_ANALYTICS"
```

---

## Project Structure Quick Reference

```
07-presidential-analytics/
├── src/
│   ├── ingest/           # Data collection scripts
│   └── utils/            # Configuration and logging
├── sql/
│   ├── ddl/              # Table definitions
│   └── dml/              # Data manipulation
├── dashboard/            # Streamlit dashboard
├── config/               # Configuration files
└── data/                 # Local data storage (gitignored)
```

---

**Need Help?** Check the main [README.md](README.md) for detailed documentation!

