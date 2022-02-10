from fastapi import FastAPI

from wecom import routes as wecom_router
from wechat import routes as wechat_router

app = FastAPI()
app.include_router(wecom_router.router)
app.include_router(wechat_router.router)
