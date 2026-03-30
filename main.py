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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_multi_export_20260330_135512.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEF4aCXVzLWVhc3QtMSJHMEUCIQD52F67kvw4PkPGEK7%2FYj7sj4MorfxFGLeAHqtM7uhrnwIgcPsjMiMAwX7cE5bIo5zZEJ4SrZvOpqh6%2FbG3ygZ8Kpwq0AMIJxAAGgw4MjAyNDI5MDMyMzUiDPxqCnI7sY9mr5jQCyqtA5FGoPPDDwPyBNg5CqigkGgt6qmU6ZmczPeSlEcA%2B6MRU59CnPPci2LiyDw02DMDWWVzq1iBuU79TpUD88WZ0jmt43D%2F4JkH4Z%2BRJcTTHg20ceqSnSwjO%2FSEP2uH7aEgr7Lfy8szKUpfa%2BuFhr8%2B7oZidePfwpymtxEkWHwcTXC1qjthn2Q24dqb1Ws8cyjDTfmLHzvqswsq5T5YPdQMsJ2ZrAYMVkD0S%2B4tfMNF9zPdTL5vFhE7mmQvV9RstT%2FuUhC1W%2BBOaILfJwhnoxP0KzfZFMxQyMApDr5SnTqWV9ZEIftAMon4HEq9kI9lfLlj%2F34rUjdw2g8J0l1qjqYAMdwJFcGxOW4pZWzogaMUt4tQXNRrsRU%2BWnlclYvRhzOiLC2IfjHaqEboKa9PuWtEot4OORxWCE88oqbsAqG53AUrE3ANR7QTtw7egme4JFddqKBsBAccJFUtcmLDzT1ZuRhUTac94vBEc09BSgUcPkf%2B7Tc%2FijqzFysNZm7GoxUg5WLAmbBc79jXZ7rt8Tqem5svVy8WRVMJUjLTHbVjLftBz2muOdXm5Qapjp9OvzCmuajOBjreAv3VwVWdqIuoqPQehXb5FLjV%2Bn82w26HvoYN1tCK%2FPRpykJr1ZBhjfUJVjiPyAlEgHY0wieU%2FSNngVOSArcQBpq0YD7s7AR6fI%2BNphS3J3ITWizGhi6lzBZ%2F1O89YklRDY5MAJgtJvyp7yroMDcGxooOWpXAPjaYV%2BTacSscGZIoi5jsWyk3dkGd5uYezO0eEWx4BuAJ5joL3XzVruHnABQVB0ktE3HmcC%2FC6khZM%2ByxdqxoeHskHLSHB82RR6NesvjNeNuYuijw0SVCef1y4ZTfreolffdbypvu2VEkkMmyS2oaqJJ3WzIh%2F9iSLcJMGJaX8CwHBPQALQzOUtg0CGMZlAQxQHmZGCywzlMpaoaiZMrNSVfaoQzvRkgwwv1E5TNLf0u5jqDAfXmIQBAxqJ0kagpGD3z1NMB5SZqzN1UNsBnMzKxInAU9vafElw3xeeGa1ksfmYXXWuNBf%2F18&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODBTLPMDY7M%2F20260330%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260330T140214Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=1cfe9141657b298d0d424e154d92e63bc1a7b94921e09cce7cd014a981b9d747")

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
