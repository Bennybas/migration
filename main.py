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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_full_export_20260219_204450.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQCZhaZZQatcMXLsSeSlU%2FJICpgUMjSoajSC70A5nCPKnQIhAOQQW5UhcL7nOxzOCDvulbdJ9hCu9Cq2JaZVbTIlC7thKtUDCJH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMODIwMjQyOTAzMjM1Igzt7G9mqOMcrePyvIwqqQP0g9WaDUpZPknsCIGRZiwbgQ%2FANxD%2F25whSAFC0mmHvboixG1DaGeuLkYmM8PQ09UkX8Vc%2FO2%2F9e475Qf5%2FUPV52n2gbtwOPIYbylt9qa9vZ2pgHnvSoMzGLRTLJoPpLqFW2kBAKRzoHy1yLK1p1uB8lywL8N2W%2BaW8pWvELCZInC5qpd0QGVQBawQIfVxIJTP0sjmmDjQ3%2BcY%2FGc4wb2wgs1l3ROcDko1oJMe5PTXuA9UTXsGv%2BNL1HhgzgHgyhw%2FQSVfDF4IQzO854b6BMBfjreBiRNJH7GMunP9suX1TkUBsyNiYfgldQdHySkJwz1yD2KeaVL3W2s3Vmzz%2FKqZsVp%2Bf71EsQkdHeB98jbe75gTMIRcVs085baFmJnIrNLdqGK1S25pWws8d2oEwRoZ8AkafcNFMLcCmys5SJCJr2HwbK5EPrKBChnH42weXSLlzMDdLWDVLiROjcqjKu8juf%2F5X4iRBvEIJ%2FB0eSsRsA7kJ78Pol9oj2u9dno%2BsyDi76HtKQdKHJnmsTFm0hWCcWTsEX1ctS2A0DLOtqJblfNdHCf1OHm8ojDDieDMBjrdAol3TV%2F6DCjPvvD9wCg4Z7nnG%2BfDyKL6DmfmhUktvE85TsSgg1zbzq9HhV6yY1yzfjtXSiQwwyH4nJP9Ds65kZQ6JTZP1IMj1HfLQqWEjGzs9GBk2NYtcM0g5igI45G7FceJU95VrRtBdnJeXUQkFFK4ag%2BfVFrdJeB%2B9oUxMzu8HbnHmeI%2Fzfx%2FQFt4W1a83NtqfSaRx2OltBL2TphqlYItMhJF2FjG0xv%2BZQ1G6B3wLyHcNFlVkLLFxxv1%2FmFjJCvCxirjv2ssG3%2BQHeijuIMUVLuMZh9MprfluuLZlYmIhTnCI6pvRAGYfNsoXw%2F6i1%2BxhSB7Pf8WM6s69mrnXc31CM3JEwGHtaI4DM%2FGQSXz%2B23Yr9WILUQbZzZJ76D0MYVkmDfCxE4m%2B2zTeGDywDBl0vsQSt03mtsDe8v38hDsu3njHBH7pzvWrVewYTro3f8%2Bh8NDPhTPOQcqYec%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODB3AYBVN4B%2F20260220%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260220T073619Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=8d156a873998eb2111ef5a2d45e6d7882292d4dbdd07964952bf1e4614f17ec8")

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
