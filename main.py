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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_multi_export_20260331_150002.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEHgaCXVzLWVhc3QtMSJGMEQCIHwZINV%2Fe1c0oYTRGvsDZ0T90u6jLGkg75%2BiN3bV9by3AiBkRdwjD1xTvzLo9S1mJ55jycT1vVIjVDMTLImiEY0xWSrQAwhAEAAaDDgyMDI0MjkwMzIzNSIMpn%2BDeLBvsrW1t1BPKq0D7Uv3Z8zAP2X9gToWpd7YpYW3IwaGcDjWa8moRWObdf5GJ4XnvupaTXCkLTQ5cDFCy4JUDSjqkafLqt%2BX1TWVqgXCssEPtqTe5cGFh%2FVyLRArUwddVys2qalTGvbOjwcUxAxsVA8%2F4TjGQ3LyR5WWP4qlgAYV89PqP8gQC2RO4sgB9hesuBQejfa57nF117pmtXyCItxu2TxhG1vtWOjzsFdGbl3yjldEuqWXutHJtYpsAobnIPU5zNnS5rSatvpVOFAlxxdP7cvXtqq5avJ8aBY%2BBrXcWpuAhqXJzC0wJQLL0JCFF%2BA%2BSE6NBQhNWo%2FeHjsmDY59wfpaz1aJ78ArFX%2BWv96wf8kut002hHOhfOSXH9p9wz8AptEzeaYdSBo8J%2BBN4BSvQTU66goZymIn17RQUWbIlmENmJZ7d4rg%2B2381wtsZJ26DJzoE53HmvHBVYJBY7Ocq%2Fv%2FVXbE2IJzlab5x0bOpTx2tD5luzBJK7hjVxbUQmfQJelM%2B8zW4D1zmZboaYmavb5wMPDqpLJdnckwvYhMLPfIaAyR9NzBUGH6qKTl9Fj8g3pMVYwgMNyWrs4GOt8CLJHMlX20MAp4LJBIn6rmzS2bCk%2FcAfvrn8tODDbCxpoPR%2FFn7ivhbYlM%2BPdf0Eh8drTQ1zcIjBBk5LVIPzWGQ9J2FIofPPUiq6opCGNtLBPuMeRLT7tocq0XvQgPu%2BU6aZ3H676nldfUtFVUyHRId5UePagdOAuH3dIfR4a4eQyjU7DZfbRVoulHMHyc44NxF21ybafXSeR2LtVKgNiLUfIH6vzd6ZMuf%2BmgaeFxa50x%2BOe0MTFNwukxaONTsNhJIArIY%2Fo7f13EiBh58fXQtGCFkxwpBg8NgmML4MeoYDPgq7jjoReG83sqg%2B1qLU5AuSLlQGbzmREp3Hi%2BZE%2BvqZ6sThnDyi%2BVL6cQ4qPd1XFeaNAlQEg1SBLfSvGmaWRuE97R%2FGv%2BfaQcQgE%2BqmVS%2Bi%2Fsx2wTAufJbJ3DO%2BWnphDsSvJhIuUMKwkRd13804dMnarPLIz9KhkBGhtkkWPX&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODBVHB7CR4F%2F20260331%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260331T150536Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=c68ca2f930a7bc3d330f22c6821ef2f239c115677495d8baced76d17711baf11")

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
