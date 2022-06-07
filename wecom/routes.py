from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import HTMLResponse

from wechatpy.enterprise import parse_message, create_reply
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.enterprise.exceptions import InvalidCorpIdException

from utils.fetch_vmess import fetch_info
from utils.credential import WECOM_AESKEY as AES_KEY
from utils.credential import WECOM_CORPID as CORP_ID
from utils.credential import WECOM_TOKEN as TOKEN

router = APIRouter()

@router.get('/wecom')
async def wecom(
    msg_signature: str,
    timestamp: str,
    nonce: str,
    echostr: str
):
    crypto = WeChatCrypto(TOKEN, AES_KEY, CORP_ID)
    try:
        echostr = crypto.check_signature(
            msg_signature,
            timestamp,
            nonce,
            echostr
        )
    except InvalidSignatureException:
        raise HTTPException(status_code=403)

    return HTMLResponse(content=echostr)

@router.post('/wecom')
async def wecom(
    msg_signature: str,
    timestamp: str,
    nonce: str,
    body_msg: str = Body(..., media_type='application/html')
):
    crypto = WeChatCrypto(TOKEN, AES_KEY, CORP_ID)
    try:
        body_msg = crypto.decrypt_message(
            body_msg,
            msg_signature,
            timestamp,
            nonce
        )
    except (InvalidSignatureException, InvalidCorpIdException):
        raise HTTPException(status_code=403)
    else:
        msg = parse_message(body_msg)
        if msg.type != 'event':
            reply = create_reply('暂不支持该类型_(:зゝ∠)_', msg)
        else:
            reply = await fetch_info(msg.key)
            reply = create_reply(reply, msg)
        return HTMLResponse(crypto.encrypt_message(reply.render(), nonce, timestamp))
