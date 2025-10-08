# GitHub Actions Workflows

## 🇸🇳 Senegal Data Pipeline

Automated data collection and loading for the Presidential Analytics project.

### What It Does

This workflow automatically:
1. 🌍 Collects latest development data from World Bank API (NO API KEY NEEDED!)
2. 🇸🇳 Updates Senegalese presidential information
3. ☁️ (Optional) Uploads to AWS S3
4. ❄️ Loads data into Snowflake
5. 📊 Generates summary reports
6. 💾 Archives data as artifacts

### Schedule

- **Automatic**: Runs every Monday at 8 AM UTC
- **Manual**: Can be triggered anytime from Actions tab
- **On-demand**: Triggered when pipeline code changes (optional)

### Setup Instructions

#### 1. Add Snowflake Credentials

Go to: **Repository Settings → Secrets and variables → Actions**

Add these secrets:

| Secret Name | Value | Required |
|-------------|-------|----------|
| `SNOWFLAKE_ACCOUNT` | Your Snowflake account (e.g., `abc12345.us-east-1`) | ✅ Yes |
| `SNOWFLAKE_USER` | Your Snowflake username | ✅ Yes |
| `SNOWFLAKE_PASSWORD` | Your Snowflake password | ✅ Yes |
| `AWS_ACCESS_KEY_ID` | AWS access key (for S3) | ⚠️ Optional |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key (for S3) | ⚠️ Optional |

#### 2. Enable Workflows

1. Go to **Actions** tab in your repository
2. Click "I understand my workflows, go ahead and enable them"
3. Find "Senegal Data Pipeline" workflow
4. Click **Enable workflow**

#### 3. Test the Workflow

**Option A: Manual Trigger**
1. Go to **Actions** tab
2. Select "Senegal Data Pipeline"
3. Click **Run workflow** dropdown
4. Click the green **Run workflow** button

**Option B: Wait for Schedule**
- Will run automatically every Monday at 8 AM UTC

### Viewing Results

#### Check Run Status
1. Go to **Actions** tab
2. Click on the latest run
3. View the summary and logs

#### Download Data
1. Go to completed workflow run
2. Scroll to **Artifacts** section
3. Download `senegal-data-XXX.zip`

#### View in Snowflake
```sql
USE DATABASE SENEGAL_ANALYTICS;

-- Check latest data
SELECT 
    COUNT(*) as total_records,
    MIN(year) as earliest_year,
    MAX(year) as latest_year,
    COUNT(DISTINCT indicator_code) as unique_indicators
FROM development_facts;

-- Check presidents
SELECT * FROM presidents_dim WHERE is_active = TRUE;
```

### Customizing the Schedule

Edit `.github/workflows/senegal-data-pipeline.yml`:

```yaml
schedule:
  - cron: '0 8 * * 1'  # Every Monday at 8 AM UTC
```

**Common schedules:**
- Daily at midnight: `0 0 * * *`
- Every Sunday: `0 0 * * 0`
- First day of month: `0 0 1 * *`
- Every 6 hours: `0 */6 * * *`

Use [crontab.guru](https://crontab.guru/) to build custom schedules.

### Monitoring

**Email notifications:**
- GitHub sends email on workflow failures (by default)
- Configure in: Settings → Notifications

**Status badge:**
Add to your README:
```markdown
![Senegal Pipeline](https://github.com/YOUR-USERNAME/data-engineering-portfolio/actions/workflows/senegal-data-pipeline.yml/badge.svg)
```

### Troubleshooting

#### Workflow not running?
- Check if workflows are enabled in Actions tab
- Verify cron schedule syntax
- Ensure secrets are added correctly

#### Snowflake connection failed?
- Verify SNOWFLAKE_ACCOUNT format (should be `account.region`)
- Check user permissions in Snowflake
- Ensure warehouse is running

#### Data collection failed?
- World Bank API should always work (no auth needed)
- Check logs in Actions tab for specific error
- Data might be temporarily unavailable

### Cost Considerations

**GitHub Actions:**
- ✅ **FREE** for public repositories
- ✅ Unlimited minutes for public repos
- ✅ Artifacts storage: free for 30 days

**Snowflake:**
- ⚠️ Charges for compute time
- ⚠️ Storage charges
- 💡 Tip: Use auto-suspend on warehouse
- 💡 Tip: Schedule during free trial or off-peak

### Best Practices

1. ✅ Keep secrets secure (never commit credentials)
2. ✅ Monitor workflow runs regularly
3. ✅ Set appropriate retention for artifacts
4. ✅ Use manual triggers for testing
5. ✅ Review Snowflake costs periodically

### Advanced: Multiple Workflows

You can create additional workflows for:
- **Data validation**: Check data quality after load
- **Dashboard deployment**: Auto-deploy Streamlit app
- **Notifications**: Send Slack/email reports
- **Backup**: Archive data to multiple locations

### Support

- 📖 [GitHub Actions Docs](https://docs.github.com/en/actions)
- ❄️ [Snowflake Connector Docs](https://docs.snowflake.com/en/user-guide/python-connector)
- 🌍 [World Bank API](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation)

---

**Built for the Senegal Presidential Analytics project** 🇸🇳

