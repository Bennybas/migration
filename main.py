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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_multi_export_20260331_172537.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEKP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIQCbLBb38yOBNq7UkkPpYKmW25qUsIz9aOzF1ZEWuJR%2FnAIgL59fRzVLZ5LuZvjirEQol9OiAKoNmzwoE2zp3hC8IaMq2gMIbBAAGgw4MjAyNDI5MDMyMzUiDONQyteiV6QSFaMF9Sq3A1fzEyrsmtw%2F%2BBM2hwG3qmsD0VsPl1GtZeNkYrigOBo6q%2FVEQ%2FcxfP3GEabySAoOxjwX%2FQf6Lir62JiNboaIL55KOeVmJiayEnQag33u6ajuFUem2Jgl4zLHJyzyI8klnCVe8GzCIn3vJBXVmWmGwfJegqt2XrsiZS3%2FIirBdHSuilYPtiWskqbSKIwB4SE63Vz2A8hKucFv5N3UK9tPtXIGu2Wf5hrWErs26Hoslen44zWXcYklf805cG7om%2B5QVwR64QeTYCNzW57QpjpwfZsh8IHh2b%2BJsr0ctUCKArAJlCnDCm9CPGF0D37aKQSA%2BYvjNc2MFNOHcYzWLsPa9C9IkoXixFQX5eAtcbUyBrthSQK6moYM3FSL6otrMl2HuKRIsnGRPOgSLiO%2Fb1EgkTaxu1AphSQzysQPMAVa1qg4IPEAYV1kNw1Rq8AHabIPnT7EddnRL7i1rIVS4InYgFY1DfdeodzsvtKuCW9yw3w0efk%2BAwXUHzQzrweKoHzuMQ6pGcKQFW3kpA9eJUheCxTjeg%2BmUOcE1F2LiOLmp%2BLAUARON%2BcNCBrQaW7ieCKNKg4F1rUnjekwlMW3zgY63gLdp8kkGqBtdkbfxny9eJQtW%2BNPiQ4in9Iy9x8gral766QMFTwhlxTT4ehr5dvkc0ML8GhJgQDppeZ1FVSS9ShddbEqk4w9sO8gaFcwyOVRo%2FjAjqQpIIWpDmsUKj%2F1t3gmNQmY%2FW2kd0aElz9bHFRYSlIxGczPXXhQAftHU4JyXZ%2BfNnRkv7%2FUMTf9i8hhKdBtvymDJXSSPzY9nqL9i1xE51Wzc1imDR4Fme2Az7zI3%2B72X%2FWZgm%2FQIj0H7YWk3cENLZMIblK%2BqdxxRtbUc4UY071zNmHYSRExRSIo%2BtpbfhdRL82S6NhhZ10WqZ4xb2nEzHPvx3ACYNNEXFPPaSLEm6qJeEMcvE25pDPbVG79pIfJFK3Wg9n6LJTtzPC2x9Rtz7w1XgXjKaVsND47inresbhvZSt%2FEBwXNwULswyQAkKcU5Gc3hAMMJ0dsVr32GuB4Tdq8e4Dz4WP2RXJ3Q%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODBYFM5N5KJ%2F20260402%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260402T103822Z&X-Amz-Expires=21600&X-Amz-SignedHeaders=host&X-Amz-Signature=e05840919353cc4e0438fc905c9f5fc286a3059cbbd110e860acc5f8ac1330d6")

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
