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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_full_export_20260218_153547.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEKH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIQCVVXchQxAe1NYqwLU6YVVfVNLerrOhsMuW%2Flr7LLNJ6AIgSiqp%2FGBIDmvHIdeXRNnX0zFsJbRrLKewW6gAIa%2BfV2YqzAMIaRAAGgw4MjAyNDI5MDMyMzUiDEpEXHFKykRVyfLTSyqpA91b7ARKfkdCIePMc6114Iif7eJnZ05KMfaiWx6VkZYPf1SDg%2F9%2FnLqsMMeUDFw2btK%2FQRQ7R9dlym3mqO2irzlrIYbv0LStc5cAyRgr6Mc9nsmWIvSxSjimD2ghBbw7U7uLyDy73czEsAFUe8aZ9xj%2BE80xxg%2BMNV%2BqwPQAjG6JyZeNysKO0PPAIWen0FJwnUbJEhHUYmRNKKmD4dnf80ELL2KkmfMSLeF37yMK5D6aqw29h3CL28qZE729hqhMrbMg06IeDFNmo%2FJczcp3hPBSEswIUd5z0yMkUI92QQrP4JkdjCAWWj7mgcn9PSaQm5j6kwwEE94wY%2BFkdgbv2dw%2FQth5mobEBnRgaZONcM3XGM5S9axi3MqVsb0Eu%2Brx5HHLJYb%2FswQ3OMn22fFQ0cADVSA395U3wTAIkczxzKJTIf4IdrhBkIlGpkfrYlh%2Bw0bz45bSG6mNJxKUXOu4V4D4MYfkHw0PVdVQZBsQxElwwjxEuReauRbgiI%2B20QDbpAcaWSm1u10rhiD5rVGpciyuGOu%2BP%2F31ZIDV8kD34dlsw2XSJWG0DkuzMKyf1cwGOt4CDkTA0W3rk76MSzgmDxZ5DJweePN4beX93tN6pVsdBUzZ%2BDTp0lMn38moGrL%2Beuy1rKThUI17P74ROjkzA%2FvIbov7bml4%2BZwxVoiNe7jPdmWQB0DTRHKi5L%2BE5fxQSY41xDQbuYiYFlokyTKZY7Wjw9v6qlTxMUK%2Bux9nEIlm7go75sdOFU0kSc1aZ03bDtvukfqYYLY6fsfryHTcvIhENUyT2LPga7fC1c4OfrsqhX8Vc%2Bf%2FeTjnLzj3qlT06G6To52kZsTs%2FL6jQiWOFE53Vl9LzC5IFWBBeUXmu5o6bA8dmahyVD6Gamed5K1OfvVCxF0a7yV9mP%2B6fG89nFubCyswbL6s5cYMeTaVDuynlHQTRU1wLg49HYU%2BIT%2BSs9mJBfAH74bdsP%2BnqxTa86oMbfJ%2F2UgQ520r%2BNmuojJmzSF8XTwWLos9hOdtHh%2FE93odEVWKsFBZcQD3s5G2z1o%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODB66IXA4RP%2F20260218%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260218T161233Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=682dc748d14cceda56b93ad3267e1c8f9d29ae2b4b5dc4b485a9dc6f1a0655b7")

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
