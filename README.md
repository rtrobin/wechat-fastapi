# wechat-fastapi

微信公众号和企业微信后台服务 based on [FastAPI](https://fastapi.tiangolo.com/) and [wechatpy](https://github.com/wechatpy/wechatpy)

## 使用方法

- `git clone` or `git pull`
- 将微信公众号的 `token`, `AES_KEY`, `appid` 填入到 `docker-compose.yml` 中对应的环境变量位置
- 将企业微信的 `token`, `AES_KEY`, `corpid` 填入到 `docker-compose.yml` 中对应的环境变量位置
- `docker compose up -d`

当前功能：

- 发送指定命令，抓取指定网站的内容，并返回
