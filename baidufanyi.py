# coding: utf8

import json
import requests
import random
import hashlib
from sakurakit.skdebug import dwarn, derror

appid = ''  # 你的appid
secretKey = ''  # 你的密钥


def translate(text, to='zhs', fr='ja'):
    try:
        query = text
        salt = random.randint(32768, 65536)
        sign = appid+query+str(salt)+secretKey
        sign = hashlib.md5(sign.encode('utf-8')).hexdigest()

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            "from": "jp",
            "to": "zh",
            "q": query,
            "salt": str(salt),
            "sign": sign,
            "appid": appid
        }
        url = 'https://api.fanyi.baidu.com/api/trans/vip/translate'
        res = requests.post(url=url, headers=headers, data=data, timeout=4)
        if res.ok:
            result = json.loads(res.text)['trans_result'][0]['dst']
            return result
        else:
            derror('error')
            pass

    except requests.ConnectionError, e:
        dwarn("connection error", e.args)
    except requests.HTTPError, e:
        dwarn("http error", e.args)
    except UnicodeDecodeError, e:
        dwarn("unicode decode error", e)
    except (ValueError, KeyError, IndexError, TypeError), e:
        dwarn("json format error", e)
    except Exception, e:
        derror('error', e)
    else:
        pass
