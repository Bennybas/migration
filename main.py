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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_multi_export_20260414_045044.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCIA5tsFUuYxNGRYA8JAXsidWIQ5F50UmlXsZHtSsVoOPXAiBn93aGKE%2BQv4OSN8YfFHxx9JyOU3Yg03Okb4oWxOMMgyrZAwiP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDgyMDI0MjkwMzIzNSIMbvMjflCtc1i%2BE7hUKq0D2lR6gNkV5JHt5v%2FFDki6rToyhcpOrOSFTxHN4yqjFv3YMn3vispR%2FpRbCq00vxm42CPQPMZ8072tZqva7aU6FEKQnvdw6Z8jmmyZxV9PLEJFTs2e07m1anI1RI2A4eQpfnUmu7azEmHUIpwa4ntBewarS2LLmzXoHglWPKz5tPk1YEFAy1bjqWQ8QBFDsE8QPpiHTvgf5FXokXqZIGle8h0CK8NE6SDrrsxYfZ%2FHanP%2F44YwHdXs0t%2Bk6LzyA5HPGv3QaK4lHaSnw%2BWGgKkF2fhGsbQ%2F2H8Z6d3RlLiVc3RrhQR%2B1WPxYYIr11L%2FMre2ern0TNRnJEcNfi28bcPUimfKkOaoDOLAbl70HcPQ4s37URc5XOvQ5xYydfPhEAMuNKrlSTNM%2BsAtq%2FiY75Tw%2BdgsSaEnFLFFJJfu9tn9lp%2FkiaC8T2PrcSrXEs381aAkh4vJ6SpFsXaB%2B5xvU7bm2l%2FVp8lEa095ecysJESEsgG5GZc%2FJTgYHsnY4pt9J1guziuUASlIslXqkI4mxX8%2Fh3cBhEileM7%2BBY9HrbriHEBOmPeV2RqBTO37SBHjMJ3F%2BM4GOt8Cd2XxOxLsAuExfg%2FbW5FSKY9uBNTSBK3HD2n2TcbXEl%2FwRJRy2QqqCunvW2yy0CATaWg%2FwvrfqfuM3QXg5sP3mGvOLtq1YULks67L5reTMdLR4mt61THAPqqnIjL0bGvmmGn%2F3wi%2FLw7hvmhEn7IwANkivHmH6ZO%2BQjxtapF7PjyUgPDeVCgrBUS7eAuTrMWk%2BHlorgrWd3w9%2BYh%2BNk%2BPZonmTqya5TMHCnpFS%2Fwt9ub7EZRoKkLWdP3Zycxnttw1Nbesr8rUlayICcco%2FSognuvooTA4FGN7Bt7hK1Js932u7CN2iB493D%2Fk5r53ApjMoryau%2FocfI4QO2eSEF0weOD%2FO%2F8rI71VwP%2Fnu0tyQRdIYRXW6paheU0kVEJQ9QHJ7Etk%2FLgJvuVDHTcgsw0BkP2xwDLpm7CCUND76N44g%2BsD2FYm50Nli3gWPY4OGbufUPvtFgJA0jjOGAjIgqKn&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODBS5CZPEEF%2F20260414%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260414T142151Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=e0007b325e86fc36a415e26da93a75577fc012b7bdd2dde448b17947fbc0ec02")

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
