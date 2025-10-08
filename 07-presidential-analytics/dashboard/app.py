"""
Presidential Analytics Dashboard
Interactive Streamlit dashboard for analyzing economic performance by president
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

# Page configuration
st.set_page_config(
    page_title="Presidential Economic Performance",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("📊 Presidential Economic Performance Dashboard")
st.markdown("*Analyzing US Economic Metrics Across Presidential Administrations (1945-Present)*")

# Sidebar
st.sidebar.header("Filters")

# Load data (in production, this would connect to Snowflake)
@st.cache_data
def load_sample_data():
    """Load sample data for demonstration"""
    # This is sample data - in production, query Snowflake
    presidents = [
        {"id": 40, "name": "Ronald Reagan", "party": "Republican", "start": "1981-01-20", "end": "1989-01-20"},
        {"id": 41, "name": "George H. W. Bush", "party": "Republican", "start": "1989-01-20", "end": "1993-01-20"},
        {"id": 42, "name": "Bill Clinton", "party": "Democratic", "start": "1993-01-20", "end": "2001-01-20"},
        {"id": 43, "name": "George W. Bush", "party": "Republican", "start": "2001-01-20", "end": "2009-01-20"},
        {"id": 44, "name": "Barack Obama", "party": "Democratic", "start": "2009-01-20", "end": "2017-01-20"},
        {"id": 45, "name": "Donald Trump", "party": "Republican", "start": "2017-01-20", "end": "2021-01-20"},
        {"id": 46, "name": "Joe Biden", "party": "Democratic", "start": "2021-01-20", "end": None},
    ]
    
    # Generate sample economic data
    import numpy as np
    np.random.seed(42)
    
    economic_data = []
    for pres in presidents:
        start_date = pd.to_datetime(pres['start'])
        end_date = pd.to_datetime(pres['end']) if pres['end'] else pd.Timestamp.now()
        dates = pd.date_range(start=start_date, end=end_date, freq='M')
        
        for date in dates:
            economic_data.append({
                'date': date,
                'president': pres['name'],
                'party': pres['party'],
                'GDP_Growth': np.random.normal(2.5, 1.5),
                'Unemployment': np.random.normal(5.5, 2),
                'Inflation': np.random.normal(2.0, 1),
                'SP500_Change': np.random.normal(8, 10),
            })
    
    return pd.DataFrame(presidents), pd.DataFrame(economic_data)

presidents_df, economic_df = load_sample_data()

# Sidebar filters
selected_parties = st.sidebar.multiselect(
    "Select Parties",
    options=presidents_df['party'].unique(),
    default=presidents_df['party'].unique()
)

selected_presidents = st.sidebar.multiselect(
    "Select Presidents",
    options=presidents_df[presidents_df['party'].isin(selected_parties)]['name'].unique(),
    default=presidents_df[presidents_df['party'].isin(selected_parties)]['name'].head(3).tolist()
)

selected_metrics = st.sidebar.multiselect(
    "Select Economic Metrics",
    options=['GDP_Growth', 'Unemployment', 'Inflation', 'SP500_Change'],
    default=['GDP_Growth', 'Unemployment']
)

# Filter data
filtered_df = economic_df[
    (economic_df['president'].isin(selected_presidents)) &
    (economic_df['party'].isin(selected_parties))
]

# Main dashboard layout
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Presidents Selected",
        len(selected_presidents),
        f"{len(selected_presidents)} of {len(presidents_df)}"
    )

with col2:
    avg_gdp = filtered_df['GDP_Growth'].mean()
    st.metric(
        "Avg GDP Growth",
        f"{avg_gdp:.2f}%",
        f"±{filtered_df['GDP_Growth'].std():.2f}"
    )

with col3:
    avg_unemployment = filtered_df['Unemployment'].mean()
    st.metric(
        "Avg Unemployment",
        f"{avg_unemployment:.2f}%",
        f"±{filtered_df['Unemployment'].std():.2f}"
    )

with col4:
    avg_inflation = filtered_df['Inflation'].mean()
    st.metric(
        "Avg Inflation",
        f"{avg_inflation:.2f}%",
        f"±{filtered_df['Inflation'].std():.2f}"
    )

st.markdown("---")

# Time Series Charts
st.subheader("📈 Economic Indicators Over Time")

tabs = st.tabs(selected_metrics if selected_metrics else ['No metrics selected'])

for idx, metric in enumerate(selected_metrics):
    with tabs[idx]:
        fig = go.Figure()
        
        for president in selected_presidents:
            pres_data = filtered_df[filtered_df['president'] == president]
            party = pres_data['party'].iloc[0]
            color = '#0015BC' if party == 'Democratic' else '#E81B23'
            
            fig.add_trace(go.Scatter(
                x=pres_data['date'],
                y=pres_data[metric],
                name=president,
                line=dict(color=color, width=2),
                mode='lines'
            ))
        
        fig.update_layout(
            title=f"{metric.replace('_', ' ')} by Presidential Administration",
            xaxis_title="Date",
            yaxis_title=metric.replace('_', ' '),
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Comparison Section
st.subheader("🔍 Presidential Comparison")

col1, col2 = st.columns(2)

with col1:
    # Average metrics by president
    avg_by_president = filtered_df.groupby('president')[selected_metrics].mean().reset_index()
    
    fig_bar = px.bar(
        avg_by_president,
        x='president',
        y=selected_metrics,
        title="Average Economic Metrics by President",
        barmode='group',
        height=400
    )
    fig_bar.update_xaxis(tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    # Party comparison
    avg_by_party = filtered_df.groupby('party')[selected_metrics].mean().reset_index()
    
    fig_party = px.bar(
        avg_by_party,
        x='party',
        y=selected_metrics,
        title="Average Economic Metrics by Party",
        barmode='group',
        color='party',
        color_discrete_map={'Democratic': '#0015BC', 'Republican': '#E81B23'},
        height=400
    )
    st.plotly_chart(fig_party, use_container_width=True)

st.markdown("---")

# Data Table
st.subheader("📋 Detailed Data")

# Summary statistics
summary_df = filtered_df.groupby(['president', 'party'])[selected_metrics].agg(['mean', 'std', 'min', 'max']).round(2)
st.dataframe(summary_df, use_container_width=True)

# Raw data (optional)
with st.expander("View Raw Data"):
    st.dataframe(filtered_df[['date', 'president', 'party'] + selected_metrics], use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
**Data Sources:**
- Economic Data: Federal Reserve Economic Data (FRED)
- Presidential Data: Historical Records

**Pipeline:** API → S3 → Snowflake → Dashboard

*Part of the Data Engineering Portfolio - Presidential Analytics Project*
""")

# Instructions for connecting to Snowflake (commented out for demo)
"""
# To connect to Snowflake, uncomment and configure:

from snowflake.connector import connect
import snowflake.connector

@st.cache_resource
def get_snowflake_connection():
    return snowflake.connector.connect(
        user='YOUR_USER',
        password='YOUR_PASSWORD',
        account='YOUR_ACCOUNT',
        warehouse='YOUR_WAREHOUSE',
        database='PRESIDENTIAL_ANALYTICS',
        schema='PUBLIC'
    )

@st.cache_data(ttl=600)  # Cache for 10 minutes
def load_data_from_snowflake():
    conn = get_snowflake_connection()
    
    # Load presidents
    presidents_query = "SELECT * FROM presidents_dim WHERE is_active = TRUE"
    presidents_df = pd.read_sql(presidents_query, conn)
    
    # Load economic facts
    economic_query = "SELECT * FROM economic_facts ORDER BY observation_date"
    economic_df = pd.read_sql(economic_query, conn)
    
    return presidents_df, economic_df
"""

