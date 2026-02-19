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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_full_export_20260218_153547.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEK7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQCwcuWOirQGHNteLOWBeXOUlBcoVoeV0Er59ndwYs5mTwIhAPcbybH0TQBuNlCKKfVMZil1sHOaIWXt5Sr8sihG00xDKswDCHcQABoMODIwMjQyOTAzMjM1IgzmJml0naACtWMzJ8wqqQNNG5NPAra3XGTo4fAfJ9DtNhOh36VvCdOqrGSLKZaiGgGq7HGB2hrghoEfRQes4dRYDGxbSSmdADb9nJPHsi3Dc14mOT%2B2XV5RZQ9FqHV9kuotLPoVOUP0dh18FoBKTxbqLD14AoewOxOOOko6DNodvADSTqMCf%2FfmODFbjaQehqoJbUHZKEFB7h%2BVRP3AUcZYZ9ofS321jzAwHDxebYt0pUk6qaAiRAQtpYv2zrWF%2FhPKkO4SObmojYSZ3x1OEhgbAuYCyRBT2zFrXte6LgzDUGgETRKeQ%2Fa%2BZEqaGdlywkz5ouKiEYcTXACWiIegonvMNdxnerb0yNIoRZxjuBDSZmNIPCV88YsPD5ueYaL4RD54pZmMPfFRIurW%2FyvO8IhyElXq%2FfdYgIZvf%2BhUxkKN4n606Ugl5mFc%2FspBSsgFuuuk7YMVGvqeYlDDjxiNTGNwCg4qIAG3N6fZIh9B1vziFOtEM6r0JBZdqreaC8Mn%2F4rjRLtdzq12YocDfs%2FtTqIUF0eWGySFGwNzw94Wx6JKgmjDKXdpLIbqF1ZUWGobL4kl70J%2BC7x3wTDCy9rMBjrdAtbyeXCcNl5sVUM5JLQroqw2R7nsZOZVw4QM5Eh9zwboIXwmW0RaU4smeR7xvRGGgV%2BRxVMb33RuMksXbycL42DXttnt4bhGCObFOaXG49gFWGX8atI1XvsmYWXX2Ou6LFiBaA162oNAP62LsHgca%2Fp8B0VDn2IRw72Pw5T1uFjTwjPL4v3%2BsslVEN0i7fkVsYtmzCDLRm1bIdBHgqTW3EM2pl0MnDz3qq%2BwgZAGf8SQY45Uzub2H9a3vtN6qXN%2BC%2FN1VYtjpMy3LzXZUWqWIJ9uulCjtMGtT6IcvyI0ut8gHb1SIPn%2B%2FCWydCohnucQykNwHavZ5pPzeuckDEqDhBujGjUYUUEAFrepeml%2BhlXzuvGBPs4qi1K%2BaXBM%2BPsQr9M7CT82xyZd7NkUAmG3CSJi4Pcff6OzYzQYkF3HmWxyajpJKxteDFX4ZcAYRwuQM%2FJRtzLgAUzMgjpephw%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODB324MEAS2%2F20260219%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260219T055654Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=6cff6f75f5e9fc0276c0684065c751b4a268b73a6c899a9beab9564de0e48d57")

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
