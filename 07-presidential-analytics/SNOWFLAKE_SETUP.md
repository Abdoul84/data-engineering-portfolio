# ❄️ Snowflake Setup Guide

## Quick Start: Set Up Snowflake for Senegal Analytics

### Step 1: Create Snowflake Account (5 minutes)

1. **Sign up for free trial**
   - Go to: https://signup.snowflake.com/
   - Choose your cloud provider (AWS, Azure, or GCP)
   - Choose region closest to you (e.g., US East)
   - Create account (30-day free trial with $400 credits)

2. **Complete registration**
   - Verify email
   - Set username and password
   - Log into Snowflake

3. **Note your account identifier**
   ```
   Format: <account_locator>.<region>
   Example: xy12345.us-east-1
   
   To find it:
   1. Click your name (top right)
   2. Click "Account"
   3. Copy the "Account Locator"
   4. Add your region (shown in URL or account page)
   ```

### Step 2: Create Warehouse (2 minutes)

In Snowflake UI:

```sql
-- Create a small warehouse for data loading
CREATE WAREHOUSE IF NOT EXISTS COMPUTE_WH
  WAREHOUSE_SIZE = 'X-SMALL'
  AUTO_SUSPEND = 300        -- Auto-suspend after 5 minutes
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE;

-- Grant usage
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE ACCOUNTADMIN;
```

Or use the UI:
1. Click **Admin** → **Warehouses**
2. Click **+ Warehouse**
3. Name: `COMPUTE_WH`
4. Size: `X-Small`
5. Auto Suspend: `5 minutes`
6. Click **Create Warehouse**

### Step 3: Run Table Creation Scripts (2 minutes)

**Option A: Using Snowflake UI**

1. Click **Worksheets** in left menu
2. Copy and paste the SQL from these files (in order):
   - `sql/ddl/presidents_dim.sql`
   - `sql/ddl/economic_facts.sql`
   - `sql/ddl/performance_view.sql`
3. Click **Run All** (or Ctrl+Enter)

**Option B: Using SnowSQL CLI**

```bash
cd 07-presidential-analytics

# Install SnowSQL (if not already installed)
# https://docs.snowflake.com/en/user-guide/snowsql-install-config

# Run scripts
snowsql -a <your_account> -u <your_username> -f sql/ddl/presidents_dim.sql
snowsql -a <your_account> -u <your_username> -f sql/ddl/economic_facts.sql
snowsql -a <your_account> -u <your_username> -f sql/ddl/performance_view.sql
```

### Step 4: Verify Setup

Run this query in Snowflake:

```sql
-- Check database and tables exist
USE DATABASE SENEGAL_ANALYTICS;
USE SCHEMA PUBLIC;

SHOW TABLES;

-- Should see:
-- PRESIDENTS_DIM
-- DEVELOPMENT_FACTS
```

### Step 5: Configure Local Access

**Create config file:**

```bash
cd 07-presidential-analytics
cp config/config.yaml.example config/config.yaml
```

**Edit `config/config.yaml`:**

```yaml
snowflake:
  account: "xy12345.us-east-1"      # Your account
  user: "YOUR_USERNAME"              # Your username
  password: "YOUR_PASSWORD"          # Your password
  warehouse: "COMPUTE_WH"
  database: "SENEGAL_ANALYTICS"
  schema: "PUBLIC"
  role: "ACCOUNTADMIN"
```

**Or use environment variables (more secure):**

```bash
export SNOWFLAKE_ACCOUNT="xy12345.us-east-1"
export SNOWFLAKE_USER="your_username"
export SNOWFLAKE_PASSWORD="your_password"
```

### Step 6: Test Connection & Load Data

```bash
cd 07-presidential-analytics

# Collect data (if not already done)
python src/ingest/worldbank_api.py
python src/ingest/presidents_data.py

# Load to Snowflake
python src/load/snowflake_loader.py
```

Expected output:
```
======================================================================
🇸🇳 SENEGAL ANALYTICS - Snowflake Data Loader
======================================================================
✅ Connected to Snowflake successfully
📋 Step 1: Creating tables...
👥 Step 2: Loading presidents data...
✅ Loaded 5 presidents records
📊 Step 3: Loading development indicators...
✅ Loaded 1,234 development indicator records
✅ Step 4: Verifying data...
🎉 DATA LOAD COMPLETE!
```

### Step 7: Query Your Data

```sql
USE DATABASE SENEGAL_ANALYTICS;

-- View presidents
SELECT 
    president_name,
    party,
    start_date,
    end_date,
    tenure_days / 365.25 as years_in_office
FROM presidents_dim
WHERE is_active = TRUE
ORDER BY start_date;

-- View development indicators summary
SELECT 
    indicator_name,
    MIN(year) as earliest_year,
    MAX(year) as latest_year,
    COUNT(*) as data_points,
    AVG(value) as avg_value
FROM development_facts
GROUP BY indicator_name
ORDER BY indicator_name;

-- GDP Growth over time
SELECT 
    year,
    president_name,
    value as gdp_growth_pct
FROM development_facts
WHERE indicator_code = 'NY.GDP.MKTP.KD.ZG'
  AND year >= 1960
ORDER BY year;

-- Compare presidents by average GDP growth
SELECT 
    president_name,
    party,
    ROUND(AVG(value), 2) as avg_gdp_growth,
    COUNT(*) as years_with_data
FROM development_facts
WHERE indicator_code = 'NY.GDP.MKTP.KD.ZG'
  AND president_name IS NOT NULL
GROUP BY president_name, party
ORDER BY president_name;
```

## Cost Management

### Free Trial Details
- ✅ $400 in credits
- ✅ 30 days duration
- ✅ Full access to all features

### After Trial
**Typical costs for this project:**
- **Storage**: ~$0.01-0.10/month (very small dataset)
- **Compute**: ~$2/month (if you run queries daily)
- **Total**: **~$2-3/month** with minimal usage

**Cost optimization tips:**
1. ✅ Use **X-Small** warehouse (cheapest)
2. ✅ Set **auto-suspend** to 5 minutes
3. ✅ Use **auto-resume** (only pay when active)
4. ✅ Run pipeline weekly (not daily)
5. ✅ Suspend warehouse when not in use

**Check costs:**
```sql
-- View warehouse usage
SELECT 
    WAREHOUSE_NAME,
    SUM(CREDITS_USED) as total_credits
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE START_TIME >= DATEADD(day, -30, CURRENT_TIMESTAMP())
GROUP BY WAREHOUSE_NAME;
```

## GitHub Actions Integration

Once Snowflake is set up, add credentials to GitHub:

1. **Go to GitHub repo**
   - Settings → Secrets and variables → Actions

2. **Add secrets:**
   - `SNOWFLAKE_ACCOUNT`: `xy12345.us-east-1`
   - `SNOWFLAKE_USER`: `your_username`
   - `SNOWFLAKE_PASSWORD`: `your_password`

3. **Test workflow:**
   - Actions tab → "Senegal Data Pipeline" → Run workflow

See `GITHUB_ACTIONS_SETUP.md` for details.

## Troubleshooting

### "Failed to connect to Snowflake"

**Check:**
1. Account identifier format: `account_locator.region` (not just locator!)
2. Username and password are correct
3. Warehouse exists and is available
4. User has proper permissions

**Common fixes:**
```sql
-- Grant warehouse usage
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE ACCOUNTADMIN;

-- Start warehouse if suspended
ALTER WAREHOUSE COMPUTE_WH RESUME;
```

### "Table does not exist"

**Fix:**
```sql
-- Verify database exists
SHOW DATABASES LIKE 'SENEGAL_ANALYTICS';

-- If not, run table creation scripts
-- See Step 3 above
```

### "Insufficient privileges"

**Fix:**
```sql
-- Grant necessary privileges
GRANT ALL ON DATABASE SENEGAL_ANALYTICS TO ROLE ACCOUNTADMIN;
GRANT ALL ON SCHEMA PUBLIC TO ROLE ACCOUNTADMIN;
GRANT ALL ON ALL TABLES IN SCHEMA PUBLIC TO ROLE ACCOUNTADMIN;
```

### "Warehouse timeout"

**Fix:**
```sql
-- Resume warehouse manually
ALTER WAREHOUSE COMPUTE_WH RESUME;

-- Check warehouse status
SHOW WAREHOUSES LIKE 'COMPUTE_WH';
```

## Security Best Practices

1. ✅ **Never commit credentials** to Git
2. ✅ Use **environment variables** for local development
3. ✅ Use **GitHub Secrets** for CI/CD
4. ✅ Enable **MFA** on Snowflake account
5. ✅ Use **least privilege** (create separate user for apps)
6. ✅ Rotate passwords regularly

### Create Separate User for Applications

```sql
-- Create a dedicated user (more secure than using admin)
CREATE USER senegal_pipeline_user 
  PASSWORD = 'strong_password_here'
  DEFAULT_WAREHOUSE = COMPUTE_WH
  DEFAULT_ROLE = DATA_LOADER;

-- Create role
CREATE ROLE IF NOT EXISTS DATA_LOADER;

-- Grant permissions
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE DATA_LOADER;
GRANT USAGE ON DATABASE SENEGAL_ANALYTICS TO ROLE DATA_LOADER;
GRANT USAGE ON SCHEMA PUBLIC TO ROLE DATA_LOADER;
GRANT INSERT, SELECT, UPDATE ON ALL TABLES IN SCHEMA PUBLIC TO ROLE DATA_LOADER;

-- Assign role to user
GRANT ROLE DATA_LOADER TO USER senegal_pipeline_user;
```

## Resources

- 📘 [Snowflake Free Trial](https://signup.snowflake.com/)
- 📖 [Snowflake Documentation](https://docs.snowflake.com/)
- 🐍 [Python Connector Guide](https://docs.snowflake.com/en/user-guide/python-connector)
- 💰 [Pricing Calculator](https://www.snowflake.com/pricing/)
- 🎓 [Snowflake University](https://learn.snowflake.com/) (Free courses)

---

**Need help?** Check the main README or create an issue!

