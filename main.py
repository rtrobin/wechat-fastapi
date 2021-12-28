from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse

from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)

import os

app = FastAPI()
TOKEN = os.environ.get('TOKEN', '')
AES_KEY = os.environ.get('AESKEY', '')
APPID = os.environ.get('APPID', '')

@app.get('/wechat')
async def wechat(
    request: Request
):
    signature = request.query_params.get('signature', '')
    timestamp = request.query_params.get('timestamp', '')
    nonce = request.query_params.get('nonce', '')

    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        raise HTTPException(status_code=403)

    echo_str = request.query_params.get('echostr', '')
    return HTMLResponse(content=echo_str)

@app.post('/wechat')
async def wechat(
    request: Request
):
    timestamp = request.query_params.get('timestamp', '')
    nonce = request.query_params.get('nonce', '')
    encrypt_type = request.query_params.get('encrypt_type', 'raw')
    msg_signature = request.query_params.get('msg_signature', '')

    body_msg = await request.body()
    if encrypt_type == 'raw':
        # plaintext mode
        msg = parse_message(body_msg)
        if msg.type != 'text':
            reply = create_reply('暂不支持该类型_(:зゝ∠)_', msg)
        else:
            reply = create_reply(msg.content, msg)
        return HTMLResponse(reply.render())
    else:
        # encryption mode
        from wechatpy.crypto import WeChatCrypto

        crypto = WeChatCrypto(TOKEN, AES_KEY, APPID)
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
                reply = create_reply(msg.content, msg)
            return HTMLResponse(crypto.encrypt_message(reply.render(), nonce, timestamp))

    