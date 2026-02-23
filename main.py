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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_export_20260223_085840.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBEaCXVzLWVhc3QtMSJHMEUCICbhseW6UD7w0F1E4QHbgIphfvCzHYU8qR5bdqokVfmXAiEAku%2BxPJL17Id0IpOpleUI0AdO7kB%2FxBZZAbF6Q%2BimEy4q1QMI2v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw4MjAyNDI5MDMyMzUiDEQxbkSC5U206ZUQHiqpA0FiMdz%2B56RK15syts7lG77Wpwj62EXAVMK5TF35b2k%2BRP7OCOseXkbhUCE7VDpjua9BHxE3kdtrlccJso%2FjYsHTlQO8Jjq4YTylbeKKF7gjUTGMrt6QX5toTvi6VYJZNcofd5oT3wVaKh9TVxADZ2GSw8nclNxPeu9sNa%2F%2BPnFpnhnVBBSMIEf7xq9A5ehY2lldg920hu%2F2ElvgtiycEaTl5qtLKwJf40YGfmEZLH7Yd3tMc6O9CRtgMtrK73HVF%2FemJ8WBb5PTMUWyG7wWCOqs5Ugdt70Ojih2yMiJIp9vojNNWxuzmS2BukE4nZMcSwnVPhz8ZndyXhcY4nIAt8pCbbwnNUreR6BzuNa0BSXfbRKlAXuokYW1Aw4UyaWcE83JwHmD0pzY10f%2B9nr9SkrnSjNOm%2Bs6Htr9QE8Ncy5sHG%2FuiNfYIYWq2NP6xBN8LgbZonXg52g73CAAyPV4jdMit9D%2FfserpSBbMpg4ppQ0ELz8ajIJr%2FmnpreIZPQRhdSZ2lHlkVb6cn%2Blkc7sRuLKTB9ziYuBcZDd4Ft0u2JYeUqpqst7fmivMOmt8MwGOt4C2F92TU2gvqyOzpHT2VOUv0PBAG9HayNGR4UUEs139V39va8Tg6TJNHICcBT8p58d%2BoZoxFWDw4ODNYgPr9zlZyUpSYndAeE3jT2etNtbRzd55BnrZChhDLhoU6lASMeO2tbaUH3LH3SG1NnTjz9FQSAl3Dz9PWsGCNdVC%2FAPYhF9aYIGZvlg%2B9sfeunSlMTFPrjBhLadJLgbw%2BiUQyvyzaEzKhtDEclzR1HnwnRYhx%2Fx5dGCeMGCeKVHWPBBafG%2B7pSi7AZxBWIYESgp6lR7CPAAvtdTEf5xDmdVByeztKhX1Yec1hlDPLKVXcXjWrNSgESXAvLbxrTJnWt9IBvoBRu4paAWdUir2ATq4e33IJORxsMLLY42pqlKmrkQObugsqMNXXmFq3sRTBks69FoJEbMdIg9OnJ1uPAQQuLksg1gzFKS0DOebXCa2Lqk%2FH1ZZDn3CP%2BCB6e9PHkHP4o%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODBY2LVULO5%2F20260223%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260223T090110Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=993cb5749347e836837fbda3a2af4efa1655e58e81bd4a0a72b16e3840df5548")

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
