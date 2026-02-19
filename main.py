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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_full_export_20260218_153547.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjELv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIQDELlE6pWQVg21Ev26o7CsM2U0g7JTN0mn2FfQ3cccyaQIgCuFQswDbodjKG1T0Cx8om0mPhRjwODq7TWQXkuS%2BoJcq1QMIhP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw4MjAyNDI5MDMyMzUiDDoosdspNiMk6a1iSCqpA%2Ft%2F6xZJur9l7hEysEo2pDaSZ8wRxbboo1I8pJLQ%2F0ioVoce5vdqqz5wc7a%2Fq4Bwnm2uUNRKSAlFVejJ9NO96iIs6CbIQCgXBEdKJBOVODlvfbsQ8AEu5FCzVVxudUixMMsjZqO5ykORdNrbUgUqt7Y7fXQjBuqpgjDRfbCLkGbAIZ9jo67dwE3yKCGLwylJJdi4yY4PBhwHlzmTUwE5LLBKFdB6%2FqEDdlkFPYrvqp4GO8WpGk2ApQEagg4nd0olzkMWqEcFF1OjILFfS0a7iSZyvWWJ3xnak%2BB%2BH5qDBujjxAnIAK3dNsKP07hKpBJwW%2F%2FwneGs6D%2B%2BIrrzU7imaCYgdeeHevjBLd%2BEl%2FebF%2BaTsKkShumUz4mFxlTRcoBixe2NQgBHYZ0ApN%2B0fN6Q9M6jCISav125IkzGd67uLmz8GL%2FKGtOAKCqQYW3ezOiTnW8MjsVeOGQ4Pl9Dct2Dr0XUMac89fL1WinpAhNZRB2Y%2FZXkPxKO%2BTAsGzHU2TtDEb2vN4h7HzLmJBI4Iu9H8cwQ4vENiJpLU7HQU%2F89G5E6NR0qYLKtlyUHMPm13cwGOt4CY7YWkcwEsTiG2qIUaYVVjcScwyeeqtQN4aVJzdpwArQP1linZeVEmxXFro37vjLkFvQkA5TKYsa9WBE6dK9EBcF3fLoNxvXpGJkGojStSo0q%2FJESWSd9bp6UQSBi%2B5nLHZ5B%2F61Wdojr9%2B5khIah2XtmJc99Ub4sEzY3mgu6BwxHaFjj2UEkytDS5ale132iQX2NHSKI%2FcPNhOlzYZ8u0ZMDHMkcEgKEGXbLHzcLFNjrppzQdtYHf43wSDCnypI%2B8rkQhCJxWEiEE%2Fi5xeHunNGNPVxR6HbPy0k8R0pqmXtfctlmbROkmxKi75ZDLykUKFsovvk5rFtiPzjGkY4fE0Cj2F9bJagkUVtOWK359AKwtX1zeqBN1HegFLG53jP8OgpEWumZJW2dm39gmjBQqCZgi7V6cBks9qDqWeFtjy0XbA8KEVpnzHb%2B8FAfY1nLdmHAUB7aavKk0IiZJxk%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODBSTKA4QYK%2F20260219%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260219T184954Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=f7efac6f035ac21b5a51fa36147e40ab0f97d20955d18ce9e96d47af3afa5a04")

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
