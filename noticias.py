"""
Código que faz Web Scraping da página inicial do site Só Notícias e mostra
as notícias organizadas por categoria.
"""

from bs4 import BeautifulSoup as soup  # HTML data structure
import urllib  # Web client
import webbrowser  # biblioteca para abrir um link


def ver_secoes(noticias, return_last=False):
    if return_last:
        return return_last
    for i, key in enumerate(noticias.keys()):
        print(f"{i}: {key}")
    print(f"{i+1}: Sair")
    escolha = int(input("Escolha qual seção deseja ver: "))
    if escolha == i+1:
        return False
    secao = list(noticias.keys())[escolha]
    return secao


def ver_noticia(noticias, secao, Break=False):
    for i, noticia in enumerate(noticias[secao]):
        print(f"{i}: {noticia.h2.text}")
    print(f"{i+1}: Sair")
    escolha = int(input("Escolha qual notícia deseja ver: "))
    if escolha == i+1:
        return True
    noticia = noticias[secao][escolha].h2.a['href']
    webbrowser.open_new_tab(noticia)
    return False


# página que estaremos fazendo o Web Scraping
page_url = "https://www.sonoticias.com.br/"

# Cabeçalho do dosso request (pedido)
headers = {
    "Host": "www.sonoticias.com.br",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}

request = urllib.request.Request(page_url, headers=headers)  # faz o request
response = urllib.request.urlopen(request)  # obtem a response (resposta)
# transforma a sopa de dados em uma estrutura JSON
page_soup = soup(response.read(), "html.parser")

secoes = page_soup.find_all("div", {"class": "herald-module"})  # Pega
noticias = {}
for i, secao in enumerate(secoes):
    h2 = secao.find('h2', {"class": "h6 herald-mod-h herald-color"})
    if h2:
        noticias[h2.text] = secao.find_all('article')

return_last = False
while 1:
    try:
        secao = ver_secoes(noticias, return_last)
        if not secao:
            break
        sair = ver_noticia(noticias, secao)
        if sair:
            break
        print("0: Ler outra notícia")
        print("1: Voltar para secoes")
        print("2: Sair")
        escolha = int(input("Escolha uma ação: "))

        if escolha == 0:
            return_last = secao
            continue
        elif escolha == 1:
            return_last = False
            continue
        else:
            break
        clear_output()
    except:
        print(f"Ocorreu um erro, tente novamente")
        break
