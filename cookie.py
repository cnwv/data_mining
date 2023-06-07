import requests
from avito_cookie import cookie
from avito_headers import headers
url = "https://www.avito.ru/"
response = requests.get(url, headers=headers, cookies=cookie)
print(response.status_code)
