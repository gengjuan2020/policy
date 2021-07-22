import requests

txt = requests.get("http://www.cqcbank.com")
print(txt.content)