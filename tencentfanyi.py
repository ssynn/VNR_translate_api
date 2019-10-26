# coding: utf8

import json
import requests
import random
import hashlib
import time
import urllib
from sakurakit.skdebug import dwarn, derror

appid = ''  # 你的appid
appkey = ''  # 你的密钥
keys = ['app_id', 'nonce_str', 'source', 'target', 'text','time_stamp']


def get_req_sign(data, appkey):
    temp = ''
    for key in keys:
        temp+=(key+'='+urllib.quote_plus(data[key])+'&')
    temp+=('app_key='+appkey)
    return hashlib.md5(temp).hexdigest().upper()

def translate(text, to='zhs', fr='ja'):
    try:
        query = text.encode('utf-8')

        data = {
            'app_id':appid,
            'source':'jp',
            'target':'zh',
            'text':query,
            'time_stamp':str(int(time.time())),
            'nonce_str': str(random.randint(10000000, 90000000))
        }
        data['sign'] = get_req_sign(data, appkey)
        url = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_texttranslate'
        res = requests.post(url=url, data=data, timeout=5)
        if res.ok:
            result = json.loads(res.text)['data']['target_text']
            return result
        else:
            derror('error')
            return ''

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
        pass
    else:
        pass

if __name__ == "__main__":
    text = u"高校一年生の桜庭理沙は平均的な少女。 ある日拾ったカードの力により魔法少女となり戦うお話"
    print translate(text)