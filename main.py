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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_full_export_20260219_204450.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEL7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIELVCcIKnHec92mjvlZ7QX1%2FDn2k39UQrY9TsTjb%2B4A9AiEAmD9TIfmsNHbgJFwAcmqfe%2BvWIWEwSKy5OxHrVChMKeIq1QMIhv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw4MjAyNDI5MDMyMzUiDIJtjulwwJo%2FKmChlSqpA6YFRfPLBiX%2Bpfd%2BWZItl5h%2FmfvP1A9twg8SeFglcKci0fAaAzXnn8pABv3H6AzlptM80PYaUKjYCfrnRY6Iuthqvw2JmuAJAyVWVjDpbiT942BglAxYz2EiaF5dsYIwvWOjfc1QzdaymUJQEgqPWV0YQkjrGnoy9Z9so1DAXKo7GCiSdbXMfSTOkUzFtcx80eUICbhFoREQazkiBxYNU68q6vqq3pALuoMWoKlovDResjcJjFRPzcNzvhBrnxpPOYArtgx9i3o31XA%2Fr2yqa51F6faySV8NYyY7e9XeXfl8xopF2mj5D9dTHWcNr2J6ABI3iTyWLIDujf5qNwu3wk%2BVxXHGYG%2BMo99bFDfj5NH7alusCJJDMQjeq3RpsplJzKg3h5%2FF31Enik9o25yZjJADlou3SbI2LPtAgoivMhu1EzHj2NMOa%2FS4ob4FIwYVpVy4iMSO9FUq0CS7Qftpo7zHUINSWYIq2A8BI3Jfjnsn6uv%2BIB2%2FwkRdr5GYVtoRKCk6MKNQPrFYkL7Jx8U14R3tsJTWKoBT70oF9vhsfyGKczxRc9tNSuaqMPm13cwGOt4CRU3ZeA%2BAZVHyv2%2B5VkE03%2FoH%2B8019D0uOa5GZLZpEhkOnYzaa4vdymdcEmCk%2Bt3U5Rr%2FcBWTxEnxQRd67hLcvVBkWsvKAwoJSosFNI7ZFp4MpWGlOkzzeHR7fYPVIGxZZW2S%2FfoGospLzOx87pJvgM4HlKFAttF40dDtAAMhypBQTigCfM2rdUijV%2FSAiMizAJ9yS0%2FBJCyrX4u2EDLti9bOGQ6AVwPk2dL3UZ3VBi%2F0PamCUzvAda4vD9WiVxxVyJvEJTI6Fia6gYdJbAhU2cpIb8O3D1EnHkZm9ZQQUvIL%2FDJm25uUJZDaIF8%2BvrRBlMI1JD6LtFfdJRBu0rsaozYL5u2T422bNu3Cps%2FRcM49KDtUXbkyJbGaAfhfjyJ1xTMfnTj3eqxRJ3KixEn%2Fhv9oD3yTehrbkuqicwSqfTYc40UXAQjnr61Fwl6PcptD9nnAfjwGXlmilr0h2mM%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODBZRBTQJ6O%2F20260219%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260219T211302Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=33c1ce37ff83ea1cd6289dc41e0de3d3b8146a97e6f42e916e269be00c0159f2")

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
