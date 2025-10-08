# 🤖 GitHub Actions Setup Guide

## Quick Setup: Automated Data Pipeline

Follow these steps to enable automated data collection and loading.

### Step 1: Add Snowflake Credentials (5 minutes)

1. **Go to your GitHub repository**
   - Navigate to: https://github.com/Abdoul84/data-engineering-portfolio

2. **Open Settings**
   - Click **Settings** (top menu)
   - Click **Secrets and variables** (left sidebar)
   - Click **Actions**

3. **Add Repository Secrets**
   
   Click **New repository secret** for each:

   | Name | Value | Where to Find |
   |------|-------|---------------|
   | `SNOWFLAKE_ACCOUNT` | `abc12345.us-east-1` | Snowflake → Account → Locator |
   | `SNOWFLAKE_USER` | `your_username` | Your Snowflake login |
   | `SNOWFLAKE_PASSWORD` | `your_password` | Your Snowflake password |

   **Finding your Snowflake account identifier:**
   ```
   Format: <account_locator>.<region>
   Example: xy12345.us-east-1
   
   In Snowflake UI:
   1. Click on your name (top right)
   2. Click "Account"
   3. Copy the account locator
   4. Add your region (e.g., us-east-1, us-west-2)
   ```

4. **Optional: Add AWS Credentials** (skip if not using S3)
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

### Step 2: Enable the Workflow (2 minutes)

1. **Go to Actions tab**
   - Click **Actions** in your repository

2. **Enable workflows** (if needed)
   - Click "I understand my workflows, go ahead and enable them"

3. **Find your workflow**
   - Look for "Senegal Data Pipeline - Automated Data Collection"

### Step 3: Test Run (5 minutes)

1. **Manual trigger**
   - Click on "Senegal Data Pipeline" workflow
   - Click **Run workflow** dropdown (right side)
   - Click green **Run workflow** button

2. **Watch it run**
   - Click on the running workflow
   - Expand each step to see logs
   - ✅ Green = Success
   - ❌ Red = Failed (check logs)

3. **Check Snowflake**
   ```sql
   USE DATABASE SENEGAL_ANALYTICS;
   SELECT COUNT(*) FROM development_facts;
   SELECT * FROM presidents_dim;
   ```

### Step 4: Set Your Schedule

The workflow runs **every Monday at 8 AM UTC** by default.

**To change the schedule:**

1. Edit `.github/workflows/senegal-data-pipeline.yml`
2. Find the `cron` line:
   ```yaml
   schedule:
     - cron: '0 8 * * 1'  # Current: Monday 8 AM
   ```

3. **Popular schedules:**
   ```yaml
   # Every day at midnight UTC
   - cron: '0 0 * * *'
   
   # Every Sunday at 9 AM UTC
   - cron: '0 9 * * 0'
   
   # First of every month at 6 AM UTC
   - cron: '0 6 1 * *'
   
   # Every 12 hours
   - cron: '0 */12 * * *'
   ```

   Use [crontab.guru](https://crontab.guru/) to create custom schedules!

### What Happens Automatically?

Every run:
1. ✅ Collects fresh data from World Bank API (30+ indicators)
2. ✅ Updates Senegalese presidential information
3. ✅ Uploads to S3 (if configured)
4. ✅ Loads everything into Snowflake
5. ✅ Creates summary report
6. ✅ Saves data as downloadable artifacts (30 days)

### Viewing Results

#### Check Run History
```
GitHub → Actions → Workflow runs
```
Click any run to see:
- ✅ Success/failure status
- 📊 Summary report
- 📝 Detailed logs
- 💾 Downloadable artifacts

#### Get Notifications
- Automatic emails on failures (default)
- Configure: Settings → Notifications

#### Add Status Badge to README
```markdown
![Pipeline Status](https://github.com/Abdoul84/data-engineering-portfolio/actions/workflows/senegal-data-pipeline.yml/badge.svg)
```

### Cost & Limits

**GitHub Actions (Public Repos):**
- ✅ **100% FREE** 
- ✅ Unlimited action minutes
- ✅ 2GB artifact storage

**Snowflake:**
- ⚠️ Charges for compute (warehouse time)
- ⚠️ Charges for storage
- 💡 **Tip**: Set auto-suspend to 5 minutes
- 💡 **Tip**: Use smallest warehouse (X-Small)
- 💡 **Tip**: Data load takes ~1-2 minutes = minimal cost

**Expected cost per run:**
- Data collection: $0 (World Bank API is free!)
- GitHub Actions: $0 (free for public repos)
- Snowflake: ~$0.01-0.05 per run (with X-Small warehouse)

### Troubleshooting

#### ❌ "Snowflake connection failed"
**Fix:**
1. Verify account format: `account_locator.region` (not just locator)
2. Check username/password are correct
3. Ensure user has ACCOUNTADMIN role
4. Check if warehouse exists and is available

#### ❌ "No module named 'snowflake'"
**Fix:** Should auto-install, but check `requirements.txt` includes:
```
snowflake-connector-python==3.6.0
```

#### ❌ "World Bank API timeout"
**Fix:** Usually temporary. Workflow will retry automatically next run.

#### ⚠️ Workflow not running automatically
**Check:**
1. Workflows are enabled (Actions tab)
2. Cron syntax is valid
3. Wait for scheduled time (may take up to 15 min after schedule)

### Advanced Options

#### Run on Push (For Testing)
Uncomment in workflow file:
```yaml
push:
  branches: [ main ]
  paths:
    - '07-presidential-analytics/**'
```

#### Add Slack Notifications
Add this step to workflow:
```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
  if: always()
```

#### Deploy Dashboard Automatically
Create a separate workflow to deploy Streamlit app to Streamlit Cloud or other hosting.

### Next Steps

Once automated:
1. ✅ Your Snowflake data updates automatically
2. ✅ Dashboard always shows latest data
3. ✅ You can focus on analysis, not data collection
4. ✅ Perfect for demonstrating to recruiters!

**In interviews, you can say:**
> "I built an automated data pipeline that runs weekly via GitHub Actions, collecting development data from the World Bank API and loading it into Snowflake. It requires zero manual intervention and costs virtually nothing to run."

---

## 📸 Screenshots to Take for Your Portfolio

1. GitHub Actions workflow running successfully
2. Workflow summary showing data loaded
3. Snowflake query showing fresh data
4. Artifacts downloaded and opened

These demonstrate your automation skills! 🚀

---

**Questions?** Check the main README or `.github/workflows/README.md`

