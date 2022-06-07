import os
import json

CREDENTIAL_FILE = os.environ.get('CREDENTIAL_FILE', '')
with open(CREDENTIAL_FILE, 'r') as fp:
    credentials = json.load(fp)

WECHAT_AESKEY = credentials['WECHAT_AESKEY']
WECHAT_APPID = credentials['WECHAT_APPID']
WECHAT_TOKEN = credentials['WECHAT_TOKEN']
WECOM_AESKEY = credentials['WECOM_AESKEY']
WECOM_CORPID = credentials['WECOM_CORPID']
WECOM_TOKEN = credentials['WECOM_TOKEN']
