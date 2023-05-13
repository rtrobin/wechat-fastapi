from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import base64

from wecom import routes as wecom_router
from wechat import routes as wechat_router
from utils.fetch_vmess import fetch_info

app = FastAPI()
app.include_router(wecom_router.router)
app.include_router(wechat_router.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get("/v2ray")
async def read_root():
    vmess = await fetch_info('vmess')
    ss = await fetch_info('ss')
    vmess_byte = (vmess+'\n'+ss).encode()
    vmess_b64 = base64.b64encode(vmess_byte)
    message = vmess_b64.decode()
    return PlainTextResponse(message)

@app.get("/v2")
async def url():
    vmess = await fetch_info('vmess')
    ss = await fetch_info('ss')
    return PlainTextResponse(vmess+'\n'+ss)
