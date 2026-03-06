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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_export_20260306_063727.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBcaCXVzLWVhc3QtMSJGMEQCIE0vZBS94p3f1%2BZ0KAdXuyokeRuiLwAi5ftojYM14rJBAiB7LxhPQDsD%2BCMyp14d0U3qAgLY5KSOvy%2Fag7yT6oyvvCrVAwjg%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDgyMDI0MjkwMzIzNSIM8ryjcfSDqszUr9jyKqkDWLvHwB8lDi%2BujHWop%2BqFlv3zSPlhlvRqa3GuvdMAp%2BaFrxedWVa0djthUDVBubrCs%2B8oMZb5%2Bvs1Xr7dHcg8Oq35aNWvjfeImraZ%2FQoVXNr0dihhXydg1pIAsfajdXjDa5hPama9OA0%2Fw5nA1RWLzKNL5dNTTRkUuHdvKTYDPVh9J7wdc8PLFLAQIxt6UnpDlliRdMLTbkeG3yKml3jWS9GY3owH23ViOPXiuUDBaeMtDXd0mjuoDFuF55Pcrp39eNlNbQdQ%2BPgOAedP%2FAgxM7PMiOvc4AXEQjjNRuI8bZPX4t%2FECd6mny8fvflOkCSIr%2FCjhe%2FoMIThKx5nyhDnCvXn7o0r%2F6L9TLn4iruajykJYtoUSUijkWhaSFSo5Nqc3kymu21NjM%2B69rya9D%2BdqLgDHfHCJLpFTAAZUAJF0IoITdhWOMAVjpVyPId2LIOqJL6hSQ%2BQ1ZIPMqZTV%2FoS8L91Cq4kPTXZZ6J9gAQBOosLTNKF9iG3enLCpR530VEoWz3Uf6i0CgGM7uJRNQRFw%2Bw1ovQu0p0YRZ1nACe62Fyf5DRWWSmufjAwhPGpzQY63wKqjLTKBHY8dKL8Um0ZpO5apAcFSMvUuPshTJC%2FnU2clq7k2Es3h%2BgVYKVw1Aaljfcj2GS4Jdhd3HrHGhgw%2Bf1YoqjYPB%2F7eh%2BL2r2JUcwTuBHF0%2BiqscofyZKBByYHYWxStvs4tZUWBFwFDG0ZuFAmcpRajXm46c5AbYMnJPavxDQuJTt%2BAMWWHcFELACBUsDYTXAc6jRKwwow9%2FREjoC2DfpOUKkUmW3dLJN0%2F39oxct49ykPpvu1fIjxbOyPhB6C0l9r0z8I8n2eS7bkdiZ4lGez8yB7ffWRBcpwaK8a7LGLtZ6RVHrX4mdpjcQyK4rJ3r7XUxUkFQpYoMQdJ1bodWnwyg6Rgr9HWREv0H6iCjOCrJOJqmlngf25bWqEvfbAHaQt6oPwnI7zJ6l4Ls6AbIaotitpnL2fHNyrJf6wEGYZWt8OwVW8jd6P2pbB3GbigOAo9Uis5KvNTQdquZg%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODBZU3B56ET%2F20260306%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260306T065836Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=a31565f59f4a806bc45775f03d80abe588ae887326a37b0eba91c1cd65e5d9ff")

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
