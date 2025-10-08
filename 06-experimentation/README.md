# 🧪 KPI Design & Experimentation Framework

## Overview

This project demonstrates how to design comprehensive KPI frameworks and experimentation strategies aligned with business objectives. It covers hypothesis formulation, A/B test design, metrics selection, and statistical analysis for product optimization.

## 🎯 Project Goals

- Design actionable KPI hierarchies
- Create hypothesis-driven experiments
- Build proper A/B test allocation strategies
- Link leading indicators to lagging outcomes
- Analyze user journeys for optimization
- Develop data-driven product recommendations

## 🛠️ Key Concepts

### 1. KPI Framework Design
Hierarchical metrics structure linking daily actions to business outcomes.

**KPI Types**:
- **North Star Metric**: Single metric defining success
- **Leading Indicators**: Predictive, actionable metrics
- **Lagging Indicators**: Outcome metrics (revenue, retention)
- **Counter Metrics**: Safety checks (technical debt, churn)

### 2. Experimentation Design
Statistical framework for testing product changes.

**Components**:
- Hypothesis formulation
- Test cell allocation
- Success metrics definition
- Statistical power analysis
- Results interpretation

### 3. User Journey Mapping
Understanding product flows to identify optimization opportunities.

**Elements**:
- Onboarding flow
- Core feature adoption
- Engagement patterns
- Retention drivers
- Churn triggers

## 📂 Project Structure

```
06-experimentation/
├── README.md                     # This file
├── case-studies/
│   ├── spotify_analysis.md      # Music streaming product analysis
│   ├── linkedin_analysis.md     # Professional network analysis
│   └── experiment_designs.md    # Detailed experiment proposals
├── frameworks/
│   ├── kpi_framework.md         # KPI hierarchy template
│   ├── experiment_template.md   # A/B test design template
│   └── metrics_catalog.md       # Common metrics library
└── docs/
    ├── statistical_methods.md   # Statistical testing guide
    └── best_practices.md        # Experimentation guidelines
```

## 🚀 Getting Started

### Understanding the Framework

This project is primarily conceptual and analytical rather than code-heavy. The focus is on strategic thinking, metric design, and experimental rigor.

### Key Deliverables

1. **Product Analysis** - Deep dive into user experience
2. **KPI Framework** - Metrics hierarchy aligned with goals
3. **Experiment Designs** - 3+ testable hypotheses
4. **Expected Impacts** - Leading/lagging metric predictions

## 💡 Key Frameworks

### KPI Hierarchy Template

```
Business Objective: [e.g., Increase user engagement]
    |
    ├── North Star Metric: [e.g., Weekly Active Users]
    |
    ├── Leading Indicators (Predictive & Actionable)
    │   ├── Daily Active Users (DAU)
    │   ├── Session Frequency
    │   ├── Feature Adoption Rate
    │   └── Time to First Value
    |
    ├── Lagging Indicators (Outcome)
    │   ├── Monthly Retention Rate
    │   ├── Customer Lifetime Value (LTV)
    │   └── Revenue per User
    |
    └── Counter Metrics (Safety)
        ├── Bug Report Rate
        ├── Page Load Time
        └── Support Ticket Volume
```

### Experiment Design Template

```markdown
## Experiment: [Name]

### Hypothesis
[If we {change}, then {expected impact} because {reasoning}]

### Metrics
**Primary Success Metric**: [What you're optimizing for]
**Secondary Metrics**: [Supporting indicators]
**Counter Metrics**: [What might go wrong]

### Test Design
- **Control Group**: 50% - Current experience
- **Treatment A**: 25% - [Variation description]
- **Treatment B**: 25% - [Alternative variation]

### Expected Impacts
**Leading Metrics** (1-7 days):
- [Metric]: Expected [+/- X%] change
- [Metric]: Expected [+/- X%] change

**Lagging Metrics** (30+ days):
- [Metric]: Expected [+/- X%] change
- [Metric]: Expected [+/- X%] change

### Sample Size & Duration
- Minimum Detectable Effect (MDE): [X%]
- Required Sample Size: [N users per group]
- Estimated Duration: [X weeks]

### Segmentation Analysis
- [Segment 1]: Expected different behavior because...
- [Segment 2]: Expected different behavior because...
```

## 📊 Example Case Study: Music Streaming Product

### Product Journey Analysis

**Phase 1: Onboarding (Day 0-3)**
- Sign up flow: Email, social auth
- Music taste survey (5 genres, 10 artists)
- First playlist generation
- **Optimization Opportunity**: Reduce time to first song played

**Phase 2: Core Usage (Day 3-30)**
- Daily listening sessions
- Playlist discovery & creation
- Social sharing features
- **Optimization Opportunity**: Increase session frequency

**Phase 3: Retention (Day 30+)**
- Habit formation
- Premium conversion
- Feature depth usage
- **Optimization Opportunity**: Drive weekly recurring usage

### Experiment 1: Personalized Onboarding

**Hypothesis**:
If we reduce the onboarding survey from 15 questions to 5 questions and use ML to infer preferences, then users will reach their first song 2 minutes faster, leading to higher Day 1 retention.

**Test Design**:
- **Control (50%)**: Current 15-question survey
- **Treatment A (25%)**: 5-question survey + ML inference
- **Treatment B (25%)**: Skip survey, learn from behavior

**Metrics**:

| Type | Metric | Control Baseline | Treatment A Target | Treatment B Target |
|------|--------|------------------|-------------------|-------------------|
| Leading | Time to First Song | 8 min | 6 min (-25%) | 4 min (-50%) |
| Leading | Onboarding Completion | 75% | 85% (+13%) | 90% (+20%) |
| Leading | Songs Played Day 1 | 12 | 15 (+25%) | 18 (+50%) |
| Lagging | Day 1 Retention | 45% | 50% (+11%) | 52% (+16%) |
| Lagging | Day 7 Retention | 28% | 31% (+11%) | 30% (+7%) |
| Counter | Survey Accuracy | 85% | 75% (-12%) | 65% (-24%) |

**Expected Insights**:
- Treatment B may have highest Day 1 but lower Day 7 due to poor recommendations
- Treatment A balances quick start with sufficient preference data
- Power users may prefer detailed survey (segment analysis)

### Experiment 2: Social Proof in Discovery

**Hypothesis**:
If we show "X friends listened to this" on playlist recommendations, then users will explore 30% more playlists, increasing session length and engagement.

**Test Design**:
- **Control (50%)**: Standard playlist cards
- **Treatment (50%)**: Playlist cards with friend activity

**Metrics**:

| Type | Metric | Control Baseline | Treatment Target | Reasoning |
|------|--------|------------------|------------------|-----------|
| Leading | Playlists Explored | 3.2 per session | 4.2 (+31%) | Social proof increases curiosity |
| Leading | Playlist Play Rate | 18% | 24% (+33%) | Friend endorsement = trust |
| Leading | Session Length | 32 min | 38 min (+19%) | More exploration = more listening |
| Lagging | Weekly Sessions | 4.1 | 4.8 (+17%) | Better discovery = return visits |
| Lagging | Social Shares | 0.3 per week | 0.5 (+67%) | Seeing friends' activity prompts sharing |
| Counter | Privacy Concerns | 2% | 5% (+150%) | Some users uncomfortable with visibility |

**Segmentation Predictions**:
- **High social users**: +40% engagement (above avg)
- **Private users**: -10% engagement (below avg)
- **New users**: +50% (no baseline comparison)

### Experiment 3: Habit Formation Nudges

**Hypothesis**:
If we send personalized push notifications at users' optimal listening time (ML-predicted), then we'll increase DAU by 15% without increasing opt-out rates.

**Test Design**:
- **Control (50%)**: Generic evening notifications (6 PM)
- **Treatment A (25%)**: ML-predicted optimal time
- **Treatment B (25%)**: Adaptive time based on recent sessions

**Metrics**:

| Type | Metric | Control Baseline | Treatment A Target | Treatment B Target |
|------|--------|------------------|-------------------|-------------------|
| Leading | Push Open Rate | 12% | 18% (+50%) | 16% (+33%) |
| Leading | Session Starts from Push | 8% | 13% (+63%) | 11% (+38%) |
| Leading | DAU | 42% | 48% (+14%) | 46% (+10%) |
| Lagging | Weekly Retention | 65% | 70% (+8%) | 68% (+5%) |
| Lagging | 30-Day Retention | 38% | 42% (+11%) | 40% (+5%) |
| Counter | Notification Opt-Out | 5% | 6% (+20%) | 5.5% (+10%) |

## 🎓 Key Learning Areas

### Metric Selection Criteria

**SMART Metrics**:
- **Specific**: Clearly defined, no ambiguity
- **Measurable**: Quantifiable with existing data
- **Actionable**: Team can influence through product changes
- **Relevant**: Tied to business objectives
- **Timely**: Updates frequently enough to inform decisions

**Common Metric Pitfalls**:
❌ Vanity metrics (downloads, page views without context)  
❌ Trailing indicators only (can't course-correct)  
❌ Too many metrics (analysis paralysis)  
❌ Metrics without context (no segments, no time series)  
❌ Ignoring counter metrics (optimizing one thing breaks another)  

### Experiment Design Best Practices

1. **Randomization**: Ensure truly random assignment to avoid bias
2. **Sample Size**: Calculate statistical power before launching
3. **Duration**: Run long enough to measure lagging indicators
4. **Novelty Effects**: Account for short-term excitement
5. **Network Effects**: Be careful with social features (spillover)
6. **Multiple Testing**: Adjust p-values when running many tests

### Statistical Considerations

**Minimum Detectable Effect (MDE)**:
```
MDE = (Z_alpha + Z_beta) * sqrt(2 * variance / sample_size)

Where:
- Z_alpha: Significance level (typically 1.96 for 95% confidence)
- Z_beta: Statistical power (typically 0.84 for 80% power)
- variance: Metric variance in control group
- sample_size: Users per test cell
```

**Sample Size Calculation**:
```python
import scipy.stats as stats

def calculate_sample_size(baseline_rate, mde, alpha=0.05, power=0.8):
    """
    Calculate required sample size per group
    
    Args:
        baseline_rate: Control group conversion rate (e.g., 0.10 for 10%)
        mde: Minimum detectable effect (e.g., 0.02 for 2 percentage points)
        alpha: Significance level (Type I error)
        power: Statistical power (1 - Type II error)
    
    Returns:
        Required sample size per group
    """
    effect_size = mde / baseline_rate  # Relative lift
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    
    variance = baseline_rate * (1 - baseline_rate)
    n = ((z_alpha + z_beta) ** 2 * 2 * variance) / (mde ** 2)
    
    return int(n) + 1

# Example: Improve 10% conversion by 2 percentage points
sample_size = calculate_sample_size(
    baseline_rate=0.10,
    mde=0.02,  # 2 percentage points
    alpha=0.05,
    power=0.8
)
print(f"Required sample size per group: {sample_size:,}")
# Output: Required sample size per group: 3,841
```

## 🔍 Real-World Applications

### Product Areas for Experimentation

**Onboarding**:
- Sign-up flow optimization
- Initial value demonstration
- Feature education
- Habit formation

**Engagement**:
- Feature discovery
- Content recommendation
- Notification strategies
- Social proof

**Monetization**:
- Pricing strategies
- Premium feature gating
- Upsell timing
- Payment flow optimization

**Retention**:
- Re-engagement campaigns
- Churn prediction & prevention
- Loyalty programs
- Community building

## 📈 Industry Examples

### Company KPI Frameworks

**Spotify**:
- North Star: Time Spent Listening (TSL)
- Leading: DAU, Session Frequency, Discovery Rate
- Lagging: Retention, Premium Conversion, LTV

**LinkedIn**:
- North Star: Weekly Active Users (WAU)
- Leading: Connections Made, Content Shares, Profile Views
- Lagging: Member Retention, Job Applications, Revenue per User

**Airbnb**:
- North Star: Nights Booked
- Leading: Search to Book Rate, Host Response Time, Review Rate
- Lagging: Guest Retention, Host Retention, GMV

## 🔗 Related Projects

- [Analytical Patterns](../05-analytical-patterns/) - Calculate these metrics at scale
- [Fact Modeling](../02-fact-modeling/) - Store experiment results
- [Spark Pipelines](../03-spark-pipelines/) - Process large experiment datasets

## 📚 Resources

- [Trustworthy Online Controlled Experiments](https://experimentguide.com/) - The A/B Testing Bible
- [Evan Miller's A/B Tools](https://www.evanmiller.org/ab-testing/) - Statistical calculators
- [Amplitude Experimentation](https://amplitude.com/amplitude-experiment) - Modern experimentation platform
- [Optimizely Knowledge Base](https://support.optimizely.com/) - Experiment design patterns

---

**Key Takeaway**: Great data engineering enables great experimentation. The faster you can measure, the faster you can learn and improve.


