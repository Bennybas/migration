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
PRESIGNED_URL = os.getenv("MIGRATION_PRESIGNED_URL","https://gilead-scout.s3.us-east-1.amazonaws.com/migration/scout_s3_multi_export_20260331_172537.zip?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJHMEUCIQChCMkeiub6hNh%2BYxOkJBEPlBgPc2Ff%2FT1O9m23pX3cLQIgLQoGi5cD3G5a6DMc%2FFo7rZH4BFjTxt3ktrPczc2HXPoq0AMIRxAAGgw4MjAyNDI5MDMyMzUiDH0lGiJOhZHOmtmtuSqtA3v3GMTm6LGM7rjkVe08jxCzZxakwke6EQ4b5da%2FcDB3Ea%2BaqaQ522z8FJLMeVG3fJhiOh%2BtrLgs3SMOkGvBGiSItG5Pf62A72ehVxxM%2F6d5BnmABkc2cnTw8Z14gn3Q6MY5l40CN9W2pDh6ETiWrl3jkBCduKZkk%2B85iGu4yZg7slBrJrO3CVRfdOL1uqi7vhks1U6rcLBaLAGo0oq81gk1XoI5xHSW6NubhomtPdS2c4p%2FUBBZcn4O%2BX5deN5BbgvuStVtn14sVyF%2F%2F2ywYTYHTPX%2B%2BB0ERs0W3mXFu6rgiTKhRrL%2FrRuJIFdrnXu%2Fyiqr2PiDdp81gUHvd6C%2FUkA74uMsIty2qvij4wSQ8Y7KbJ%2FNjyCH9szKbOGKq93A3T1eyOGLD82G53dw4iSkLcBSsv0U8vYnxoRcAnNofDsKyncitgcemZqqJPnNCTSQr7MVfT4e0fWHNMcgCPqkf9ndTmiXfDnohQXgw9VPRA%2FB1lWNwpAnyV8KvORwuG0b7wr60uNpgn9uXe0YlOPoZ3t04zmyKzKFGMqV7SCVpKNUni13r4ca%2Frvm9N5GgzD%2B7rDOBjreAjCmpDHFRKA3eCUTyeE2Q434d%2BtI%2Byz1Cl3kJjAPlQ8urGvyfI2a1ijy3k1i9DcFBk0DyYmjWDs6Phd9tA6%2F9qxPrtJehXD96H%2FURXUPM0wezhr1Yyexfuau%2BmYFmLjIa6rBvTzMoAqtLJh56MZLVsjqBE84GcO36tjKO9yUk5v1zBMnNn2tWIiamqPjXT1XFNmJH3fbnwsNJJLx3YEdyh%2Fel0NQYwGK8%2BNuOthaZ%2BeP1Bpu53mQ6FsyzkYCuT%2FPx67WE1HQqO71suHAfW7zfe%2F0Z%2FKxQdm3vhRuV94RjGtb7Q7BHWYlndOi1I6NQsMcfho2H%2BFZlU2YKB4ZE6p514Yq0tLPc62CXmVfW2GVlYDrbQuabHjaiP0uCMMYIpzFT1W9e8SdEn4B723q74z1vXJOdFGn4Tq%2BjjvGjN7guEXZumMyIFr6sd4xUTRoGcawzvratv674GNEvz3Z5Ngu&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA356SJODBT7JS6SIC%2F20260331%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260331T212329Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=deacb4f06aea3e5091d1d3336936865c0b32a8dfb1f9b711ebb73d3d9f44b136")

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
