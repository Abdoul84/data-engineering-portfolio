"""
Senegal Development Intelligence Platform - Demo Version
Works without Snowflake connection for demo purposes
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page configuration - Mobile responsive
st.set_page_config(
    page_title="Senegal Development Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for mobile responsiveness
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(90deg, #f8f9fa, #e9ecef);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2E8B57;
        margin: 0.5rem 0;
    }
    .region-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
    }
    @media (max-width: 768px) {
        .main-header { font-size: 2rem; }
        .subtitle { font-size: 1rem; }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🌍 Senegal Development Intelligence Platform</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Comprehensive Analytics • Comparative Analysis • Regional Insights</p>', unsafe_allow_html=True)

# Create demo data
def create_demo_data():
    """Create comprehensive demo data for Senegal"""
    
    # Presidents data
    presidents_data = [
        {'PRESIDENT_NAME': 'Léopold Sédar Senghor', 'PARTY': 'Union Progressiste Sénégalaise (UPS)', 'START_DATE': '1960-09-05', 'END_DATE': '1980-12-31'},
        {'PRESIDENT_NAME': 'Abdou Diouf', 'PARTY': 'Parti Socialiste (PS)', 'START_DATE': '1981-01-01', 'END_DATE': '2000-04-01'},
        {'PRESIDENT_NAME': 'Abdoulaye Wade', 'PARTY': 'Parti Démocratique Sénégalais (PDS)', 'START_DATE': '2001-04-01', 'END_DATE': '2012-04-02'},
        {'PRESIDENT_NAME': 'Macky Sall', 'PARTY': 'Alliance pour la République (APR)', 'START_DATE': '2013-04-02', 'END_DATE': '2024-04-02'},
        {'PRESIDENT_NAME': 'Bassirou Diomaye Faye', 'PARTY': 'Pastef', 'START_DATE': '2024-04-02', 'END_DATE': None}
    ]
    presidents_df = pd.DataFrame(presidents_data)
    
    # Population data (1960-2024)
    years = list(range(1960, 2025))
    population_data = []
    base_pop = 3340000
    
    for i, year in enumerate(years):
        growth_rate = 3.0 + np.random.normal(0, 0.5)
        if year == 1960:
            pop = base_pop
        else:
            pop = population_data[-1]['TOTAL_POPULATION'] * (1 + growth_rate/100)
        
        urban_pct = min(23.0 + (year - 1960) * 0.8, 68.0)
        
        population_data.append({
            'YEAR': year,
            'TOTAL_POPULATION': int(pop),
            'URBAN_PERCENTAGE': round(urban_pct, 1),
            'POPULATION_GROWTH_RATE': round(growth_rate, 1)
        })
    
    pop_df = pd.DataFrame(population_data)
    
    # Economic data
    economic_data = []
    for year in years:
        if year <= 1980:
            gdp_growth = 3.5 + np.random.normal(0, 1.5)
            inflation = 8.0 + np.random.normal(0, 2.0)
        elif year <= 2000:
            gdp_growth = 3.2 + np.random.normal(0, 2.0)
            inflation = 12.0 + np.random.normal(0, 3.0)
        elif year <= 2012:
            gdp_growth = 4.5 + np.random.normal(0, 1.8)
            inflation = 6.0 + np.random.normal(0, 2.0)
        else:
            gdp_growth = 5.5 + np.random.normal(0, 1.2)
            inflation = 4.0 + np.random.normal(0, 1.5)
        
        economic_data.append({
            'YEAR': year,
            'GDP_GROWTH_RATE': round(gdp_growth, 1),
            'INFLATION_RATE': round(inflation, 1),
            'UNEMPLOYMENT_RATE': round(15.0 - (year - 1960) * 0.1, 1),
            'TRADE_BALANCE_GDP': round(-8.0 + np.random.normal(0, 2.0), 1)
        })
    
    econ_df = pd.DataFrame(economic_data)
    
    return presidents_df, pop_df, econ_df

# Load demo data
presidents_df, pop_df, econ_df = create_demo_data()

st.success(f"✅ Demo Data Loaded: {len(presidents_df)} presidents, {len(pop_df)} population records, {len(econ_df)} economic indicators")

# Sidebar
st.sidebar.header("🎛️ Navigation")
st.sidebar.markdown("""
**📊 Data Dimensions:**
- 🇸🇳 **Senegal Focus**
- 🌍 **Regional Comparison** 
- 🗺️ **Regional Breakdown**
- 📈 **Trend Analysis**

**📝 Note:** This is a demo version with simulated data
""")

# Create comparative data (West African countries)
def create_comparative_data():
    """Create comparative data with West African neighbors"""
    countries = ['Senegal', 'Mali', 'Burkina Faso', 'Niger', 'Guinea', 'Gambia', 'Guinea-Bissau']
    
    comparative_data = []
    for year in range(2020, 2025):
        for country in countries:
            if country == 'Senegal':
                gdp_growth = 5.5 + np.random.normal(0, 1.0)
                population_growth = 3.0 + np.random.normal(0, 0.3)
                urbanization = 67.0 + (year - 2020) * 0.8
            elif country == 'Mali':
                gdp_growth = 3.2 + np.random.normal(0, 1.5)
                population_growth = 3.2 + np.random.normal(0, 0.4)
                urbanization = 42.0 + (year - 2020) * 0.6
            elif country == 'Burkina Faso':
                gdp_growth = 4.8 + np.random.normal(0, 1.2)
                population_growth = 2.8 + np.random.normal(0, 0.3)
                urbanization = 30.0 + (year - 2020) * 0.5
            elif country == 'Niger':
                gdp_growth = 6.2 + np.random.normal(0, 1.8)
                population_growth = 3.8 + np.random.normal(0, 0.5)
                urbanization = 16.0 + (year - 2020) * 0.3
            elif country == 'Guinea':
                gdp_growth = 4.5 + np.random.normal(0, 2.0)
                population_growth = 2.6 + np.random.normal(0, 0.4)
                urbanization = 38.0 + (year - 2020) * 0.7
            elif country == 'Gambia':
                gdp_growth = 3.8 + np.random.normal(0, 1.3)
                population_growth = 2.9 + np.random.normal(0, 0.3)
                urbanization = 61.0 + (year - 2020) * 0.6
            else:  # Guinea-Bissau
                gdp_growth = 3.5 + np.random.normal(0, 2.2)
                population_growth = 2.4 + np.random.normal(0, 0.4)
                urbanization = 45.0 + (year - 2020) * 0.5
            
            comparative_data.append({
                'year': year,
                'country': country,
                'gdp_growth_rate': round(gdp_growth, 1),
                'population_growth_rate': round(population_growth, 1),
                'urbanization_rate': round(urbanization, 1)
            })
    
    return pd.DataFrame(comparative_data)

# Create regional data within Senegal
def create_regional_data():
    """Create regional breakdown data for Senegal"""
    regions = [
        'Dakar', 'Thiès', 'Diourbel', 'Fatick', 'Kaolack', 'Kolda',
        'Ziguinchor', 'Tambacounda', 'Matam', 'Saint-Louis', 'Louga'
    ]
    
    regional_data = []
    for year in range(2020, 2025):
        for region in regions:
            if region == 'Dakar':
                population = 3500000 + np.random.normal(0, 50000)
                urbanization = 95.0 + np.random.normal(0, 1.0)
                economic_activity = 85.0 + np.random.normal(0, 3.0)
            elif region in ['Thiès', 'Diourbel']:
                population = 1800000 + np.random.normal(0, 30000)
                urbanization = 65.0 + np.random.normal(0, 2.0)
                economic_activity = 70.0 + np.random.normal(0, 4.0)
            elif region in ['Kaolack', 'Fatick']:
                population = 1200000 + np.random.normal(0, 25000)
                urbanization = 45.0 + np.random.normal(0, 3.0)
                economic_activity = 60.0 + np.random.normal(0, 5.0)
            elif region in ['Ziguinchor', 'Kolda']:
                population = 800000 + np.random.normal(0, 20000)
                urbanization = 35.0 + np.random.normal(0, 3.0)
                economic_activity = 55.0 + np.random.normal(0, 6.0)
            else:  # Northern and Eastern regions
                population = 600000 + np.random.normal(0, 15000)
                urbanization = 25.0 + np.random.normal(0, 4.0)
                economic_activity = 45.0 + np.random.normal(0, 7.0)
            
            regional_data.append({
                'year': year,
                'region': region,
                'population': int(population),
                'urbanization_rate': round(urbanization, 1),
                'economic_activity_index': round(economic_activity, 1)
            })
    
    return pd.DataFrame(regional_data)

# Generate comparative and regional data
comparative_df = create_comparative_data()
regional_df = create_regional_data()

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["🇸🇳 Senegal Focus", "🌍 Regional Comparison", "🗺️ Regional Breakdown", "📈 Trend Analysis"])

with tab1:
    st.header("🇸🇳 Senegal Development Overview")
    
    # Key metrics in responsive cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        latest_pop = pop_df[pop_df['YEAR'] == pop_df['YEAR'].max()]['TOTAL_POPULATION'].iloc[0]
        st.markdown(f'''
        <div class="metric-card">
            <h4>📊 Total Population</h4>
            <h2>{latest_pop:,.0f}</h2>
            <p>2024 Estimate</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        latest_urban = pop_df[pop_df['YEAR'] == pop_df['YEAR'].max()]['URBAN_PERCENTAGE'].iloc[0]
        st.markdown(f'''
        <div class="metric-card">
            <h4>🏙️ Urbanization</h4>
            <h2>{latest_urban:.1f}%</h2>
            <p>Urban Population</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        avg_gdp_growth = econ_df['GDP_GROWTH_RATE'].mean()
        st.markdown(f'''
        <div class="metric-card">
            <h4>💰 GDP Growth</h4>
            <h2>{avg_gdp_growth:.1f}%</h2>
            <p>Average Annual</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        latest_inflation = econ_df[econ_df['YEAR'] == econ_df['YEAR'].max()]['INFLATION_RATE'].iloc[0]
        st.markdown(f'''
        <div class="metric-card">
            <h4>📈 Inflation</h4>
            <h2>{latest_inflation:.1f}%</h2>
            <p>Current Rate</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pop = px.line(
            pop_df,
            x='YEAR',
            y='TOTAL_POPULATION',
            title="Population Growth (1960-2024)",
            labels={'TOTAL_POPULATION': 'Population', 'YEAR': 'Year'}
        )
        fig_pop.update_traces(line=dict(width=4, color='#2E8B57'))
        st.plotly_chart(fig_pop, use_container_width=True)
    
    with col2:
        fig_gdp = px.line(
            econ_df,
            x='YEAR',
            y='GDP_GROWTH_RATE',
            title="GDP Growth Rate Over Time",
            labels={'GDP_GROWTH_RATE': 'GDP Growth (%)', 'YEAR': 'Year'}
        )
        fig_gdp.update_traces(line=dict(width=4, color='#FF6B6B'))
        st.plotly_chart(fig_gdp, use_container_width=True)

with tab2:
    st.header("🌍 West African Regional Comparison")
    
    # Country selector
    selected_countries = st.multiselect(
        "Select Countries to Compare",
        options=comparative_df['country'].unique(),
        default=['Senegal', 'Mali', 'Burkina Faso', 'Niger']
    )
    
    if selected_countries:
        filtered_comp_df = comparative_df[comparative_df['country'].isin(selected_countries)]
        
        # Comparison charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig_gdp_comp = px.bar(
                filtered_comp_df,
                x='country',
                y='gdp_growth_rate',
                title="GDP Growth Rate Comparison (2020-2024)",
                labels={'gdp_growth_rate': 'GDP Growth (%)', 'country': 'Country'},
                color='country',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_gdp_comp, use_container_width=True)
        
        with col2:
            fig_urban_comp = px.bar(
                filtered_comp_df,
                x='country',
                y='urbanization_rate',
                title="Urbanization Rate Comparison",
                labels={'urbanization_rate': 'Urbanization (%)', 'country': 'Country'},
                color='country',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_urban_comp, use_container_width=True)

with tab3:
    st.header("🗺️ Regional Breakdown Within Senegal")
    
    # Year selector
    selected_year = st.selectbox(
        "Select Year",
        options=sorted(regional_df['year'].unique()),
        index=len(regional_df['year'].unique())-1
    )
    
    if selected_year:
        year_data = regional_df[regional_df['year'] == selected_year]
        
        # Regional charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pop_reg = px.bar(
                year_data,
                x='region',
                y='population',
                title=f"Population by Region ({selected_year})",
                labels={'population': 'Population', 'region': 'Region'},
                color='population',
                color_continuous_scale='Viridis'
            )
            fig_pop_reg.update_xaxes(tickangle=45)
            st.plotly_chart(fig_pop_reg, use_container_width=True)
        
        with col2:
            fig_urban_reg = px.bar(
                year_data,
                x='region',
                y='urbanization_rate',
                title=f"Urbanization by Region ({selected_year})",
                labels={'urbanization_rate': 'Urbanization (%)', 'region': 'Region'},
                color='urbanization_rate',
                color_continuous_scale='Blues'
            )
            fig_urban_reg.update_xaxes(tickangle=45)
            st.plotly_chart(fig_urban_reg, use_container_width=True)

with tab4:
    st.header("📈 Trend Analysis & Forecasting")
    
    # Trend analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Population trend with projection
        fig_pop_trend = go.Figure()
        
        fig_pop_trend.add_trace(go.Scatter(
            x=pop_df['YEAR'],
            y=pop_df['TOTAL_POPULATION'],
            mode='lines+markers',
            name='Historical',
            line=dict(color='#2E8B57', width=3)
        ))
        
        # Simple projection (linear trend)
        last_year = pop_df['YEAR'].max()
        last_pop = pop_df[pop_df['YEAR'] == last_year]['TOTAL_POPULATION'].iloc[0]
        
        # Project next 10 years
        future_years = list(range(last_year + 1, last_year + 11))
        avg_growth = pop_df['POPULATION_GROWTH_RATE'].tail(5).mean()
        projected_pop = [last_pop * (1 + avg_growth/100) ** (year - last_year) for year in future_years]
        
        fig_pop_trend.add_trace(go.Scatter(
            x=future_years,
            y=projected_pop,
            mode='lines',
            name='Projected',
            line=dict(color='#FF6B6B', width=2, dash='dash')
        ))
        
        fig_pop_trend.update_layout(
            title="Population Trend & Projection",
            xaxis_title="Year",
            yaxis_title="Population"
        )
        
        st.plotly_chart(fig_pop_trend, use_container_width=True)
    
    with col2:
        # Economic trend
        fig_econ_trend = px.line(
            econ_df,
            x='YEAR',
            y=['GDP_GROWTH_RATE', 'INFLATION_RATE'],
            title="Economic Indicators Trend",
            labels={'value': 'Rate (%)', 'YEAR': 'Year'},
            color_discrete_sequence=['#2E8B57', '#FF6B6B']
        )
        st.plotly_chart(fig_econ_trend, use_container_width=True)
    
    # Key insights
    st.subheader("🎯 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📈 Population Trends:**
        - Steady growth: 3.0% annually
        - Rapid urbanization: 68% by 2024
        - Projected to reach 25M by 2035
        
        **💰 Economic Performance:**
        - Strong GDP growth under current leadership
        - Stable inflation management
        - Improving trade balance
        """)
    
    with col2:
        st.markdown("""
        **🌍 Regional Position:**
        - Leading urbanization in West Africa
        - Strong economic growth vs neighbors
        - Political stability advantage
        
        **🗺️ Internal Dynamics:**
        - Dakar dominates economically
        - Rural-urban development gap
        - Infrastructure needs in regions
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <strong>🌍 Senegal Development Intelligence Platform</strong><br>
    <small>Comprehensive Analytics • Comparative Analysis • Regional Insights<br>
    Demo Version with Simulated Data<br>
    Last Updated: """ + datetime.now().strftime('%B %d, %Y') + """</small>
</div>
""", unsafe_allow_html=True)

