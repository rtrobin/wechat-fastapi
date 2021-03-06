from typing import Optional

from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import HTMLResponse

from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)

from utils.fetch_vmess import fetch_info
from utils.credential import WECHAT_AESKEY as AES_KEY
from utils.credential import WECHAT_APPID as APP_ID
from utils.credential import WECHAT_TOKEN as TOKEN

router = APIRouter()

@router.get('/wechat')
async def wechat(
    signature: str,
    timestamp: str,
    nonce: str,
    echostr: str
):
    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        raise HTTPException(status_code=403)

    return HTMLResponse(content=echostr)

@router.post('/wechat')
async def wechat(
    msg_signature: Optional[str] = None,
    timestamp: Optional[str] = None,
    nonce: Optional[str] = None,
    encrypt_type: Optional[str] = 'raw',
    body_msg: str = Body(..., media_type='application/html')
):
    if encrypt_type == 'raw':
        # plaintext mode
        msg = parse_message(body_msg)
        if msg.type != 'text':
            reply = create_reply('暂不支持该类型_(:зゝ∠)_', msg)
        else:
            reply = await fetch_info(msg.content)
            reply = create_reply(reply, msg)
        return HTMLResponse(reply.render())
    else:
        # encryption mode
        crypto = WeChatCrypto(TOKEN, AES_KEY, APP_ID)
        try:
            body_msg = crypto.decrypt_message(
                body_msg,
                msg_signature,
                timestamp,
                nonce
            )
        except (InvalidSignatureException, InvalidAppIdException):
            raise HTTPException(status_code=403)
        else:
            msg = parse_message(body_msg)
            if msg.type != 'text':
                reply = create_reply('暂不支持该类型_(:зゝ∠)_', msg)
            else:
                reply = await fetch_info(msg.content)
                reply = create_reply(reply, msg)
            return HTMLResponse(crypto.encrypt_message(reply.render(), nonce, timestamp))
