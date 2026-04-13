from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import os
import logging

app = FastAPI(title="Migration Service API")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# Pre-signed URL from environment variable
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_multi_export_20260413_102823.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEKv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIArwnw1M1kkw8C96nIZjeCiluO871YR2lsD6ElLfMIUlAiEAmECIuMTXuh9CKqnjTspw1Qvrg5Cd649YDyEAhP0Ip7Mq0gMIdBAAGgw4MjAyNDI5MDMyMzUiDEWBUJkPgfBhbUVYOCqvA67d6zey9squnWCKYy3%2Few2fupZWeRKzdd1lASDalJ%2FWgftiQ8wp01RrcZzHR87OOoYOw93XGqvG%2F3Ukl5uai2PNlp51MTsdK9vu%2FaZbS%2FaoeeSeLjdbpZ1Qv19MJXUz1QeTOxaSaJefPLrc8%2FmDHL3aZBC5QQKbKMYTBBOB8QkFUu5%2Bn8HlFkywi8d85rOEEWvzbcp5WnqSt5qUtzcrnfsxlNO4BAj6FjJAQUtou1OpmzGJMukNR96c9jA9JN5CjJaliWC3RUpNGb4vdwvTJkxkCULwWgcJ93cy20L0BNssyW9Irptj%2FRWMGsggU4woOMyf2KnLtkUwW9SXuM3nx3onRh0kQyXzEnK9GUYyjtTfIhGtH%2FfLnxn%2BIa4hYuZ%2Bwxk95MaWsspLZ0ywd4u1EnHhSjIpe5I7krq6Ce43kKoGQvD3mb2mjONxme7Tl%2BKhbHTOKjS76EQgeerLE%2BPRhlJ%2Bgb%2FQN5NQ%2BsAoyXlnWiU1aZ4wXaJh5D8wh9MSzr3gC1ekTIJWwfrIDx5p5y9NGpmWU%2FtC%2FBmHWbB3JMTk5bbRrNTo1HdTZ%2F1lT7azFj89MNSQ8s4GOt4C5dD1vtYu%2B6PPiGw4QYT4zi2V1QWcyypSrtQeybat5ePfHdtOmuUzFMM992%2FQMgrO4j%2B6Lx2NA9kbiDcySu0Iq%2FnVuCk7ccV9lyy3%2F0t%2BghQkNPu%2BPEzJ4U6T%2FJvq5nRf3mWzhp3tkxPo%2BE12hycVtGWvWfqW4aybF5sICXIDamaGVb8zw%2F%2BoSph2YQLbFM9%2FI%2FgMlRvrcud1SP7WLpcAJQXGeOw6jn%2F8UwnNGLRNbwhpKLnthwxgSMegRJmiAlMdSjS4wqEy4xUXncakByz0iCKFUdOHJaedbBzzMYs0e1qln7D56u2ut4yvE9zT5%2B3kKqhdT9WEYrMdIP%2F8AXLoXBa%2Bu1kmH8vDy%2BFAKMNLCtcXExpZTXio6xpGWJgz5VpYUiPZ9LP74wJVxh9WHEjN3JLm%2Fe5L1mjItfsLZ3T8MOZLASGB4HE9g2s0lYZUlzTGOoAIz%2BtmWJiHgVRJhzE%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODBW6DSNXAB%2F20260413%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260413T105756Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=2d7c63613c7c96c6b4f1d67088469dc507cfbfcff9d26cd124e4845fa6655d3f")

@app.get("/")
async def root():
    return {"message": "Migration Service API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/migrate")
async def migrate_environment():
    """
    Returns the pre-signed URL for migration files.
    """
    if not PRESIGNED_URL:
        raise HTTPException(
            status_code=500,
            detail="Pre-signed URL not configured (MIGRATION_PRESIGNED_URL missing)"
        )

    logger.info("Returning pre-signed URL")
    
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "presigned_url": PRESIGNED_URL,
        },
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
