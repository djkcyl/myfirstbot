import httpx

resp = httpx.get("http://a60.one:404/", params={"num": 5})
data = resp.text

print(data)
