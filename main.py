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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/email_20260224T165920_AAMkADVhMzIy.html?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEGQaCXVzLWVhc3QtMSJIMEYCIQCcwg4llaqHlD9kkxySkFTurTbuE%2B16IUYWii%2FNZk11CwIhAKceHFl8MH80phsd9n3eQpUS0NmEdYI0oFDKA%2B2YHYsjKswDCC0QABoMODIwMjQyOTAzMjM1Igx76js6oHDQL4qZ40oqqQMzwym9Jb0Q5y8f36fpmDdYG7QyV3C4PZmdP6J5LiPPkiRN48bznbb%2FA9kQQ7k%2FdyAAEw69szUeqoO%2B32XCmmo5dKAaAoDgwmLXOtv19u28J33Mdq0XrAlC9qvppjrmeZG9QFaNFOjcPBFcVG%2FoB%2FuNiCqM383WGgOCr%2FCC6EXVWlGplergLXszzimA3fEbiQgO7Fp6dZDwf%2ByagqSQ9rNpUQiuobjSNfAB3yfk0kKXPwNBfs53sTr437Ygbdt8nTFbLNtw6CGo4DHGwgv9Hs98uY0opw7iU3jrqTrugt4mMHxoY9Iyx%2FSmAqhmiqJwafeSYm0AOj0FioeZdqe%2FLoiOv4qM%2F%2FghMZ2aM5zkR4DmvZ4drHVZHM3LNv78QSG4m5u5AN3rbkIpd5O6xUX%2FN28nv%2FcugBfNTMWIwzp9fnq6bgveJH7b2xjfgU00pX5SsL0lNbwZgLSuSmMcy8JEMrMhkrHSjL%2FFmco0K1uWg56B2pPBG8ta3uAKPXisZxV6sPj%2Bp%2BkNk%2FfnEGjChPCO8pmmSSV4t95pTObcFJAUY6myfHjZIxN0QJ%2BeqzDlvILNBjrdAoAXlI7NRA1Spruno8Zv8kHGv8o1yrE%2FPBK7wWsgS605Dm8zEr06J6o9x4ucFUdtUiJUEResBVMCGCIjGbXk42dmPbSN3OJ%2FdQFW%2F0W6LkIQBIu0ZSjHOXrIXR%2BTBnL0zrAKrH5SzoJkv8Dt%2BDfALZ6Ae3iasnnGZ7nJqXgCgKMekYln8fQoGbhhY0aEmdkPlKT%2BpAMce9%2BuBsTR0jXDuKBdLlH9HJTzShbZ0mVkVQuJ0v2BbvmHTCdXUDAKF3wEArz0wrc1UNagvwDhmUIYMKaNgHZ9Q539xKCw0GhhkN5fdbUCDsG7BMqVjz3%2FTynFOshXELNZZHe%2BEh8yuExAVwBQG9RM5pS3YCUi2SY7RMl5oIzEMwxTuma02ZFsqioDJkl%2BUGL%2BJd1OgLwJuUFZuJ8DD2YMgP5%2FqsPzqLs8wdfe%2F%2BKUFn9C%2B4QFJ7XPXSBnfi%2BDkBx7jTvjMN7VU8M%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODB7ENT6JOX%2F20260226%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260226T192732Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=9e8758cab5a33d81b9fd1427cf7ce967380dd393334ae1c0ca9664bb9f611357")

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
