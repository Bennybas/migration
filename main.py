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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_multi_export_20260331_172537.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEHoaCXVzLWVhc3QtMSJHMEUCIQDqaA0WfCEp5wWlY0ikUQoK2ZQm%2BkaTTz%2Bkf5azTfLoHQIgWaOvWhxUv7xYsicee09S17mnc86nkghOWWv2B5lvZygq0AMIQxAAGgw4MjAyNDI5MDMyMzUiDGspe3d929T4vOJM%2FiqtA3bGhECwmxMF9cvDE5NiZlj1co9s6ySc40gMRoCgMiB8h4jaMuSmoYSMO4R6tMHrRzfTWGs6Ig7p2EpL3UTGKRoFi24jwgfKuJ9j4RsNSpo3bDUe2TjoggcOgC%2F%2BCKjznjtbgticOFzogUDxcIXVqD7Foba7kjd7J2EwCOrhNwtoIC%2BWdbs1MVNL%2BQ4tQb6waJLTVkhAzQvt%2BVAJeIztxZOZzdc2gECnuJuqv1bqhRBujj%2FI2WPHXw%2B8dD7Y%2BfyKFeNj3jvuteqnQ6A2GSLvjR9agouTyDtdiQLaeXCGDf1AT6rToO4FeG8hFKnn%2BvT6WaKfXqfmhMURc9rf2GqG%2F01U4FVNwKmJahXOYAptz6MLWqLEEGLEln%2FyMkG7rCLQYHTqr6wfJdI72wY6GtKQAiqCSomfLcH541ZYbpIJajg14V%2BvOQMMdpUXTbsvxclfVGYbsCG8ZeYojVk%2BIfFloIWIUNyF6Y5hepKWrCtT%2F8yIO4vUD9gNvC6IV6FZD1a7TRWFC5OuffIcKMK0doIbTKZ5C%2BYpYSmo7d53xnzAKZXB7zFiZvq8XK5Mf8mbsjDclq7OBjreAgWbzgKZpUnWQ5J92tLz9o1RXtfVWbIoGC961thDgff%2BdT3ePrvKAI2TPzPvjT7e35WB4XpX5m3KLksWKdgD3NdjzSK5HBh4RoNYPpC5UpLxQJSiigRTZxu%2Fn9Ww00eyk4cBzIf419eVgtayGd7bBSmsutBOvPTgUnNfX7PKhCY%2Bg3nFsUtkMnmfC6NaWdEhBEJ5QmIEuVaxvmPl1DMh5F2R4k%2BkWmfaWUHPeO1jzijmcGVbExqgHHohOeJfLIMFn9eQCiahieJgUfqDUSYqH0Fj3unL68wLQroXS2NRFm2xboyJ3nGHSwsYpGWcETMauuiSkn58PbXvGOOHpQTTvi5%2BkcDe0U%2FXPgRJ9XLizSTCjWHnfkfwnyzCaoEI7Ome3%2BWSGcU%2FAjL5uS8u8l9S6BZMtKYhAmFQNb68poEiRhEP76Jd3IdWkIQTuauZ%2BFlfWEcTVuesT9RF0icL1Tew&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODBSME26DW5%2F20260331%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260331T172800Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=86ab17bc72b4dcd0848417fb39af07249dfd8f2301790495bffbea111b9c5555")

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
