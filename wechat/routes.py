import os
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

router = APIRouter()
TOKEN = os.environ.get('WECHAT_TOKEN', '')
AES_KEY = os.environ.get('WECHAT_AESKEY', '')
APP_ID = os.environ.get('WECHAT_APPID', '')

@router.get('/wechat')
async def wechat(
    msg_signature: str,
    timestamp: str,
    nonce: str,
    echostr: str
):
    try:
        check_signature(TOKEN, msg_signature, timestamp, nonce)
    except InvalidSignatureException:
        raise HTTPException(status_code=403)

    return HTMLResponse(content=echostr)

@router.post('/wechat')
async def wechat(
    msg_signature: str,
    timestamp: str,
    nonce: str,
    encrypt_type: Optional[str] = None,
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
