# Gunicorn configuration file.

bind = '[::]:17892'
workers = 1
worker_class = 'uvicorn.workers.UvicornWorker'
raw_env = [
    'CREDENTIAL_FILE=./secret/credential.json'
]

errorlog = '-'
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# import requests
# from utils.fetch_vmess import fetch_info
# import asyncio

# def on_starting(server):
#     from utils.credential import WECOM_AESKEY as AES_KEY
#     print('server starting')
#     print(AES_KEY)
#     # print(WECOM_CORPID)
#     print(requests.get('https://www.google.com'))
#     info = asyncio.run(fetch_info('vmess'))
#     print(info)