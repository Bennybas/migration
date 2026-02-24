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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_export_20260224_151903.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEDAaCXVzLWVhc3QtMSJGMEQCIH%2Fhnzbq9n16BapiTHJeIb%2BywhufXHkGh%2FI0LDox909zAiBfOKATFCXrZHfXNiN7kfVA2wVqYP%2F2RvNBdQeI93zZ7SrVAwj5%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDgyMDI0MjkwMzIzNSIMLyj6pck2cjODE%2FJ9KqkDK%2Bj7PSLeIHGLRrtMqEDC29zqqyOdcQvkFsHCTMTmQdmZ96Nv39jKoe2UlHKrqu5HzDJiiXmEZ82PUCNbou%2BjNFkE1xsh4EkFfJpPmckUlfi4E9di02riwwv8TzncZu%2BxmlUgXLIsykwcQ2odS7V86O1ZNzq3BahCNjXaaW9hibtSK7uODKNsCEFqCErDdZ5TkzWynxF44zbnlMRL7umSTxkUoswwoLmbLM4Lc1x5Q%2FhIgpF6yEqeTWBzseObdKknnfMuvwl%2BmTsuNT38%2BQk6OcR5p1NNZyXr6diMj%2FUxVC1Ztq3iZXl4HJ7347dPvbf7lM3%2FkZxKP6y%2F99GoWLBHvm1%2B6JRLEzM8Zn%2FeU47KUHZg8IB7E2aA8YLXFMiK5pg892gjH4Hv933KOAzcTWl7AUACaOGiDIc7M3UCSAxujiten8uvHmYQ48tZFp32kGNPcHInQIPNsz%2B1Kj1omqCo7028RzF0rtJuszRmsGOxJa1UblThC8BCF%2FYnGuUVJIuvtFTL8ML0fJEcT8gjDlCYaayrA8nTsk9S2s6kROFzv7DvL59c0AX0gFgwlaj1zAY63wLsJb27Xv2MVCWJd4fq1YKGco7RbZAkjEMyf9stPwWVt2XcP%2FhPnb9ohqu6%2FhTQCTKbfovhsn0z8HGGrC5ObC1kgIUvYIlJuby0yBLBA1%2FpQ7vEuceVARFWDOADKM2YTOvUtfvYJF05UnW1BCdXVuGaT%2BA6Usa52mHMN1i%2Fsly4jV5eYpdW%2B%2F%2BJne4DI6lSjbTYHJs%2Fioum%2FTDTd4JGSldKj5zfqQEhGfceSzM242VJk89nXrzytoApJe6IzDVkrRRr9QhNAt7gYoO%2FEEYP84TP6tD7sAQtyFPq31sDiLP0AHW1XHDYO7xlS8bUVE0oNJzpgQsgdT2%2FSruy1BqQn%2BhsZxB2BhP4Dd9h93Y7S%2F1c%2FN8lVPJP7nQY8dOCqXqKMOFnicqKC7r7VChwvj5g59eQpdUIzkR77izdlvG7nKdcPqZLijo8AfLZhOJzBqWGDxmgwx6jv16n%2BtlS5tYolIA%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODB2FPI6IO3%2F20260224%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260224T153740Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=799bc22b80c23cb091f55047ad940d4f54a5244aaf462ddbc2bd91ff4e80d897")

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
