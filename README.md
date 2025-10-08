# 🚀 Data Engineering Portfolio
**Professional Data Engineering Projects | December 2024**

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Apache Spark](https://img.shields.io/badge/Apache_Spark-E25A1C?style=flat&logo=apache-spark&logoColor=white)](https://spark.apache.org/)
[![Apache Flink](https://img.shields.io/badge/Apache_Flink-E6526F?style=flat&logo=apache-flink&logoColor=white)](https://flink.apache.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

---

## 👋 About This Portfolio

This portfolio demonstrates my hands-on expertise in **data engineering**, showcasing production-ready projects across the full spectrum of modern data infrastructure. From designing dimensional models to building real-time streaming pipelines, these projects reflect industry best practices and cutting-edge technologies.

**🎓 Completed**: [DataExpert.io Community Academy Bootcamp](https://learn.dataexpert.io/) (January 2025)  
**👨‍🏫 Instructor**: [Zach Wilson](https://learn.dataexpert.io/) - Founder at EcZachly, Lead Instructor (Ex-Netflix, Ex-Airbnb Data Lead)

*A huge thank you to Zach Wilson for creating this exceptional bootcamp at [DataExpert.io](https://learn.dataexpert.io/)! The hands-on approach and real-world insights from his experience at top tech companies made this learning journey invaluable.*

---

## 🎯 Skills & Technologies

### **Core Competencies**
- ✅ Data Modeling (Dimensional & Fact Tables, SCD Type 2)
- ✅ Big Data Processing (Apache Spark, PySpark, Distributed Computing)
- ✅ Real-Time Streaming (Apache Flink, Apache Kafka)
- ✅ SQL Optimization & Advanced Analytics
- ✅ Data Pipeline Architecture & Testing
- ✅ Production Engineering Best Practices

### **Tech Stack**
| Category | Technologies |
|----------|-------------|
| **Languages** | SQL, Python, PySpark |
| **Big Data** | Apache Spark, Apache Iceberg, Apache Flink |
| **Streaming** | Apache Kafka, Real-Time Processing |
| **Databases** | PostgreSQL, Snowflake |
| **Cloud** | AWS S3, Snowflake Data Warehouse |
| **APIs** | FRED API, REST APIs |
| **Visualization** | Streamlit, Plotly |
| **Infrastructure** | Docker, Docker Compose |
| **Testing** | pytest, Unit Testing, Data Quality |
| **Version Control** | Git, GitHub |

---

## 📂 Featured Projects

### 1. 📊 [Dimensional Data Modeling](01-dimensional-modeling/)
**Building Scalable Analytical Data Models**

Designed and implemented slowly changing dimensions (SCD Type 2) with incremental processing pipelines for efficient historical tracking.

**Key Achievements**:
- Built actor/player dimension tables with quality classification
- Implemented incremental cumulative table generation
- Created graph-based data structures for network analysis
- Designed efficient temporal queries with complex CTEs

**Technologies**: PostgreSQL, SQL, Docker  
**Skills**: Dimensional Modeling, SCD Type 2, Incremental Processing

[View Project →](01-dimensional-modeling/)

---

### 2. 📈 [Fact Data Modeling & Aggregations](02-fact-modeling/)
**Optimized Fact Tables for OLAP Workloads**

Engineered high-performance fact tables with array-based metrics and cumulative aggregations for growth analytics.

**Key Achievements**:
- Developed user activity tracking with device-level granularity
- Implemented datelist_int compression for efficient storage
- Built reduced monthly fact tables with array metrics
- Created deduplication strategies for data quality

**Technologies**: PostgreSQL, Advanced SQL, Array/Map Types  
**Skills**: Fact Modeling, Data Compression, Growth Analytics

[View Project →](02-fact-modeling/)

---

### 3. ⚡ [Apache Spark Production Pipelines](03-spark-pipelines/)
**Distributed Data Processing at Scale**

Built production-grade PySpark jobs with advanced optimization techniques including broadcast joins, bucketing, and comprehensive unit testing.

**Key Achievements**:
- Implemented broadcast join optimization for dimensional data
- Created bucket joins for large-scale fact tables (16 buckets)
- Developed unit tests using pytest and chispa
- Optimized partition strategies for performance

**Technologies**: Apache Spark, PySpark, Apache Iceberg, pytest  
**Skills**: Spark Optimization, Unit Testing, Distributed Computing

[View Project →](03-spark-pipelines/)

---

### 4. 🌊 [Real-Time Streaming with Apache Flink](04-streaming-flink/)
**Event Processing & Sessionization at Scale**

Implemented real-time streaming pipelines with sessionization logic and time-based windowing for live analytics.

**Key Achievements**:
- Built user sessionization with 5-minute gap windows
- Created real-time aggregations by IP and host
- Developed streaming analytics with watermarks
- Implemented fault-tolerant streaming architecture

**Technologies**: Apache Flink, Apache Kafka, Python  
**Skills**: Stream Processing, Real-Time Analytics, Event-Driven Architecture

[View Project →](04-streaming-flink/)

---

### 5. 📊 [Advanced Analytical Patterns](05-analytical-patterns/)
**Growth, Retention, and Funnel Analysis**

Implemented sophisticated analytical frameworks for product analytics including growth accounting, cohort analysis, and conversion funnels.

**Key Achievements**:
- Built growth accounting (new/retained/resurrected/churned)
- Developed cohort retention analysis frameworks
- Created multi-step funnel analysis
- Implemented window-based trend analysis

**Technologies**: SQL, PostgreSQL, Analytical SQL  
**Skills**: Product Analytics, Growth Metrics, Cohort Analysis

[View Project →](05-analytical-patterns/)

---

### 6. 🧪 [KPI Design & Experimentation](06-experimentation/)
**A/B Testing and Metrics Framework**

Designed comprehensive KPI frameworks and experimentation strategies with proper statistical rigor and business alignment.

**Key Achievements**:
- Defined KPI hierarchies (leading vs. lagging indicators)
- Designed A/B testing frameworks with proper allocation
- Created hypotheses linking metrics to user behavior
- Analyzed product user journeys for optimization

**Technologies**: Statistical Analysis, Product Analytics  
**Skills**: Experimentation, A/B Testing, KPI Design

[View Project →](06-experimentation/)

---

### 7. 🏛️ [Presidential Analytics Pipeline](07-presidential-analytics/)
**Modern Data Pipeline: API → S3 → Snowflake → Dashboard**

Built an end-to-end data pipeline analyzing US presidential economic performance with real-time data ingestion, cloud storage, and interactive visualization.

**Key Achievements**:
- Integrated FRED API for automated economic data collection
- Implemented S3 data lake with partitioned storage
- Designed Snowflake data warehouse with SCD Type 2 dimensions
- Built incremental merge strategy for cost-efficient updates
- Created interactive Streamlit dashboard with real-time filtering

**Technologies**: Python, AWS S3, Snowflake, Streamlit, FRED API  
**Skills**: API Integration, Cloud Data Lakes, Data Warehousing, Dashboard Development

[View Project →](07-presidential-analytics/)

---

## 🏆 Project Highlights

### **Most Complex Implementations**

1. **SCD Type 2 Pipeline** - Fully incremental slowly changing dimension with historical tracking
2. **Spark Bucket Joins** - 3x performance improvement using broadcast and bucket joins
3. **Real-Time Sessionization** - Sub-second latency streaming event processing
4. **Growth Accounting** - Complete user lifecycle tracking framework

### **Code Quality**
- ✅ Production-ready, well-documented code
- ✅ Comprehensive unit tests with pytest
- ✅ Docker containerization for reproducibility
- ✅ Git version control with clear commit history

---

## 📊 Portfolio Metrics

- **7 Major Projects** across analytics and infrastructure
- **50+ SQL Queries** demonstrating advanced analytical techniques
- **15+ Python Scripts** for data pipelines and distributed processing
- **Interactive Dashboard** with real-time filtering and visualization
- **150+ Hours** of hands-on development
- **Full Test Coverage** with unit and integration tests
- **Cloud Integration** with AWS S3 and Snowflake

---

## 🚀 Getting Started

### Prerequisites
```bash
- Docker & Docker Compose
- PostgreSQL Client
- Python 3.8+
- Apache Spark 3.x (for Spark projects)
```

### Quick Start

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd data-engineering-portfolio
```

2. **Explore individual projects**
Each project folder contains:
- `README.md` - Project overview and setup instructions
- `src/` or `sql/` - Implementation code
- `docker-compose.yml` - Local development environment (where applicable)
- `tests/` - Unit tests (where applicable)

3. **Run a sample project**
```bash
# Example: Dimensional Modeling
cd 01-dimensional-modeling
docker-compose up -d
# Follow README for specific instructions
```

---

## 📚 Project Structure

```
data-engineering-portfolio/
├── 01-dimensional-modeling/     # SCD Type 2, Incremental Processing
├── 02-fact-modeling/            # Fact Tables, Array Aggregations
├── 03-spark-pipelines/          # PySpark Jobs, Optimization
├── 04-streaming-flink/          # Real-Time Processing
├── 05-analytical-patterns/      # Growth, Retention, Funnels
├── 06-experimentation/          # A/B Testing, KPIs
├── 07-presidential-analytics/   # API → S3 → Snowflake → Dashboard
├── docs/                        # Additional documentation
├── assets/                      # Diagrams, screenshots
└── README.md                    # This file
```

---

## 💡 What Makes This Portfolio Stand Out

### **Production-Ready Skills**
✅ Not just tutorials - real implementations solving complex problems  
✅ Code follows industry best practices and design patterns  
✅ Comprehensive testing and quality assurance  
✅ Scalable architectures designed for production environments  

### **Full-Stack Data Engineering**
✅ **Analytics Engineering**: Dimensional modeling, metrics, KPIs  
✅ **Infrastructure Engineering**: Spark, Flink, streaming pipelines  
✅ **Data Quality**: Testing, monitoring, validation  
✅ **Business Impact**: Metrics tied to real-world outcomes  

### **Modern Technologies**
✅ Industry-standard tools: Spark, Flink, Kafka, PostgreSQL  
✅ Cloud-ready: Docker containerization, scalable architecture  
✅ Best practices: Version control, testing, documentation  

---

## 🎓 Bootcamp & Training

**[DataExpert.io Community Academy Bootcamp](https://learn.dataexpert.io/)**  
- **Program**: Free Community Edition Bootcamp
- **Instructor**: [Zach Wilson](https://learn.dataexpert.io/) (Founder at EcZachly, Ex-Netflix, Ex-Airbnb Data Engineering Lead)
- **Completed**: January 2025
- **Format**: Hands-on projects, real-world scenarios, comprehensive homework assignments
- **Website**: [https://learn.dataexpert.io/](https://learn.dataexpert.io/)

**Why This Bootcamp Stands Out**:
- 🌟 Taught by an industry expert with experience at Netflix and Airbnb
- 🌟 Focuses on production-ready skills, not just theory
- 🌟 Covers the full data engineering spectrum from analytics to infrastructure
- 🌟 Free and accessible to the community
- 🌟 Includes advanced topics like SCD Type 2, Spark optimization, and real-time streaming

**Course Modules Completed**:
1. Dimensional & Fact Data Modeling
2. Apache Spark & PySpark Optimization
3. Real-Time Streaming with Apache Flink
4. Advanced Analytical Patterns & KPIs
5. Experimentation & A/B Testing Frameworks
6. Data Quality & Pipeline Best Practices

---

## 💼 Seeking Opportunities

I'm actively seeking **Data Engineer** roles where I can contribute to building scalable, reliable data infrastructure.

### **Ideal Roles**:
- Data Engineer
- Analytics Engineer
- Big Data Engineer
- Data Platform Engineer
- Senior Data Engineer

### **What I Bring**:
- Strong foundation in both analytics and infrastructure
- Production-ready coding skills with testing
- Experience with modern data stack technologies
- Problem-solving mindset with attention to detail
- Passion for building reliable, scalable systems

---

## 📫 Let's Connect!

I'd love to discuss how my skills can contribute to your data team!

**LinkedIn**: [Your LinkedIn URL]  
**GitHub**: https://github.com/Abdoul84/data-engineering-portfolio  
**Email**: [Your Email]  
**Portfolio**: https://github.com/Abdoul84/data-engineering-portfolio

---

## 🙏 Acknowledgments

- **[Zach Wilson](https://learn.dataexpert.io/)** - Exceptional instruction, real-world insights, and for creating the [DataExpert.io Community Academy](https://learn.dataexpert.io/). His experience at Netflix and Airbnb brought invaluable industry perspective to every lesson.
- **[DataExpert.io Community](https://learn.dataexpert.io/)** - Collaborative learning environment and supportive community
- **Open Source Community** - Amazing tools and documentation that power modern data engineering

*Special shoutout to Zach for making world-class data engineering education accessible and free to the community! 🙌*

---

## 📄 License

This portfolio is available for educational and demonstration purposes.

---

<div align="center">

**⭐ If you find this portfolio interesting, please consider starring the repository!**

*Built with ❤️ and a passion for data engineering*

</div>

---

*Last Updated: October 2025*


