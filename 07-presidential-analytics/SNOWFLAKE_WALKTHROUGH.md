# ❄️ Snowflake Setup Walkthrough - Step by Step

## Part 1: Create Your Snowflake Account (5 minutes)

### Step 1: Sign Up

1. **Go to**: https://signup.snowflake.com/
2. **Choose Edition**: Standard (free trial)
3. **Choose Cloud Provider**: 
   - AWS (recommended)
   - Select region closest to you (e.g., US East)
4. **Fill in**:
   - First Name
   - Last Name
   - Email
   - Company (can use "Personal" or your name)
   - Country
5. **Click**: "CONTINUE"
6. **Check email** for verification link
7. **Click link** and create password

### Step 2: Log In & Get Your Account Identifier

1. **Log into Snowflake** (you'll be redirected after signup)
2. **Find your account identifier**:
   - Look at the URL in your browser
   - Format: `https://app.snowflake.com/<ACCOUNT_IDENTIFIER>/`
   - OR Click your name (top right) → "Account"
   
3. **Write it down**:
   ```
   Account Locator: _____________ (e.g., ABC12345)
   Region: _____________ (e.g., us-east-1)
   Full Account: _____________ (e.g., ABC12345.us-east-1)
   
   Username: _____________
   Password: _____________
   ```

---

## Part 2: Create Warehouse (2 minutes)

### Option A: Using Web UI (Easiest)

1. **Click** "Warehouses" in left sidebar (or Admin → Warehouses)
2. **Click** "+ Warehouse" button (top right)
3. **Fill in**:
   - Name: `COMPUTE_WH`
   - Size: **X-Small** (cheapest!)
   - Advanced Options:
     - Auto Suspend: **5 Minutes**
     - Auto Resume: **✓ Checked**
     - Initially Suspended: **✓ Checked**
4. **Click** "Create Warehouse"

### Option B: Using SQL (Copy-Paste This)

1. **Click** "Worksheets" in left sidebar
2. **Copy and paste** this SQL:

```sql
-- Create warehouse
CREATE WAREHOUSE IF NOT EXISTS COMPUTE_WH
  WAREHOUSE_SIZE = 'X-SMALL'
  AUTO_SUSPEND = 300
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Warehouse for Senegal analytics pipeline';

-- Verify it was created
SHOW WAREHOUSES LIKE 'COMPUTE_WH';
```

3. **Click** "Run" (or press Ctrl+Enter / Cmd+Enter)
4. **Check results** below - should see your warehouse

---

## Part 3: Create Database & Tables (3 minutes)

### Step 1: Create Database

In the Worksheets tab, **copy and paste** this:

```sql
-- =================================================================
-- STEP 1: Create Database
-- =================================================================

CREATE DATABASE IF NOT EXISTS SENEGAL_ANALYTICS
  COMMENT = 'Senegal Presidential & Development Analytics';

-- Use the database
USE DATABASE SENEGAL_ANALYTICS;

-- Create schema
CREATE SCHEMA IF NOT EXISTS PUBLIC;
USE SCHEMA PUBLIC;

-- Verify
SHOW DATABASES LIKE 'SENEGAL_ANALYTICS';
```

**Click "Run All"** (or select all and Ctrl+Enter)

### Step 2: Create Presidents Table

**Copy and paste** this:

```sql
-- =================================================================
-- STEP 2: Create Presidents Dimension Table
-- =================================================================

USE DATABASE SENEGAL_ANALYTICS;
USE SCHEMA PUBLIC;

CREATE TABLE IF NOT EXISTS presidents_dim (
    president_key INT AUTOINCREMENT PRIMARY KEY,
    president_id INT NOT NULL,
    president_name VARCHAR(100) NOT NULL,
    party VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    terms INT,
    tenure_days INT,
    is_current BOOLEAN,
    key_policies TEXT,
    notable TEXT,
    
    -- SCD Type 2 fields
    effective_date DATE NOT NULL,
    expiration_date DATE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    
    -- Audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_presidents_id 
  ON presidents_dim(president_id);
  
CREATE INDEX IF NOT EXISTS idx_presidents_active 
  ON presidents_dim(is_active);

-- Verify
DESCRIBE TABLE presidents_dim;
```

**Click "Run All"**

### Step 3: Create Development Facts Table

**Copy and paste** this:

```sql
-- =================================================================
-- STEP 3: Create Development Facts Table
-- =================================================================

USE DATABASE SENEGAL_ANALYTICS;
USE SCHEMA PUBLIC;

CREATE TABLE IF NOT EXISTS development_facts (
    fact_key INT AUTOINCREMENT PRIMARY KEY,
    year INT NOT NULL,
    indicator_code VARCHAR(50) NOT NULL,
    indicator_name VARCHAR(200),
    value DECIMAL(20, 4),
    president_id INT,
    president_name VARCHAR(100),
    party VARCHAR(100),
    
    -- Country metadata
    country VARCHAR(100) DEFAULT 'Senegal',
    country_code VARCHAR(10) DEFAULT 'SN',
    
    -- Data quality fields
    is_estimated BOOLEAN DEFAULT FALSE,
    data_source VARCHAR(100) DEFAULT 'World Bank',
    data_quality_score DECIMAL(3, 2),
    
    -- Audit fields
    ingestion_timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    
    -- Unique constraint
    CONSTRAINT uk_development_obs UNIQUE (year, indicator_code)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_dev_year 
  ON development_facts(year);
  
CREATE INDEX IF NOT EXISTS idx_dev_indicator 
  ON development_facts(indicator_code);
  
CREATE INDEX IF NOT EXISTS idx_dev_president 
  ON development_facts(president_id);

-- Verify
DESCRIBE TABLE development_facts;
```

**Click "Run All"**

### Step 4: Verify Everything

**Copy and paste** this to verify:

```sql
-- =================================================================
-- STEP 4: Verify Setup
-- =================================================================

USE DATABASE SENEGAL_ANALYTICS;
USE SCHEMA PUBLIC;

-- Show all tables
SHOW TABLES;

-- Should see:
-- PRESIDENTS_DIM
-- DEVELOPMENT_FACTS

-- Check warehouse
SHOW WAREHOUSES LIKE 'COMPUTE_WH';

-- Check database
SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_WAREHOUSE();
```

**Click "Run All"**

✅ If you see both tables listed, you're all set!

---

## Part 4: Save Your Credentials

### Fill This Out:

```
================================
SNOWFLAKE CREDENTIALS
================================

Account Information:
-------------------
Account Locator: _______________ (e.g., ABC12345)
Region: _______________ (e.g., us-east-1)
Full Account Identifier: _______________ (format: ABC12345.us-east-1)

Login Details:
-------------
Username: _______________
Password: _______________

Database Configuration:
----------------------
Warehouse: COMPUTE_WH
Database: SENEGAL_ANALYTICS
Schema: PUBLIC
Role: ACCOUNTADMIN

URLs:
-----
Snowflake UI: https://app.snowflake.com/<YOUR_ACCOUNT>/
Account URL: https://<ACCOUNT_LOCATOR>.snowflakecomputing.com/

Setup Date: _______________
```

**IMPORTANT**: 
- ✅ Save this somewhere secure (password manager, encrypted file)
- ❌ DO NOT commit to Git
- ❌ DO NOT share publicly

---

## Part 5: Test Connection from Python (5 minutes)

### Create Config File

1. **Open terminal** in your project:

```bash
cd /Users/moz/data-engineering-portfolio/07-presidential-analytics
```

2. **Create config file**:

```bash
cp config/config.yaml.example config/config.yaml
```

3. **Edit** `config/config.yaml`:

```yaml
snowflake:
  account: "ABC12345.us-east-1"      # YOUR account identifier
  user: "YOUR_USERNAME"               # YOUR username  
  password: "YOUR_PASSWORD"           # YOUR password
  warehouse: "COMPUTE_WH"
  database: "SENEGAL_ANALYTICS"
  schema: "PUBLIC"
  role: "ACCOUNTADMIN"
```

4. **Save the file**

### Test the Connection

**Run this** in terminal:

```bash
python -c "
import snowflake.connector
import yaml

# Load config
with open('config/config.yaml') as f:
    config = yaml.safe_load(f)

# Connect
conn = snowflake.connector.connect(
    account=config['snowflake']['account'],
    user=config['snowflake']['user'],
    password=config['snowflake']['password'],
    warehouse=config['snowflake']['warehouse'],
    database=config['snowflake']['database'],
    schema=config['snowflake']['schema']
)

# Test query
cursor = conn.cursor()
cursor.execute('SELECT CURRENT_DATABASE(), CURRENT_WAREHOUSE()')
result = cursor.fetchone()
print(f'✅ Connected! Database: {result[0]}, Warehouse: {result[1]}')
conn.close()
"
```

**Expected output**:
```
✅ Connected! Database: SENEGAL_ANALYTICS, Warehouse: COMPUTE_WH
```

❌ **If you get an error**:
- Check account identifier format (must include region!)
- Verify username/password
- Check if warehouse is running

---

## Part 6: Load Sample Data (5 minutes)

### Collect Data First

```bash
cd /Users/moz/data-engineering-portfolio/07-presidential-analytics

# Collect World Bank data
python src/ingest/worldbank_api.py

# Collect presidents data
python src/ingest/presidents_data.py
```

**Wait** for both to complete (~2-3 minutes)

### Load to Snowflake

```bash
# Load everything to Snowflake
python src/load/snowflake_loader.py
```

**Expected output**:
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

### Verify in Snowflake UI

Go back to Snowflake Worksheets and run:

```sql
USE DATABASE SENEGAL_ANALYTICS;

-- Check presidents
SELECT 
    president_name,
    party,
    YEAR(start_date) as start_year,
    YEAR(end_date) as end_year
FROM presidents_dim
WHERE is_active = TRUE
ORDER BY start_date;

-- Should see 5 presidents from 1960 to present

-- Check development data
SELECT 
    indicator_name,
    COUNT(*) as data_points,
    MIN(year) as earliest_year,
    MAX(year) as latest_year
FROM development_facts
GROUP BY indicator_name
ORDER BY indicator_name
LIMIT 10;

-- Should see 30+ indicators with data from 1960s
```

✅ **If you see data, you're done!**

---

## Part 7: Add to GitHub Secrets (Final Step)

### For Automated Pipeline

1. **Go to**: https://github.com/Abdoul84/data-engineering-portfolio/settings/secrets/actions

2. **Click**: "New repository secret"

3. **Add each secret**:

| Name | Value (use YOUR credentials!) |
|------|-------------------------------|
| `SNOWFLAKE_ACCOUNT` | `ABC12345.us-east-1` |
| `SNOWFLAKE_USER` | `your_username` |
| `SNOWFLAKE_PASSWORD` | `your_password` |

4. **Test the workflow**:
   - Go to: Actions tab
   - Click "Senegal Data Pipeline"  
   - Click "Run workflow"
   - Click green "Run workflow" button

5. **Watch it run!**

---

## 🎉 You're Done!

### What You Now Have:

✅ Snowflake account with $400 free credits  
✅ COMPUTE_WH warehouse (auto-suspend saves money)  
✅ SENEGAL_ANALYTICS database  
✅ 2 tables: presidents_dim, development_facts  
✅ Sample data loaded  
✅ Python connection working  
✅ GitHub Actions configured  

### Next Steps:

1. ✅ Run queries in Snowflake
2. ✅ Let GitHub Actions run automatically (every Monday)
3. ✅ Build dashboard
4. ✅ Add to your resume!

---

## 💡 Quick Reference

**Snowflake UI**: https://app.snowflake.com/  
**Your Account**: `https://app.snowflake.com/<YOUR_ACCOUNT>/`

**Common Queries**:

```sql
-- Switch to your database
USE DATABASE SENEGAL_ANALYTICS;

-- See all tables
SHOW TABLES;

-- Count records
SELECT 
    'Presidents' as table_name,
    COUNT(*) as records
FROM presidents_dim
WHERE is_active = TRUE
UNION ALL
SELECT 
    'Development Data',
    COUNT(*)
FROM development_facts;

-- GDP growth over time
SELECT 
    year,
    president_name,
    value as gdp_growth_percent
FROM development_facts
WHERE indicator_code = 'NY.GDP.MKTP.KD.ZG'
ORDER BY year;
```

---

## 🆘 Troubleshooting

### "Connection timeout"
- Check account identifier format: `ACCOUNT.REGION` (not just `ACCOUNT`)
- Verify region matches your signup

### "Invalid username or password"
- Re-enter credentials carefully
- Try resetting password in Snowflake UI

### "Warehouse not found"
- Run the CREATE WAREHOUSE command again
- Check warehouse name is exactly `COMPUTE_WH`

### "Permission denied"
- Use ACCOUNTADMIN role (default for trial accounts)
- Grant yourself permissions if needed

---

**Need help?** Check `SNOWFLAKE_SETUP.md` for detailed troubleshooting!

