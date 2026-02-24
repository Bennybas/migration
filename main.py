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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_export_20260224_082124.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjECkaCXVzLWVhc3QtMSJHMEUCIQC2HpPwAr%2Bkk1Qexnt1C7DHvKnpgzwb9KxetdCD12g1WQIgIHv4mr%2Bz1l3O7FFBCT3lLXI2PvKCkecF%2BA1G6FffY20q1QMI8v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw4MjAyNDI5MDMyMzUiDNOI4HBQzufWj7iMsyqpA4J9ke949%2B3mKLAeuV752Y7HeqGA%2FxNC0VR%2FNi%2FJA%2FzFfMsKtaZ0i7A1iddGLd0hWhTQv9%2FYuYxB8fgTpbQJnk7FUZtFCj3AYnBkXqzBO4Q69%2Bl6kWiA25DfTTfHzmeaGjJXRhMyt6b9VpuhLc6ub8o9LUShekYf%2F7uNlHmKbenIsXGSIoM5XF4c9jf2JzU5OSRtH8F%2B0mUeWhZfIM7ziuNRqoExwlDLDFDhqblDJ5vIYo0sKzJzOpF9HMeBen2P6noQ2854mqfWY%2BAN4WogHxx8DZqvJutNnYfhnlN5TgrOHPxAttTMt%2BtGDAweMP0K%2FLqQhwcIIAc2dAFBn7mRx%2BruaXCcOuCkPCVpen4MGK8vEtyL7o6sgzdwks1FZRA8S9rvP%2BSTr7SE0cdCl6xj372TrAwK0xT5Ml0GolOSyfAqjP8sDG1WzxIzyKxzGId2I0H3Vkt3Ymq%2BlLWCdZBfNw0%2FYzfmCRSFIhJ8ma8jD34lRtluK0XeCC2MbC5huPi2vHMuTLnfSO7PqrXV5l07CO2XfwXW1cAI7oDlQyNv9f7mmSuegh9QEC%2BgMJWo9cwGOt4C9dthe3oDTujeGsdQn5CCQzJEWiAZnVunHwdEe1hrpufawLOL8wSGrSr1G0OyRsI7nQORV%2B7mGdN4hQRJnmniemETi%2FVVo6eSS9k2UNPfM26DRM5BBQ2sUjnFzQjykJtuAdRuXBdMFGcZWqeUSScW2J2JH6H3a908rj3h2m59AQ2va8s6766QpPDPj0jrxOWQjJYUmnGB5aweBOWMJUXQGbe2Qvm9lu%2FnhsrtTgHW5%2Fg39vlBUbLDp%2F1%2Fd4aGlbwSxvAZoQYSgKsR2HCTA0d5%2BkPjckRpilkx%2FCDMVJelV9tNcp3Xl%2FgVqoHeYTH9PNYCWbX49BRgSKknQ6imwjT5r2kcG4tifd%2BZKHgr%2FiHFWt6dc%2BLLxWlsLuYz5owRxWgOjAbEXmKXVupZA4KZ4mU5FRM8AeOVEtAg7BDNfuQ%2BGkCIWZrOBbeTJFG%2B9JRi68Fjp6RwUS0sjdFu3Avcmew%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODBWMHRS777%2F20260224%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260224T082545Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=5e48fbf0a712ab2edc8c981354333101f411457ce9b78966a76c16d52f3f9427")

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
