import os
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment
from pyflink.table.expressions import lit, col
from pyflink.table.window import Session

def create_sessionized_events_sink_postgres(t_env):
    table_name = 'sessionized_events'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            session_start TIMESTAMP(3),
            session_end TIMESTAMP(3),
            ip VARCHAR,
            host VARCHAR,
            num_events BIGINT
        ) WITH (
            'connector' = 'jdbc',
            'url' = '{os.environ.get("POSTGRES_URL")}',
            'table-name' = '{table_name}',
            'username' = '{os.environ.get("POSTGRES_USER", "postgres")}',
            'password' = '{os.environ.get("POSTGRES_PASSWORD", "postgres")}',
            'driver' = 'org.postgresql.Driver'
        );
    """
    t_env.execute_sql(sink_ddl)
    return table_name

def create_processed_events_source_postgres(t_env):
    table_name = "processed_events"
    source_ddl = f"""
        CREATE TABLE {table_name} (
            ip VARCHAR,
            event_timestamp TIMESTAMP(3),
            referrer VARCHAR,
            host VARCHAR,
            url VARCHAR,
            geodata VARCHAR,
            WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'jdbc',
            'url' = '{os.environ.get("POSTGRES_URL")}',
            'table-name' = '{table_name}',
            'username' = '{os.environ.get("POSTGRES_USER", "postgres")}',
            'password' = '{os.environ.get("POSTGRES_PASSWORD", "postgres")}',
            'driver' = 'org.postgresql.Driver'
        );
    """
    t_env.execute_sql(source_ddl)
    return table_name

def log_sessionization():
    """
    Instructions to Run:
    1. Ensure the `processed_events` table in PostgreSQL is populated with event data.
    2. Run this script using the command:
       docker compose exec jobmanager ./bin/flink run -py /opt/src/job/sessionize_job.py -d
    3. Verify sessionized data in the `sessionized_events` table in PostgreSQL.
    """
    print('Starting Sessionization Job!')
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(10 * 1000)
    env.set_parallelism(1)

    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    source_table = create_processed_events_source_postgres(t_env)
    sessionized_table = create_sessionized_events_sink_postgres(t_env)

    t_env.from_path(source_table) \
        .window(
            Session.with_gap(lit(5).minutes).on(col("event_timestamp")).alias("w")
        ).group_by(
            col("w"),
            col("ip"),
            col("host")
        ) \
        .select(
            col("w").start.alias("session_start"),
            col("w").end.alias("session_end"),
            col("ip"),
            col("host"),
            col("*").count.alias("num_events")  # Corrected here
        ) \
        .execute_insert(sessionized_table) \
        .wait()

if __name__ == '__main__':
    log_sessionization()
