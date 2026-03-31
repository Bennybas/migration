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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_multi_export_20260330_135512.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEHEaCXVzLWVhc3QtMSJGMEQCIFhsCU3foYKNmfRto%2BG%2Fpaxf%2BLKiUW9WtgfJlV%2BZ3D%2BSAiBfpuof8zvlNt%2BfbVSNvshvsZQXQMUQgqmeAVENpxqNqCrQAwg6EAAaDDgyMDI0MjkwMzIzNSIMTimT74BX9sulu57KKq0DuBEGA9ldoGyLyKU8pjtLwl0jUp2rWjUPs1YRkajSwSHCm6DKDwSM%2BCD3Usoxqthb0FYZbSSZFTTNbwp4513uVoZYpYuGgceXk6rhtgabrAlN1Z%2BXHTSIDeQDcotHVo4oIAlmgYnaaqsI4SXVAg2AGMGbi%2BTF1enQBOJdp%2FFADgOF7897o2ajdV75da1wBNYVYnpKu0z0S5v1FNEzV2XsGYivmb51oHUd3hxxNQgly7DJ5AmqrR4T6BGy1WysK2vJQM%2BpZ638CA2gSxJux0qItcW5qBN7FN8cQOYn3F3w1ZjqXDqKQ9E2FdNjiks4YUyPO9uFRSMXm%2FDRcX7MAqVinV4zx9OQeUpQ2M1MCcwWo%2Fq976izIRUYsLPb4VLLBs5ZJF%2BxSz1eRFeMY3DzwVkb6fuey%2Bv4%2FMtSsEI21ki3hE%2FeYGXppVPFqzddFO5E%2BDwU5qwjFRizGyZGnWWz2BVUkiIvhwOghcfJkEo1tT2yual8emv4IulXBGhpIyKIDb3mmNN3lwub%2Fw6eB%2BUlVfGuukarrXuRaKmdPcbnkkitacaRLPIY7mOKbN5aN2O6MNyWrs4GOt8CSu4xcuT8t%2BlIStynofOyUDeB5o3ifimkYyI3jBGqe5b5J9P%2BzJoDQWNuf7A2Bvi4q%2FjXPFi5xm50GxdWTQl8Yg5Siyswqwk06rxklUNlRJPlmjNkMF%2FheuDSttOaVWNxUs5vHrSGPOzuWKGSgB2leLt%2BC0KOHq97w1YjmINiS8xwv1HFDK8ayPIPxehFf0M88fRrnIQ5v6nnbjOPMqt7PlpYDWinvKfaeIVLDge9IRdvQOlug%2BE3jSBhZWyNYsGw7ijzgHL5vqYg8DfdkkvU16oVj8LuyT6%2FjsNWWnO2AtaTVu8jVFf%2Fxte0oW9Yj6UcF1wG3%2BxDpxs16j1tr6Bt%2FsNK1M1NSs0XcsV1m8iHkemQPXN8LDPrDXlGRVmArTzlslvUrrjAX8ugoa5pB4FV0oVpo7%2BjeexnAnilt6NlCIvTdnD7RSJcdEVUZrWSsrf7wuaMB9K%2BMfrZjySWWWJ4&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODB4Q4TJQH3%2F20260331%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260331T085307Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=250521a5e8a2e84de3611bacb7bda2fc1a142d0f77458eca1ce6b9680aa71e64")

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
