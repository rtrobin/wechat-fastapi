import re
import httpx

async def fetch_info(msg: str) -> str :
    msg = msg.lower()

    async def parse_url(url: str, types: list[str]) -> str:
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
        full_text = r.content.decode()
        links = []
        for type in types:
            links += re.findall(f'{type}://.+(?=</)', full_text)

        ret = ''
        for link in links:
            ret += link + '\n'
        return ret[:-1]

    if msg == 'vmess':
        url = 'https://github.com/Alvin9999/new-pac/wiki/v2ray免费账号'
        types = ['vmess', 'trojan']
    elif msg == 'ss' or msg == 'ssr':
        url = 'https://github.com/Alvin9999/new-pac/wiki/ss免费账号'
        types = [msg]
    else:
        return '暂不支持(⊙_⊙)?'

    return await parse_url(url, types)
