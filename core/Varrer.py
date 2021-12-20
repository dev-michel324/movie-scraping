from bs4 import BeautifulSoup as Soup
import requests

class Varredura():
    category = []
    links = []

    def categoria(self):
        html = requests.get(url="https://redecanais.wf/browse-filmes-dublado-videos-1-date.html").text
        soup = Soup(html, "lxml")

        page = soup.find('div', class_="pm-category-subcats")
        
        for cat in page.find_all('li'):
            if 'show' in cat.a['href']:
                continue
            else:
                self.links.append('https://redecanais.wf'+cat.a['href'])
                self.category.append(cat.text)

    def varrerPage(self, total: int, url: str):
        dic = [[], [], []]
        for i in range(1, int(total)):
            print('\nPAGE: ', i, '\n')
            get_url = url.replace('1', str(i))
            html = requests.get(url=get_url).text
            soup = Soup(html, 'lxml')

            movies = soup.find("div", class_="col-md-12")

            for i in movies.find_all('a', class_='ellipsis'):
                dic[0].append(i.text)
                dic[1].append(i['href'])

            for i in movies.find_all('img', class_='img-responsive'):
                dic[2].append(i['data-echo'])

            for i in range(len(dic[0])):
                # with open('movies.txt', 'a') as arquivo:
                #     arquivo.write(dic[0][i]+'\n'+dic[1][i]+'\n'+dic[2][i]+'\n\n')
                print(
                    'Title: '+dic[0][i]+'\n'
                    'Link: '+dic[1][i]+"\n"
                    'Img: '+dic[2][i]+"\n"
                )
            print('\n')

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
        total = n[len(n)-2]
        
        self.varrerPage(total=total, url=url)


var = Varredura()
var.categoria()
total = var.links
for i in range(0, len(total)):
    print('\nCATEGORIA: '+ var.category[i]+'\n')
    # with open('movies.txt', 'a') as arquivo:
    #     arquivo.write('\nCATEGORIA: '+var.category[i]+'\n\n')
    var.page_total(n=i)