from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import zipfile
import os
import tempfile
import shutil
import logging
from typing import Optional
import main as migration_service

app = FastAPI(title="Migration Service API")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"message": "Migration Service API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/migrate")
async def migrate_environment(file: UploadFile = File(...)):
    """
    Accepts a ZIP file, extracts it, and runs the migration process.
    """
    extract_path = None
    zip_path = None
    
    try:
        # Validate file type
        if not file.filename.endswith('.zip'):
            raise HTTPException(status_code=400, detail="File must be a ZIP file")
        
        logger.info(f"Received file: {file.filename}")
        
        # Create temporary directory for extraction
        extract_path = tempfile.mkdtemp(prefix="migration_")
        zip_path = os.path.join(tempfile.gettempdir(), f"migration_{file.filename}")
        
        # Save uploaded file
        logger.info(f"Saving uploaded file to {zip_path}")
        with open(zip_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Extract ZIP file
        logger.info(f"Extracting ZIP to {extract_path}")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)
        
        logger.info("ZIP extracted successfully")
        
        # Run migration process
        logger.info("Starting migration process...")
        result = migration_service.run_migration(extract_path)
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Migration completed successfully",
                "details": result
            }
        )
        
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid ZIP file format")
    except Exception as e:
        logger.error(f"Migration failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Migration failed: {str(e)}")
    
    finally:
        # Cleanup temporary files
        if extract_path and os.path.exists(extract_path):
            shutil.rmtree(extract_path)
            logger.info(f"Cleaned up extract path: {extract_path}")
        
        if zip_path and os.path.exists(zip_path):
            os.remove(zip_path)
            logger.info(f"Cleaned up ZIP file: {zip_path}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
