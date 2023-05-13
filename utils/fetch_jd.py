import httpx
import time

def fetch_prices(ids: list[str]) -> list[float] :
    if not ids:
        return []

    param_id = ''
    for id in ids:
        param_id += f'J_{id},'

    param = {
        'skuIds': param_id[:-1],
        'pduid': str(int(time.time()))
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62'
    }

    ret = httpx.get(
        'https://p.3.cn/prices/mgets',
        params=param,
        headers=headers
    )

    return [obj.get('p') for obj in ret.json()]

if __name__ == '__main__':
    ids = [
        '100026761926',
        '100017628668',
        '100031822030',
        '100016592743'
    ]
    ret = fetch_prices(ids)
    print(ret)
