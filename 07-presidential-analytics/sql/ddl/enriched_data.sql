-- ====================================================================
-- Enriched Data Tables for Senegal Presidential Analytics
-- Comprehensive indicators across multiple dimensions
-- ====================================================================

USE DATABASE SENEGAL_ANALYTICS;
USE SCHEMA PUBLIC;

-- Economic Indicators Table
CREATE TABLE IF NOT EXISTS economic_indicators (
    economic_key INT AUTOINCREMENT PRIMARY KEY,
    year INT NOT NULL,
    gdp_growth_rate DECIMAL(5, 2),
    inflation_rate DECIMAL(5, 2),
    unemployment_rate DECIMAL(5, 2),
    exports_gdp_percent DECIMAL(5, 2),
    imports_gdp_percent DECIMAL(5, 2),
    trade_balance_gdp DECIMAL(5, 2),
    fdi_gdp_percent DECIMAL(5, 2),
    external_debt_gdp_percent DECIMAL(5, 2),
    
    -- Country metadata
    country VARCHAR(100) DEFAULT 'Senegal',
    country_code VARCHAR(10) DEFAULT 'SN',
    
    -- Data source
    data_source VARCHAR(100) DEFAULT 'Enhanced Economic Indicators',
    
    -- Audit fields
    ingestion_timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Climate and Environmental Indicators Table
CREATE TABLE IF NOT EXISTS climate_environmental (
    climate_key INT AUTOINCREMENT PRIMARY KEY,
    year INT NOT NULL,
    average_temperature DECIMAL(4, 1),
    annual_rainfall_mm DECIMAL(8, 0),
    forest_coverage_percent DECIMAL(5, 1),
    co2_emissions_per_capita DECIMAL(6, 2),
    agricultural_gdp_percent DECIMAL(5, 1),
    food_security_index DECIMAL(5, 1),
    
    -- Country metadata
    country VARCHAR(100) DEFAULT 'Senegal',
    country_code VARCHAR(10) DEFAULT 'SN',
    
    -- Data source
    data_source VARCHAR(100) DEFAULT 'Climate & Environmental Indicators',
    
    -- Audit fields
    ingestion_timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Education Indicators Table
CREATE TABLE IF NOT EXISTS education_indicators (
    education_key INT AUTOINCREMENT PRIMARY KEY,
    year INT NOT NULL,
    literacy_rate_adult DECIMAL(5, 1),
    literacy_rate_youth DECIMAL(5, 1),
    primary_enrollment_rate DECIMAL(5, 1),
    secondary_enrollment_rate DECIMAL(5, 1),
    tertiary_enrollment_rate DECIMAL(5, 1),
    gender_parity_primary DECIMAL(4, 2),
    gender_parity_secondary DECIMAL(4, 2),
    
    -- Country metadata
    country VARCHAR(100) DEFAULT 'Senegal',
    country_code VARCHAR(10) DEFAULT 'SN',
    
    -- Data source
    data_source VARCHAR(100) DEFAULT 'Education Indicators',
    
    -- Audit fields
    ingestion_timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Health Indicators Table
CREATE TABLE IF NOT EXISTS health_indicators (
    health_key INT AUTOINCREMENT PRIMARY KEY,
    year INT NOT NULL,
    infant_mortality_rate DECIMAL(6, 1),
    maternal_mortality_rate DECIMAL(8, 1),
    under5_mortality_rate DECIMAL(6, 1),
    vaccination_coverage DECIMAL(5, 1),
    doctors_per_1000 DECIMAL(4, 2),
    hospital_beds_per_1000 DECIMAL(4, 2),
    
    -- Country metadata
    country VARCHAR(100) DEFAULT 'Senegal',
    country_code VARCHAR(10) DEFAULT 'SN',
    
    -- Data source
    data_source VARCHAR(100) DEFAULT 'Health Indicators',
    
    -- Audit fields
    ingestion_timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Infrastructure Indicators Table
CREATE TABLE IF NOT EXISTS infrastructure_indicators (
    infrastructure_key INT AUTOINCREMENT PRIMARY KEY,
    year INT NOT NULL,
    electricity_access_percent DECIMAL(5, 1),
    internet_users_percent DECIMAL(5, 1),
    mobile_subscriptions_per_100 DECIMAL(5, 1),
    paved_roads_percent DECIMAL(5, 1),
    airport_passengers DECIMAL(12, 0),
    improved_water_access DECIMAL(5, 1),
    improved_sanitation DECIMAL(5, 1),
    
    -- Country metadata
    country VARCHAR(100) DEFAULT 'Senegal',
    country_code VARCHAR(10) DEFAULT 'SN',
    
    -- Data source
    data_source VARCHAR(100) DEFAULT 'Infrastructure Indicators',
    
    -- Audit fields
    ingestion_timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Social Indicators Table
CREATE TABLE IF NOT EXISTS social_indicators (
    social_key INT AUTOINCREMENT PRIMARY KEY,
    year INT NOT NULL,
    poverty_rate_percent DECIMAL(5, 1),
    extreme_poverty_percent DECIMAL(5, 1),
    gini_coefficient DECIMAL(5, 3),
    gender_equality_index DECIMAL(5, 1),
    women_parliament_percent DECIMAL(5, 1),
    social_protection_coverage DECIMAL(5, 1),
    
    -- Country metadata
    country VARCHAR(100) DEFAULT 'Senegal',
    country_code VARCHAR(10) DEFAULT 'SN',
    
    -- Data source
    data_source VARCHAR(100) DEFAULT 'Social Indicators',
    
    -- Audit fields
    ingestion_timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Comment the tables
COMMENT ON TABLE economic_indicators IS 'Comprehensive economic indicators for Senegal including trade, debt, and FDI';
COMMENT ON TABLE climate_environmental IS 'Climate and environmental data including temperature, rainfall, and agricultural indicators';
COMMENT ON TABLE education_indicators IS 'Education statistics including literacy rates and enrollment by level';
COMMENT ON TABLE health_indicators IS 'Health indicators including mortality rates and healthcare infrastructure';
COMMENT ON TABLE infrastructure_indicators IS 'Infrastructure and connectivity indicators including electricity, internet, and transportation';
COMMENT ON TABLE social_indicators IS 'Social indicators including poverty, inequality, and gender equality measures';

-- Key column comments
COMMENT ON COLUMN economic_indicators.gdp_growth_rate IS 'Annual GDP growth rate (%)';
COMMENT ON COLUMN climate_environmental.average_temperature IS 'Annual average temperature in Celsius';
COMMENT ON COLUMN education_indicators.literacy_rate_adult IS 'Adult literacy rate (%)';
COMMENT ON COLUMN health_indicators.infant_mortality_rate IS 'Infant mortality rate per 1000 live births';
COMMENT ON COLUMN infrastructure_indicators.electricity_access_percent IS 'Percentage of population with electricity access';
COMMENT ON COLUMN social_indicators.gini_coefficient IS 'Gini coefficient measuring income inequality (0-1 scale)';

