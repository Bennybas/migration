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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_export_20260224_151903.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEEQaCXVzLWVhc3QtMSJIMEYCIQD4d%2FRR8%2BEpC%2F0qJsOqL2sUE2ssoyGApzY3HmamY4Z34AIhAIpYSyBT91pFNjMPwc%2FbAaVjxLO%2FWCNuEqIIuvCaFjgXKswDCAwQABoMODIwMjQyOTAzMjM1IgxIzXbXavW8o%2Bz0CzQqqQMZtbqEvmRVDHn1s9VPbUlouas5RVR6ApKe15vcQjlVlEeSUWajH3sSwhvgcgfc8%2B3Mppmp%2FYiVKF3BmgaD1TVcizOfK6tpc5CGyDWPIzxpw1Tz%2Bul9Si%2FtRYq8FBWZg9ZGWMjq%2FqnuXi9fIAg%2FoR4dNf1EmVPQNPhMHi%2FqWU9lWahsgijGg3h1vc3MaqVFF7OHWZHNz8axM592wGfpUPEtAc%2B71VoN%2BkRR9Qb61lJtR9fpNl1Ghk2R4IJ01BU4BPvDUP5vylwNcGKRT0tFTpggnBZ5gbi19QOC%2BwV7VX7fyvMigHdAX1qVi5Aww8RIZZV2yPQS%2BswHi7h2iSKYJggxwW2WSIz0qSsN1CgETom5wR6DPgsNqSr0ELzKPcGFRmfYB8yirYWNGhiL%2FiswBWu07Oqv0t36%2F9At9DvNn4M43XSKopnFNlM6Zhh7ZlXiAoYXebuDViDg5aJHNeNBSBekuofk9afCcYylTAPVdVnSMlW9UZt9paSQk%2FTP0NWHYczCZEmn1viJn99mQafHxJHfyOnKWMfmLX9%2FnhH8ulQ1YVbxH8JUsgF1kDCsr%2FvMBjrdAiGiQkJ2RaxQrRm%2BZ0VZ1FTsOE%2FDPIzUDE97bGzIs5gLIc6ub9t5ZFHtup%2FOItjxNeAu6k9zm0DKD9N2bNIv6rgyDMX19mJgvX3PiVntFM%2BwI8ZZRllVW1U5bHdlCFFJR4ULQjfoLqNqdn4fxf0dhUBEjq9R6YqZC3ZKhsWQJTMLAXbpVRo2NtFsfn5tDwwLk0yqjXc005tkB5Kg4AuCOhE6X8rH9icLw9l%2Fo37X8sZOinOFhFoumq2Sy2stOqmma4OhhkVG74RzDSMTichQoG9wI%2BRbVVZydbavp0gFPZsi48ecMYJTXWdvVamgLvGj2TEaaqoZ4Cb8qMTmfKkY0v6TPg6MjinHlblhELI8SAzzckqKoejny4BPc%2F7kEweT1IXqDozx9MhlWQd898G3Uoqxeu27rIc3g%2BcXPAQBJq0xar3GJzMA%2BW03%2BsHOqS1G7cL0427wdphFwecYrOI%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODBXGZ7FY4Y%2F20260225%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260225T110652Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=f54832ddd2272e2c2f46920fffb2a0c2c62a8f7539a2b6941b8922415853dbbe")

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
