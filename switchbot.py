import base64
import hmac
import hashlib
import time
import requests
import json


# こぴぺした！
#  https://qiita.com/masaki12-s/items/0295a96fd5a70442f7d5
class SwitchBot:
    def __init__(self, token, secret):
        self.token = token
        self.secret = secret
        self.base_url = 'https://api.switch-bot.com'

    def make_sign(self, token: str, secret: str):
        nonce = ''
        t = int(round(time.time() * 1000))
        string_to_sign = bytes(f'{token}{t}{nonce}', 'utf-8')
        secret = bytes(secret, 'utf-8')
        sign = base64.b64encode(
            hmac.new(secret, msg=string_to_sign,
                     digestmod=hashlib.sha256).digest())
        return sign, str(t), nonce

    def make_request_header(self, token: str, secret: str) -> dict:
        sign, t, nonce = self.make_sign(token, secret)
        headers = {
            "Authorization": token,
            "sign": sign,
            "t": str(t),
            "nonce": nonce
        }
        return headers

    def get_device_list(self, deviceListJson='deviceList.json'):
        devices_url = self.base_url + "/v1.1/devices"
        headers = self.make_request_header(self.token, self.secret)
        try:
            # APIでデバイスの取得を試みる
            res = requests.get(devices_url, headers=headers)
            res.raise_for_status()
            deviceList = json.loads(res.text)
            # 取得データをjsonファイルに書き込み
            print(deviceList["body"]["infraredRemoteList"])
            with open(deviceListJson, mode='wt', encoding='utf-8') as f:
                json.dump(deviceList["body"]["infraredRemoteList"],
                          f, ensure_ascii=False, indent=2)
        except requests.exceptions.RequestException as e:
            print('response error:', e)

    def use_device_command(self, device: str, action: str):
        print('a')
        devices_url = self.base_url + "/v1.1/devices/"\
            + device + "/commands/"
        commands = {
            "command": action,
            "parameter": "default",
            "commandType": "command"
        }
        headers = self.make_request_header(self.token, self.secret)
        try:
            # APIでデバイスの取得を試みる
            res = requests.post(devices_url, headers=headers,
                                data=json.dumps(commands))
            res.raise_for_status()
            check = json.loads(res.text)
            # 取得データをjsonファイルに書き込み
            print(check)
        except requests.exceptions.RequestException as e:
            print('response error:', e)
