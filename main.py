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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_multi_export_20260331_171454.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEHoaCXVzLWVhc3QtMSJHMEUCIBfz4siZGE%2FLGMl9k5wWZzE8k5SmQkvKi%2FzN2MXlvHELAiEA%2BwlXfl6NLGhSpX5ES3%2BgdKfwLMdkTzXTKjGgVkZZiwQq0AMIQhAAGgw4MjAyNDI5MDMyMzUiDKLoe5E9yyHwfBdndyqtA3D4VlCrWgx%2Fkfj5wV%2FHX8cseGbibpkRb5G3EZaGejXM0iR8PTp3SMkD7lvj4tBHWj5mA4UuBQT8fT%2BTeyoRAapIRh6m0U5Gx6N0flny5IMTTHYjhzdxkQdKtwq2VbOOfcbseZX5DNZyOEtldu5z5dwjbAf%2FlGsJwWbOaNeL6HC8WGf%2Bh4yZuUOznSycoPw3LRAYJtrbkzQWLWit9vaavh99Z%2BhTNBMeywUTn1FlEIXALofrFUavnE3LEq%2BZJ5l6mhrc8OFLJ7hlIkz%2BsS73N3YR33L9xLa5l5U6t8b8NGcCzUG2WDX%2FDNDD%2BqKNc1Lc1jVUGgsXPAzjTCu%2BtkoC%2F50Nzo4jXx8UuyTWa%2FyXkOMekO8eFdgAacXvvDRnJDakCP0reBqJ7GVpzZk947WeAlOqYSbIgYQHGhDYvi%2Bd2txKBgot6vbWkPodOqIr2F%2BOjcMyIn4FtdqLvWCXV91SC3GDy6rlpg5jIJ4eaF32mJli3o5KOAsS7lYvlp9iSakSNGEZZ9OM7McrikjpQ4ExS8qQ2%2B9kIUP0183uF7m%2F5Mr4VZDIjEPR5vnsRAr5%2BjDclq7OBjreAhEqHvOljIRzv4XBvIeXojf%2B%2FKut9ZRVy06ati4bH2klXOHxl9wUnx2IpDmH3%2FeFJn6qyxXZkigtHtVaue52uNNDh%2Bm96cUFjnGOENSBtVc7Cx%2FcfYMCfkfIWw1KtB5PzHboYI4ozFMbwub93S9z5iHJpZk2CCGksIlBDJBPrNH4jElFnDZDJeQWWsiyd90UZcAcN4k4Z6I%2BT6DeU3GmLMOrXEZ%2B1gSt4Jftow9jHOxMHb1JEhsUA0lSC96bGBzToOPpylv5NX0P5%2BLj2BFFgBfjMqDRQgumKyEkJcA820stKMo9eJtDbM6d3kP8xQ%2Fv8QSF%2FkzNvMcIUpXjcn9x6P9DZi8NNEQP%2BD%2B2LXbdv9%2Fdq3%2F73%2B2A6m8o9rVHVKbclqoQIIanCe82Vp2eiLn3q8Sl3679Uol7GcGDCjY4VYcz2%2BjWi3%2BgZ054%2FObploCKdcCZcXOWvA4m9wOUR6Cr&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODBZDKJIHBF%2F20260331%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260331T171846Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=e52ffc483bb5fdc953acb8d261b2c4451bb59fca845febebb68c19a754de1a9a")

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
