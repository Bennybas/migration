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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_multi_export_20260414_035806.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEL3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQC8OWwisNdLdIL9jwDMmmvyoVCfp6FCRQGJbFz2jH9%2FZwIhAICIy1vmcqw4%2BrwYmsxvIPlUN5b0GzihR1cLkVaoU5Z3KtkDCIb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMODIwMjQyOTAzMjM1Igz2c20p9N%2Bzk8XG8gsqrQPs%2FqedC6MSp9K%2FvT73xIHgpspuVFCAXb%2F25m5PF%2B%2BIbQekE9sMfXF%2FLwegcVnSxZfTnDfHuTKJBEwYdYKjiZ46U%2FVywa0xXwka9jd4XIIB8oXBLLNN6%2FIW9utWWwRuxXY8hf5U%2BO87E1WPdt4Hhmicfxu3EbmJi4lCQU0hbHxAg5D1MZ3ZJ80%2FTQdAUN84vNuE7miQJb%2B7pIKWKJWnl5XZl9riticc%2BAauvt%2BRB7I85KEvA3dyKnZpt2XNscp87but1ZEc7yO0xUkqDXT2As64YPScuv9uC3sBGz9aSrJ3xdL2H%2FpcQmyTa3bFYOLyATfvH1AU4nXJmiw9kQGZ40RaOCCVX2F5fCV6nq9CSy5fm%2BnSKhbvySgOYClIezIpg7NnIwzbfWS4eXlcOH5Cf9JyC%2FdY1fVZlzTKjrspkO20fE21sbiJz4Qz%2F3FJvnDDS%2FshsdpPoRLCZm%2B1ToZy14uTFq80j0aTq%2Bwz78HRMJxhvNI%2BUvitOfsI8RdrwPWTELRle7E5Y3CobOwtYoTdRIz%2Fm1hIly5yrqWAylmFaGMXAZBsDusiSp11cJAY8sww6Yz1zgY63QKIvYUZdRKA3kkWHm70cJMtoLjIGT%2BFFZVnfiIRyHMLphohvlOXlWL4XNS2PSSIQkVg8rCSpt7ARt%2Bas8G3xAQySeRtrsK%2BOgw5ZmujkmqH2WvJZVVsyZiTlHrZ4kC%2F%2BXW%2FkZbsokqZQq5mC9u3tfYOfpS7k%2BgFl3dHmlUVLzJRSnUqOa137l8VjIlT7hwqjalFrw3zoqfHz0q%2FF8vApzlXENOh26Oe78tnfZ%2BxMPd3GvwfA54%2F47nmisAi%2FFGDWfOmAE6g3StKm8dd61TDAD58Qnwo%2Bmndy3me%2B2akckVp%2FntQR8jfuz1YUsW3LWajDaGSbhJXj9dOih44ScuBd5OrQhpoaPNmwtOVrzM7H7WZqHyfPGZea8x9TWeE%2FvOy3gpKrfdvpOkYxvU7%2F3rxvQCW0o3Qa6zLQcYhYAVZTTWNEahjgyMIEhTglXNRUinkBMGWOijmtzuq52DP2mDY&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODB2QTE6PFK%2F20260414%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260414T043829Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=0a95023f52fe478ad4697959e5d7014ae39284fc09da2224e5b5c3e32b9ac383")

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
