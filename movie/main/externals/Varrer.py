from bs4 import BeautifulSoup as Soup
import requests

from .. import models

class Varredura():
    category = []
    links = []

    def categoria(self):
        html = requests.get(
            url="https://redecanais.wf/browse-filmes-dublado-videos-1-date.html").text
        soup = Soup(html, "lxml")

        page = soup.find('div', class_="pm-category-subcats")

        for cat in page.find_all('li'):
            if 'show' in cat.a['href']:
                continue
            else:
                self.links.append('https://redecanais.wf' + cat.a['href'])
                self.category.append(cat.text)

    def varrerPage(self, cat: int, total: int, url: str):
        dic = [[], [], []]
        for i in range(1, int(total)):
            print('\nPAGE: ', i, '\n')
            get_url = url.replace('1', str(i))
            html = requests.get(url=get_url).text
            soup = Soup(html, 'lxml')

            movies = soup.find("div", class_="col-md-12")

            for i in movies.find_all('a', class_='ellipsis'):
                dic[0].append(i.text) #title
                dic[1].append('https://redecanais.wf'+i['href']) #link

            for i in movies.find_all('img', class_='img-responsive'):
                dic[2].append('https://redecanais.wf'+i['data-echo']) #image link

            for i in range(len(dic[0])):
                dsc = self.get_description(dic[1][i])
                # filme = models.Movies(
                #     categoria=self.category[cat],
                #     nome=dic[0][i],
                #     embed='',
                #     description=dsc,
                #     link=dic[1][i],
                #     image=dic[2][i],
                #     )

                print(
                    'Title: ' + dic[0][i] + '\n'
                    'Link: ' + dic[1][i] + "\n"
                    'Img: ' + dic[2][i] + "\n"
                    'Dsc:' + dsc + "\n"
                )
            print('\n')
    
    def get_description(self, url: str):
        html = requests.get(url=url).text
        soup = Soup(html, 'lxml')

        description = soup.find('div', itemprop='description')
        return description.p.text

    def get_embed(self, url: str):
        html = requests.get(url=url).text
        soup = Soup(html, 'lxml')

        embed = soup.find('iframe')
        return embed['src']

    def page_total(self, n):
        url = self.links[n]
        html = requests.get(url=url).text
        soup = Soup(html, 'lxml')

        page = soup.find('div', class_='col-md-12 text-center')
        t = []
        for n in page.find_all('li'):
            t.append(n.text)
        n = []
        for i in t:
            n.append(i.replace('\n', ''))
        total = n[len(n) - 2]

        self.varrerPage(cat=n, total=total, url=url)


var = Varredura()
# var.categoria()
# total = var.links
# for i in range(0, len(total)):
#     print('\nCATEGORIA: ' + var.category[i] + '\n')
#     var.page_total(n=i)
# saida = var.get_description('https://redecanais.wf/venom-tempo-de-carnificina-dublado-2021-1080p_85f3217d9.html')
# print(saida)
print(var.get_embed('https://redecanais.wf/venom-tempo-de-carnificina-dublado-2021-1080p_85f3217d9.html'))
