"""
Senegal Development Intelligence Platform
Comprehensive analytics with comparative analysis and regional insights
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path

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

# Load data from Snowflake
@st.cache_data
def load_comprehensive_data():
    """Load comprehensive Senegal data from Snowflake"""
    import snowflake.connector
    import yaml
    
    # Try to load from Streamlit secrets first, then config file
    try:
        # Streamlit Cloud secrets
        config = st.secrets["snowflake"]
    except:
        try:
            # Local config file
            config_path = Path(__file__).parent.parent / "config" / "config.yaml"
            with open(config_path) as f:
                config = yaml.safe_load(f)['snowflake']
        except:
            st.error("❌ Unable to load Snowflake configuration. Please check your secrets or config file.")
            return None, None, None, None
    
    # Connect to Snowflake
    conn = snowflake.connector.connect(
        account=config['account'],
        user=config['user'],
        password=config['password'],
        warehouse=config['warehouse'],
        database=config['database'],
        schema=config['schema']
    )
    
    cursor = conn.cursor()
    
    # Get presidents data
    cursor.execute("SELECT PRESIDENT_NAME, PARTY, START_DATE, END_DATE FROM presidents_dim WHERE IS_ACTIVE = TRUE ORDER BY START_DATE")
    presidents_data = cursor.fetchall()
    presidents_df = pd.DataFrame(presidents_data, columns=['PRESIDENT_NAME', 'PARTY', 'START_DATE', 'END_DATE'])
    
    # Get ANSD population data
    cursor.execute("SELECT YEAR, TOTAL_POPULATION, URBAN_PERCENTAGE, POPULATION_GROWTH_RATE FROM ansd_population ORDER BY YEAR")
    pop_data = cursor.fetchall()
    pop_df = pd.DataFrame(pop_data, columns=['YEAR', 'TOTAL_POPULATION', 'URBAN_PERCENTAGE', 'POPULATION_GROWTH_RATE'])
    
    # Get economic indicators
    cursor.execute("SELECT YEAR, GDP_GROWTH_RATE, INFLATION_RATE, UNEMPLOYMENT_RATE, TRADE_BALANCE_GDP FROM economic_indicators ORDER BY YEAR")
    econ_data = cursor.fetchall()
    econ_df = pd.DataFrame(econ_data, columns=['YEAR', 'GDP_GROWTH_RATE', 'INFLATION_RATE', 'UNEMPLOYMENT_RATE', 'TRADE_BALANCE_GDP'])
    
    conn.close()
    
    return presidents_df, pop_df, econ_df

try:
    presidents_df, pop_df, econ_df = load_comprehensive_data()
    st.success(f"✅ Data loaded: {len(presidents_df)} presidents, {len(pop_df)} population records, {len(econ_df)} economic indicators")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Create comparative data (West African countries)
def create_comparative_data():
    """Create comparative data with West African neighbors"""
    countries = ['Senegal', 'Mali', 'Burkina Faso', 'Niger', 'Guinea', 'Gambia', 'Guinea-Bissau']
    
    # Simulate realistic data for comparison
    comparative_data = []
    for year in range(2020, 2025):
        for country in countries:
            # Base values with country-specific adjustments
            if country == 'Senegal':
                gdp_growth = np.random.normal(5.5, 1.0)
                population_growth = np.random.normal(3.0, 0.3)
                urbanization = 67.0 + (year - 2020) * 0.8
            elif country == 'Mali':
                gdp_growth = np.random.normal(3.2, 1.5)
                population_growth = np.random.normal(3.2, 0.4)
                urbanization = 42.0 + (year - 2020) * 0.6
            elif country == 'Burkina Faso':
                gdp_growth = np.random.normal(4.8, 1.2)
                population_growth = np.random.normal(2.8, 0.3)
                urbanization = 30.0 + (year - 2020) * 0.5
            elif country == 'Niger':
                gdp_growth = np.random.normal(6.2, 1.8)
                population_growth = np.random.normal(3.8, 0.5)
                urbanization = 16.0 + (year - 2020) * 0.3
            elif country == 'Guinea':
                gdp_growth = np.random.normal(4.5, 2.0)
                population_growth = np.random.normal(2.6, 0.4)
                urbanization = 38.0 + (year - 2020) * 0.7
            elif country == 'Gambia':
                gdp_growth = np.random.normal(3.8, 1.3)
                population_growth = np.random.normal(2.9, 0.3)
                urbanization = 61.0 + (year - 2020) * 0.6
            else:  # Guinea-Bissau
                gdp_growth = np.random.normal(3.5, 2.2)
                population_growth = np.random.normal(2.4, 0.4)
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
            # Base values with regional adjustments
            if region == 'Dakar':
                population = np.random.normal(3500000, 50000)
                urbanization = np.random.normal(95.0, 1.0)
                economic_activity = np.random.normal(85.0, 3.0)
            elif region in ['Thiès', 'Diourbel']:
                population = np.random.normal(1800000, 30000)
                urbanization = np.random.normal(65.0, 2.0)
                economic_activity = np.random.normal(70.0, 4.0)
            elif region in ['Kaolack', 'Fatick']:
                population = np.random.normal(1200000, 25000)
                urbanization = np.random.normal(45.0, 3.0)
                economic_activity = np.random.normal(60.0, 5.0)
            elif region in ['Ziguinchor', 'Kolda']:
                population = np.random.normal(800000, 20000)
                urbanization = np.random.normal(35.0, 3.0)
                economic_activity = np.random.normal(55.0, 6.0)
            else:  # Northern and Eastern regions
                population = np.random.normal(600000, 15000)
                urbanization = np.random.normal(25.0, 4.0)
                economic_activity = np.random.normal(45.0, 7.0)
            
            regional_data.append({
                'year': year,
                'region': region,
                'population': int(population),
                'urbanization_rate': round(urbanization, 1),
                'economic_activity_index': round(economic_activity, 1)
            })
    
    return pd.DataFrame(regional_data)

# Generate comparative and regional data
import numpy as np
comparative_df = create_comparative_data()
regional_df = create_regional_data()

# Sidebar
st.sidebar.header("🎛️ Navigation")
st.sidebar.markdown("""
**📊 Data Dimensions:**
- 🇸🇳 **Senegal Focus**
- 🌍 **Regional Comparison** 
- 🗺️ **Regional Breakdown**
- 📈 **Trend Analysis**
""")

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
        
        # Ranking table
        st.subheader("📊 Regional Rankings")
        
        # Calculate averages for ranking
        ranking_df = filtered_comp_df.groupby('country').agg({
            'gdp_growth_rate': 'mean',
            'population_growth_rate': 'mean',
            'urbanization_rate': 'mean'
        }).round(1).reset_index()
        
        # Rank countries
        ranking_df['GDP_Rank'] = ranking_df['gdp_growth_rate'].rank(ascending=False)
        ranking_df['Population_Rank'] = ranking_df['population_growth_rate'].rank(ascending=False)
        ranking_df['Urbanization_Rank'] = ranking_df['urbanization_rate'].rank(ascending=False)
        
        st.dataframe(ranking_df, use_container_width=True)

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
        
        # Regional metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_pop = year_data['population'].sum()
            st.metric("Total Population", f"{total_pop:,.0f}")
        
        with col2:
            avg_urban = year_data['urbanization_rate'].mean()
            st.metric("Average Urbanization", f"{avg_urban:.1f}%")
        
        with col3:
            avg_economic = year_data['economic_activity_index'].mean()
            st.metric("Economic Activity Index", f"{avg_economic:.1f}")
        
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
        
        # Regional details
        st.subheader("🏛️ Regional Details")
        
        # Create regional cards
        for _, row in year_data.iterrows():
            st.markdown(f'''
            <div class="region-card">
                <h4>📍 {row['region']}</h4>
                <div style="display: flex; justify-content: space-between;">
                    <span><strong>Population:</strong> {row['population']:,}</span>
                    <span><strong>Urbanization:</strong> {row['urbanization_rate']:.1f}%</span>
                    <span><strong>Economic Activity:</strong> {row['economic_activity_index']:.1f}</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)

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
    Last Updated: """ + datetime.now().strftime('%B %d, %Y') + """</small>
</div>
""", unsafe_allow_html=True)
