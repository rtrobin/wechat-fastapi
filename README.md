# wechat-fastapi

微信公众号和企业微信后台服务 based on [FastAPI](https://fastapi.tiangolo.com/) and [wechatpy](https://github.com/wechatpy/wechatpy)

## 使用方法

- `git clone` or `git pull`
- 参考 secrets/README.md 设置 微信公众号/企业微信 token 等信息
- `docker compose up -d`

当前功能：

- 发送指定命令，抓取指定网站的内容，并返回
