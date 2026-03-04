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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_export_20260304_073739.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEOn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCIHSxHSQEQoJN1mFe750HsyscQHjuvJBR6G%2B4KsZLCjTBAiBhifAGCZhivi%2F4VO%2FWWgq30bYYEQAfhLrxy9yKBuL63yrVAwiy%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDgyMDI0MjkwMzIzNSIMj2M0dRD01b6R77Y5KqkDfJ55%2BUWyHhI8nbW3Wjbfsm0Q3sFOrJWkuc08ojAod35xDTJ%2FvnmPU8YWpKJqHqIn52MAheI831PjSutdnSMBdoSfsSCiexYZx1B5bCijJCnEyG2Usl5U%2Fx7wpi8%2BYOJbHFqWJOaQf%2BX5Q1kH6DRwrQDp%2BW72j9Hnilny94k7715OEbh7VtHGkIvu2lLZDQbfXoyp18Aa4V0KARQVqHXuFb0zY%2FZEiHXwkEoud1GOgnzKJVoS2fAnq4fLE9Vp5J9x5i1Wb3CpyWsNwaRM34UWGQelNY0r6d6%2BC%2BZbXxIiIW27XAypoaY3CUegznM5oPqB9ZrCAojvPzYOpU%2BpSzsFzs0QSNm8kioZQgN01DTZleo9xkkcO4bE8cyGNtNbKqUkgDJIP9vDsD0FB8ceRlNJYlPy7FB%2F4GxQLfI7SCjjHR%2F%2BWkawKWWAHhHoKiFZfhSkCzaQyRL5pkbjDqOc0XYY5MS%2FZjNac1HZYeOBnWN03nUK16GsqfnKRZXXQDU7ZoBk1t3TyhKDMyV3mJKI%2F6IzVKuC63pkBvPye1JrGzXyqGBNXDUZYwKHe0kwjqmfzQY63wJq3Uxx2afPfjek7xCa8mv8p3E7NEz2rMUNVKci2fLlktzzTE9nSLhGK6QjEmnm7mdToDhhXnqyKVHtIVDdExqQKwj5ffBKq2YgrdcsLhn9wI9Lx0hHe%2FdluCKv%2Fm%2BFB%2F9C%2FOVk2%2FlPQ1W6BrGLTNqFTx5Nm3Cs6PJGeCIYVqu357XkDRPfTKPtcOVIGt6K6tZomSZzCDUSOogZ7JH%2B5KkXxa8A47T47C37dC5hfUpEHDz%2FiWMYXDR6a4dd7WqQW3M8eW1oj0Ni05QLTMPGDQ%2Ftd6LsqxZvypw%2BfTvxPtf42jVDZbxTXicCWm5ECyaQHINnNf2BAA48BBwk44NBIAsPXH1Qo1oCh940yw0B0h1Nh%2FE6wFHA%2B65YWecEcFLpWXjxkDAxCcYXh7DxBWCw1xF%2FIaFBqSD%2Ftf60WkwnCiTMx%2FOPxh%2BxDnSPV138BotTlBrTNsasZtsXdclqkCouhiA%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODBRFA55O3G%2F20260304%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260304T082624Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=f925180353f504709a12e8440547ca48bf7c34bbbc4f0c37e9e372efd41d3d51")

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
