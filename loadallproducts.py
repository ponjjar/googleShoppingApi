from bs4 import BeautifulSoup
import requests
import json
import re

headers = {  # <-- so the Google will treat your script as a "real" user browser.
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36 OPR/60.0.3255.50962 OPRGX/60.0.3255.50962",
    "Content-Language": "pt-BR"
}
quote = input("O que voce deseja pesquisar? ")
response = requests.get(
  f'https://www.google.com/search?q=={quote}&tbm=shop', quote,
  headers=headers).text

soup = BeautifulSoup(response, 'lxml')

data = []
menorValor = [{
    "Title": "",
    "Price": "R$ 10000000.00",
    "Supplier": "",
  }]
for container in soup.findAll('div', class_='sh-dgr__content'):
  title = container.find('h3', class_='tAxDx').text
  price = container.find('span', class_='a8Pemb OFFNJ').text.replace(',','.')
  supplier = container.find('div', class_='aULzUe IuHnof').text
  url =  str(str(container.find('a', class_='xCpuod')['href']).split('/url?url='))

  data.append({
    "Title": title,
    "Price": price,
    "Supplier": supplier,
    "URL": url
  })
  if(float(re.findall("\d+", menorValor[0]["Price"])[0]) > float(re.findall("\d+", price)[0])):
    menorValor[0]["Title"] = title
    menorValor[0]["Price"] = price
    menorValor[0]["Supplier"] = supplier
    menorValor[0]["URL"] = url


print(json.dumps(data, indent = 2, ensure_ascii = False))
print("Menor preço:"+ json.dumps(menorValor, indent = 2, ensure_ascii = False))	