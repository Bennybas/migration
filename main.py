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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_multi_export_20260414_045044.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEL7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCIBdspv78qybV8X5g0eDioPeiKjSo75qVaATPdGdoTKEOAiAmthvgci7R9mh%2FoeOSLzJ5dgQoRjQxmsCJ%2FcaWsZ3G8yrZAwiG%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDgyMDI0MjkwMzIzNSIMbrzXJBZZxDjOkXgmKq0DMuXMBC6Yi%2BuUJ6Cl6P9bs%2BiiHmGRS%2BKOPLICVb%2BLOUocESqib2oRzfzMDmXf3xRXPUZH%2Fz1zzYkpE9cKelaOGDa3nart68ZrWEHgJVGJOmvnmL%2FOnlIBHEosQHXlM3UUPtuRPtrJXA4fPF62CzvO9aBoxtGXDPNYtGQ%2FsruBTFHE8n3s1%2FkPJJhlQCMMkEwz0G6kKvt9HZiWVl4lnPvYnvI7eryt7zIt5HLIa8wsYZNAB%2B%2BHWVBpBs%2BVKS02t%2FDSs0aLVcI6nu83utiM%2BROrovrkoG02cialjaZjw%2F15hAqM5Rq%2Fc6LSy5teje%2BMk%2BRd%2FWKQ%2BBIqL6ADV8Do%2BlAmxHEPNlIDzl2%2FcCWjwrcREw1zVNocBq4S2ETieB4cedawwn1jAd5Q6kuxXZ%2FBBnlR0xfggnW4lLkvk4I6rvRgwkFRugOloLnVsBbmzWSPMRTOPC3L9d8ksulCWOVKT%2BDZKCBC%2FY%2BMaf89PdWDP5pg%2Fgl1L3Iisc7Xwbf7ouvRtu%2FzP3TerEoJqRiPpL3NHLyP4NJh3zaoTDfn%2F7xyWlMpHU78k3yCvwnd2K6OTsVHMOmM9c4GOt8Cp7d5CiIkCzLDyjIEr3jGX4ZdUZTMUEdNqdgqgGhh6k94D8ssSpO5WZ1BIm80n6hXrHBqAMpjNS%2FszVzkZQ1dwJrzejZReMq6HDYtWfHTVU%2FyfL1HHBD05QOp2psJUFa3LF3LCAxIf%2FU96ET06xtx0I4vjPa9cIjC3ULuzMVnS7RcQcKbnwEng2vYodOBljj%2FxqJDTDSVtr6PIF%2F5fJTYV7HkroHbItVm2ASyqX84z0wRI4%2FHsk5HtF5VEsk9urz5cMxru5B%2F4pSqMOKMmuJrcjnI3uhnBrthl%2BoltAioLzE7ZFvXrVxVlgO3K6YQDF3%2F%2FEZZXxKX3dQpQL4cnJQI2L22RuyzNbOlQ0pXni%2BY8pGN0OD9IkBt1l16o5b0c8m6rXnRjs9sdkrlOk8sj3rms5LaE3UjNElJrw1Z4RSQ7gvk0uHOb5G0YBbtTmr1yK7bFRpgxRzTANCHfNqkpVn6&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODBU5DW62QJ%2F20260414%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260414T051227Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=728902ba3d4bf1b26d3d887f2154dc4946c98f61df20608c510e51b40e2f3582")

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
