# YouTube Trending Analytics Data Lake

A modern Data Engineering project implementing the Medallion Architecture (Bronze, Silver, Gold) to ingest, process, and analyze YouTube Trending videos data.

## 🏗 Architecture Overview

This project is designed as a portfolio-quality, production-ready Data Lake system. It extracts daily trending data from the YouTube API and processes it through a multi-layer Medallion Architecture before loading it into an Analytics Database for visualization.

- **Orchestration**: Apache Airflow (Dockerized)
- **Data Lake Storage**: Local File System (`/data` directory simulating S3/GCS/ADLS)
- **Processing Engine**: Python (Pandas, PyArrow, FastParquet)
- **Analytics Database**: PostgreSQL
- **BI / Visualization**: Power BI / Metabase connected to PostgreSQL

## 📂 Data Flow (Medallion Architecture)

1. **Extract**: Fetch trending video data from YouTube Data API v3.
2. **Bronze Layer (Raw)**: Store raw data as `JSON` partitioned by `region` and `date`. This is an immutable exact replica of the source.
3. **Silver Layer (Cleaned)**: Read JSON, handle NULLs, clean text, and cast data types. Store as `Parquet` for optimized columnar storage and schema enforcement.
4. **Gold Layer (Aggregated)**: Aggregate data based on business logic (e.g., daily views per category, top channels). Store as analytics-ready `Parquet`.
5. **Load**: Upsert Gold datasets into the PostgreSQL Analytics Database (Data Warehouse).

## 📁 Project Structure

```text
youtube-trending-lakehouse/
│
├── dags/                           # Airflow DAGs definitions
│   └── youtube_trending_pipeline.py
├── src/                            # Core ETL logic (Decoupled from Airflow)
│   ├── extract/
│   │   └── youtube_api.py
│   ├── transform/
│   │   ├── bronze_to_silver.py
│   │   └── silver_to_gold.py
│   ├── load/
│   │   └── postgres_loader.py
│   └── utils/
│       └── logger.py               # Standardized logging
├── data/                           # Simulated Local Data Lake
│   ├── bronze/youtube_trending/region=US/dt=YYYY-MM-DD/
│   ├── silver/youtube_trending/region=US/dt=YYYY-MM-DD/
│   └── gold/daily_category_metrics/dt=YYYY-MM-DD/
├── docker-compose.yml              # Container definitions (Airflow + Postgres)
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
└── setup_datalake_dirs.py          # Script to initialize folder structure
```

## 🧠 Engineering Decisions

- **Why JSON in Bronze?** The YouTube API returns JSON. Keeping it in raw JSON in Bronze ensures an exact, immutable replica. If transformations change later, we can re-process from Bronze without re-calling the API (saving API quota).
- **Why Parquet in Silver/Gold?** Parquet is a columnar storage format. It heavily compresses the data and is highly optimized for analytical queries. It also enforces strict data schemas (e.g., ensuring `view_count` is always an integer).
- **Partitioning Strategy**: Data is partitioned by `region=.../dt=YYYY-MM-DD`. This enables partition pruning, significantly speeding up reads by allowing engines like Pandas/Spark to skip irrelevant directories.
- **Idempotency**: All Airflow tasks are designed to be idempotent. Running the pipeline multiple times for the same `execution_date` will not result in duplicated data, thanks to directory overwrites and DB Upserts.

## 🚀 Getting Started (Phase 0)

1. **Clone the repository** and navigate to the project root.
2. **Setup Data Lake Directories**: Run `python setup_datalake_dirs.py` to create the `data/` structure.
3. **Environment Variables**: Copy `.env.example` to `.env` and fill in your `YOUTUBE_API_KEY`.
4. **Start Docker**: Run `docker-compose up -d` to spin up Airflow and PostgreSQL.
5. **Access Airflow**: Open `http://localhost:8080` (Default credentials: admin / admin).
6. **Trigger DAG**: Enable and trigger the `youtube_trending_lakehouse_pipeline` DAG.

## 🗺 Roadmap

- [x] **Phase 0:** Setup foundation (Docker, Airflow, Postgres, Folder structure).
- [ ] **Phase 1:** Extract layer (API Wrapper, Pagination, JSON Dump to Bronze).
- [ ] **Phase 2:** Silver layer (Pandas cleaning, Cast types, Write Parquet).
- [ ] **Phase 3:** Gold layer (Aggregate views by category, Top Rank, Write Parquet).
- [ ] **Phase 4:** Analytics database (SQLAlchemy load from Gold to Postgres).
- [ ] **Phase 5:** Dashboard (Connect Metabase/PowerBI to Postgres).
- [ ] **Phase 6:** Production improvements (Data Quality checks, Retry strategies, Alerts).

## 📝 Commit Guidelines

Dự án này áp dụng tiêu chuẩn [Conventional Commits](https://www.conventionalcommits.org/) để quản lý lịch sử commit một cách rõ ràng và chuyên nghiệp.

**Cấu trúc:** `<type>(<scope>): <description>`

**Các loại commit (Types):**
- `feat`: Thêm tính năng mới (Ví dụ: `feat(extract): add support for youtube pagination`)
- `fix`: Sửa lỗi (Ví dụ: `fix(transform): fix null values in view_count column`)
- `docs`: Cập nhật tài liệu (Ví dụ: `docs(readme): update setup instructions`)
- `style`: Thay đổi giao diện, format code (Ví dụ: `style(dags): format python code with black`)
- `refactor`: Tái cấu trúc mã nguồn, không làm thay đổi tính năng (Ví dụ: `refactor(db): change postgres schema structure`)
- `chore`: Các công việc phụ trợ, cài đặt môi trường (Ví dụ: `chore(git): add .gitignore file`)