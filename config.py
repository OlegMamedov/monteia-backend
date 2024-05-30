import requests
import json
import uuid

PRIVATE_KEY = '''-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDw7PVwN5pXVcn3
KvVY0b6+O6v9m/FOlwOhqQKV/A//11rgcBuhSHZHBOfYjzuzvknwrGOh/IocbBiO
IBOA6F7gK1Qs1yPacv/SPjvigKEKyS5Pmv7UrF3w/iZ8Xa1sEY6fS7FrYKW/IluF
7W3ur8NZUi+Twh2wwhZdLwu2Om9QUfl1ybfgKnvcpQrfWdtHuCffeh0DpAHkshLj
f7IoQa53MzLomBoRD49E+WrOn8soEUNFQz3wEyobWV1m5STM////J+2jdFTWqqAw
HvQjr+k4/YAzqT0tkWYncs2cYgoal2lkJTaMbXDO6RImfaGOr2qor/xV8GMLB1yh
Zk2biPNFAgMBAAECggEAAt2E8MA0iim/BKZ5L7ltV+s6q/45sTddXGIOUsXiRKbl
PvPhMtTzzaE34TKCTqjBGQr5OyLxpqva2mCSjDhxnbZHnsC527ayF/sQWg64qMUE
mw40ezhp3kAs9LwiTVu965B1laUAp97hi1UVZEg3/9OkS9S8SL/V8MEnBtgSNziH
CtaqvqfIPX3/ehuwP91QAh37kFUSZzorBR9c+8q/bufNIrI10sxRLYfX5KyUzvaY
MwJbaqgP3bvtex0E+WYGnCEy31Xqqcb6cSVmmEBVq3zGl98wSsxnJlaJ6feWTByb
PacXJQjvjD5EUFTGP2rgBAZL8tC9YVtr08hR2XICIQKBgQD5pVFTubHbOW4S8NoR
9HMS6bj3qEqO04jFdXq9WAe9nv0N10wTGE6V5GU0LuNuGg9BVar8I2Dc8ArBWB13
o1HzIyCq24FVLcZ5f8hw9w/n7KM+Z51/whX1eyFW5c4BYNjuk55HQl6Qw6BTwEnD
a3dXmvf+3Nl4BsSgL2iLnLlQpQKBgQD3DtIlTSp6HAnmOTR/hzO3Sy68C1BIKN5C
FcSzUwHhlFWar6T4zWG1Vl7u9D3sDfAy4QhnBojGRMusHS7nzZCpQVlxvNY55nAq
m9A5ZdOwWKdCy/VGPwtDfZLLg2ctU1WKidJTn1TK6poPHJ23sdD6hocm9eZzi9Hd
IZqcS9v2IQKBgQDYqGXtgNJfjPb/zzGitYENH/RcUxzp2aHwpKVyIC0PnyTFV115
kPXa1o4SfML6sfkdXaj4DAgrltPuundQdlhP5+OZBMm4z/JZTdH6YCDYyiFernQd
BacjFcp4bRadUZzTaR/Lfkkt3+mL5ezegazgRekGskq2BUGuN5bG26xk1QKBgAFY
hlKHshSKNI+Zfiy3qtNzyGRj12MdPeC0R6cGa7sz2KeID2j/jWm0d73rfK7dgJJ2
YVpWUcZqt4VPf2Lp3sDdR0R0V+Jm2/OPd7noURfj071saQCh9Ui/1V3gcF5x1sRz
bb7g3lBgqMguSrmmcVH8C55ttnyopVMEDNiPHTqhAoGANhUYvEQEFftQjzE6mnN2
rf40KO1AER4JQDOPVYX0N3GEyM3+raC8mm75r+SkzylfsIn/UW/v8TxaWOOdZcBh
BmYI0cF8SCd6Y5GnLCdmBeC7aVbzWq6UnpYOEynKPTUv1glyIki5dMp8FRSuDqZK
uv0Qa5C5XuaT1GGIiOxeTHc=
-----END PRIVATE KEY-----'''

PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA8Oz1cDeaV1XJ9yr1WNG+
vjur/ZvxTpcDoakClfwP/9da4HAboUh2RwTn2I87s75J8KxjofyKHGwYjiATgOhe
4CtULNcj2nL/0j474oChCskuT5r+1Kxd8P4mfF2tbBGOn0uxa2ClvyJbhe1t7q/D
WVIvk8IdsMIWXS8LtjpvUFH5dcm34Cp73KUK31nbR7gn33odA6QB5LIS43+yKEGu
dzMy6JgaEQ+PRPlqzp/LKBFDRUM98BMqG1ldZuUkzP///yfto3RU1qqgMB70I6/p
OP2AM6k9LZFmJ3LNnGIKGpdpZCU2jG1wzukSJn2hjq9qqK/8VfBjCwdcoWZNm4jz
RQIDAQAB
-----END PUBLIC KEY-----'''

ALGORITHM = "RS256"

#Синтез речи
API_KEY_LOVO = 'fd2ef182-4006-4f35-9840-235cb5941ce3'

# Nadezhda Smirnoff | 63b409f0241a82001d51c78e
# Galina Ivanov | 63b409eb241a82001d51c782
# Pyotr Semenov | 63b409ee241a82001d51c788

#Подключение GigaChat
url = "https://developers.sber.ru/docs/api/gigachat/auth/v2/oauth"

auth = "ZDYyYTgxOTgtN2Y3OC00NWQyLTkzNzAtMGVlYzYwYTY5NWI3OjVmMjUxYTE4LWEzOGQtNDlmOS04MGU0LTQyZjRjMTA3YmNmYQ=="

payload={
  "scope": "GIGACHAT_API_PERS"
}
headers = {
'Content-Type': 'application/x-www-form-urlencoded',
'Accept': 'application/json',
"Authorization": f"Basic {auth}",
"RqUID": str(uuid.uuid4())
}

response = requests.request("POST", url, headers=headers, data=payload)

ACCESS_TOKEN_GIGA = response.json().get("access_token")

# Отправка смс кода
SMSRU_API_ID = 'your_sms_ru_api_key'


POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = '88355247'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'
POSTGRES_DB = 'gadania'

POSTGRES_URL = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
)