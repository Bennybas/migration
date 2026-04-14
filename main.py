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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_multi_export_20260413_102823.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjELz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIFj3KaBwOx20bbsjAWftfmAuR6Dhz1f0QPeR%2BDLAmHnUAiEAy%2F3znZ%2BJPXlEZoBoLRUW6nmy5p8Br9NaMoNMGoWTIYoq2QMIhf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw4MjAyNDI5MDMyMzUiDIYHyfuzwXdeO2piwSqtAzO6cBjuzTj6ZGpFUbCJ0rpMSL3XVjbDXXvdRSgz%2FGDGIbk0k%2B4H1nDdXBjgEdFMmsFiHH%2BGItzF6tQnGnqYCly%2FliFFGpYnYvpDGH7CCzeo8FhTWq8kpYiTbS9gHmnVq403R9ke1WvFQ5WesbNsRW%2BOU3342tXXdJrK6C2z7mtAV1IERNQZVQwBxUskhY9BEuu4AzYvqaZfedr6vj3syvCE%2Bhz3CwLYfVOzdQ9547529Ge6i2AzFp8VqfAN4D0FlVjM%2FWnCu7DV0012uCyykaBPA4PkAQYfC%2Bojm4VghwAIsruCDt1avLLD4TKj2bmeuTiuG8%2Bw5lSErNA30Cjjs%2FksoPPVOfl3FcGPjiFEalzi71rvAmDkXpL8E0xYLxtlBb8Zx8KY869MJNH1vTa0TnemugQaafKBCA%2BzYxjniofsBU%2Br5qptWiS9pksTK3ppLIC8cuasyeUUC3HrS%2FF5FhUrNIZ62fF82BqDXJ0mi6c1uWgxwJT9A%2F2o4j6PwvwKB%2FbrC65GqCYVs2038za7VO4LwrnpbDKCb%2FLsubZRHjp8syrElMUWNh7T57y18TDpjPXOBjreAmsRPK8gibqmrfn5Pgge7KaAdhSuL0ARkecHPEAzhAJtnvlmBMpPK7JbukPrTCMcz%2BvpEgCe90sQmt%2BX6Zr55CINXqn6bqHb0lhnEojSAVAbRay7tfkinVLkwzFDhvWz%2Fvtp%2B%2BqYArx%2F6rOKBg5rNkqjeJHStIoedJiU8EL%2FD%2BANfJQadZf8Q%2BYNQfbluqf3GsQC%2BVvKG2UheKG9zAhHmOsAbSRUmHfFLqXwc%2BDnZcREKWtd3ryKzj6btdHXcTutNDr5A%2FSxOi4%2BHgS7IYYLOmvF9T9C1MrBsshi3Bl3XSXMg9huE7pD5bBf%2BazNSYCauqppDdL5AuxnNr931esIFXRvewmKbnRe9E0TQgomcNN2%2BinT25mTnZON8VvHLsRAT8G%2BNs0OarWsTvhQ%2FK7XtTIc22m%2BC6J4sJSSA9O1w14g2mVDkfnW8Lp3x%2FU1Q%2BuKW2Emd7Y7WrQX8QImvCae&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODBZTOGNXUU%2F20260414%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260414T033719Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=a655ff9efbade7661bdc4cc7394f63894020ef2270a6821e40b38bf9de457b2e")

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
