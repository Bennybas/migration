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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_full_export_20260219_204450.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCIC9Jz7M66VluSlju1Qzvs4vOnaOpqXcmHtcl40X3OEfLAiAwUZFU5hDW08Aa23sodjcet6UyXLn6Xjlkc40v9DoTjyrVAwiP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDgyMDI0MjkwMzIzNSIMx%2B4J103TiXb5HGLNKqkDLNFdG7BtXGVmfwacPO8jAIZUMazwsTKHLHn9BpWCcZj4LzDkdIvVOCsSMa3kjmcfxT%2B0kYW%2BphLEDjP9ecFdDAR11SZmyhzWtV%2B9M78Gn1NgBdTcGhKFaSbS0HxqLdCPk1lj1zVPxigfzrioguUnuHfmvE2nDMBZBRov0bz%2FkEYq7pvcC7mqjvQLEZ%2F1f%2FI9aI0s34Zps8tvJGPUMNouNnFp4tCjpsDRV0wzPocvMFSIITg05XRDonNsk7Xck1tJO6FMDgYc5FVie%2B8qef9KD5CeN%2BQQezsA6yPgvAbwVyd2Q4sem8DDsA5w4ykKFmagQYFgIvkD0W9zIgE0COKTRniovqZ5he0mNhQrlDEdU2DiJIhCnrUF1dBdOMRwjHcatVGpjD0bWfN0pE8%2Fe5jQAMhZk5kdHuwbuBzk%2B2RcVff%2B3iNHvfHtLgom8ayf26hvCv0TLi4fFIfexZAhHw0Nn8ZxfVo7aJNDI%2BFJZHA9856Zl%2Fwh2EVcXh9idS5MOyJntPaJS0vCO8d2QHv5R1D%2BuIPxhaSrxy60VmZAgay%2B08QJozslhtuE9eYw%2BbXdzAY63wKRsH5jdXYn7rFiMripLR6EyD5Xq%2FFpng6p2rHHMDyqKw1u4%2FfoobO3dyCtvlu%2Ftb1H60xzhd5QcnY2zY9stQCwHb6mSY7xIRcTBIZs7Q3PQH6VNK9KKlh%2Blp8FylggweeoXu8rGpovmNgQer2fL4ik6N%2BC6vjwMS0I4tGJ84OZfC4LfeEgRccG6Mz9mG4r9FLGOkcpLFpP%2BvB4bj%2BMby5Mlpy4Ru5eBV%2BQoYlNQw0XwV6KxnEAvphVOqPfk8EvcAc%2BmDMt6XdHG8J6MziU9AezK3%2Fr41IZLiR8EzVIdl3AlE9GAQIv0Csqahr%2FfbS5iX6jMk8B%2FTefYm7Z0BjCyBorUJt%2F6EllX8JnVOTyP5BRNkAgBdd2S0LuRn3lstVy8skTxpiwCxMwY8tKVsMIBXt9I5N%2Bvhjz02OJZZVACXFDTxxjy4kEK9nFuBhuw8OzdluvZCwLIEKFWwTDH%2BUGhIU%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODB45EODZ7Q%2F20260220%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260220T055303Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=3259e5076cc47652cb4fccafb75b4741d50e84c537f9c9a62215e5e09d72af38")

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
