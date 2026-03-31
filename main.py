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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_multi_export_20260331_093820.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEHIaCXVzLWVhc3QtMSJHMEUCIEtpX2ry%2F1cl9z9rlbAYdyfXqEEqETHI6FOtnWacAtIDAiEAwgh7KSGPKSZKIvykV4SUrrQKFvC6RUIiyKuORiG9w%2Bcq0AMIOxAAGgw4MjAyNDI5MDMyMzUiDCLSmwBACvpRqIJ1fiqtA81hLsuDIRs5TrAx5qWCHUc2qKCM6739OAFd0FY8momSXr2nlWKyHLucORpzCneYXDNImtpXMqlkiaapXsf5Po%2BpskoeL7%2BktaVkd4yuW0Npd47Tr4maZn0%2BNeZs8tvX4bmfcMD5AyELWOExGc2bgYw8AhMfU7XdiBZdQ2fbKp8ZehMUO%2BPT%2F%2BjOUzS6MOavhrY8wxJ4TtqyV2SeJ50VFQbtvn%2FCuua1PDC9cQugrtbhmuy76POMb2vOBOCLPmp4p%2FbYlNXdH8QafzMYT7svIYaJfgBCV54MY5BQ1xWcvdKQNNZAri%2FtVdgT4sosFDzCt2FGCbSOuVIJg6vWlEydHgRsmDv%2Bf0eWynCP%2FjK7SUN3HXBW6jfwFCO4UojxAEN1WAObUfarm%2BoyNc7lZ%2BgOqmB5iYA2JP2ciwpw3obzuRSHTrA4%2Fd9FcVZGdXmkv20A%2FchLAB2A9y0Vb0b%2BCedqj2j2LQBIBsMXduafO188BE4Fry59nr%2BafgIz1XRSCfsABQnudoJXw5RGn9dxvPA6hyjGAXuj4VyiwSkRpdPdkkMfRsr5QSYAOpRvX2vbcTDclq7OBjreAnlgxUpc0%2F%2FopzHAVIW3wKV7w86uMFXNM2cc6vMNnwwh0Hh%2BQIjqVzCrxkXX0GAcbRQ1oBTcxWHQk%2F7YGDj7XfCoZ3%2FqXci0WG8TF64cR0oOUT9TXEmdarkcH9l1aqhfEwtePp5BtyEgczpqTheJ%2FTRSOps%2F9d2NTt52RDKOB4VPIZrWxnCrbyS23ImzCE1Xe4SGe%2BkuRy4F7SaTSwkJWjEdv%2F9CyGZI%2BrDo2Yfch3PFc4Z%2Bolu10N5Bhc8Mgy6iR5MIttK%2Bv%2B5%2Bq%2FA%2BHtno%2BkoHO%2FWQ8R2DJZf3Dv1Tqtg32nYy%2F1yN%2FZ0K0qvcg4xbAHdg%2BGLlD9Bk1adT7GowoTL6faGis5nwUGc4jKIhCKxwZlxtSqCnowMSQ1znRiu307y6HZZbVmpQfxjHELObzXpMcIA6tpYubNQcKue1%2BKXG8EViUAPMsvicr6TUaUsgY2QHRLkfcHNA7sI5U%2BEI&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODB77EZSNEA%2F20260331%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260331T094305Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=a8fadb32b62006a12e21baa78a6f1977237b2c551856ce6d39a2a79abec41ab6")

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
