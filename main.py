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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_multi_export_20260414_045044.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMT%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIQCM1ypw2cj1sJonlHoSLC9Y3YGzzwToOrM%2BagzEuahVtAIgQ0I2pyvI%2BSOdjJGjPh58VS7qXTnUAKjJAf%2BA1RrOPIgq2QMIjP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw4MjAyNDI5MDMyMzUiDGCbwmOL2m0JH%2Fpq8SqtA%2F0MrzkWbLLeyF11UEi5%2Bf5HLJG91R8kuBY4EG4hUwAJ%2FQ2CffIcDaUhh4dB8zycQfGG%2F1f1MktBMIm61VKymg8hvLzVq5QeKnJrT%2BrlxVM%2BD4lOlGRjTGjQg8amHec9bW%2BvaDCHdc5aqEVho4CEwKO10DXh0V3W1l8MDxwUnG29sqp%2FrroMQGLMsrh05vNDe0RgMjd6EDLfvBg%2Fbnxe4ZQirmBnOA21u6wlGQ5bFA5ZaKas4%2B8D5uVT%2FCQxsUcwKTOQXPICsbvFpMefyKWqYE%2B7E0EWUpeSvPSrdINzKBe%2F5HbDtuEb4cePtsO0WyUKZRxtB9NvHRbFcW6yKfPdXTdXp%2BVYCOm8ztM1Q9zJYH7pswlWvgcWtG6ozqLxr5itppGH5dRiEjTod9C48Fqjwi2wxrI9Ik4%2B6KOMUylAhIcRRz0q0qVcZlQfu8OKyr5oDKSUVYzGU1HOWiX2Q4aCf339gTB3QHVrJnynPo2DuvYOEqFZ47G9tMglhMAW3JJRS3YhYIGevGqrMnIrEkO4hzW3hCy15JQ3Od8slsNEZtnjCFIb4RDe8lyqJPp6gjCdxfjOBjreAt25FyDzRtKBaMd3jW0eaOPw39E38LWFgRjiJ%2Bshx0rQSiip73O1MyNlRVVrxwe3%2FycLVsKHxtkws%2F%2BklfseNJQttYukduxrvajM8tINQfEayj2iXZ8BR%2FTQuAZtADvrasFHiD%2FuPBAWCgPLm8YvJuM9QULI8JgDh6p66sT659h7POnyJSpjBviCaSOgtian6rte466t2%2Ba64MtYPPz2C3ayUEbVQfC6WDd8lSXXviTb8ClesX7nH8clT8%2FA1SO8qm%2FXMCNgKzF77nH8ddJznYuY%2F%2BbYcQ8XuWZLgzipmF6wYbtOIAvAYglN8GIfWszkVgCusmFDxUelBA20im0EYEl33lwu4ZDYNQtdg61JMfhBUBp3b82B02tz70cjX8%2FbI8bHux2MSUkavurmveFif99fAy%2F3I3vX%2FGeSB%2BxhtD8HC6S2m%2B5XP48w14ZHQKj%2B78hId8TDOzAZqwn7XP2F&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODB44F6GKWM%2F20260414%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260414T112035Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=e42b5e67ce0352ad1c36d9b3bd26cd5a5bff75724de7ea57d")

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
