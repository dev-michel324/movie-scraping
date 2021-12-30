from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from bs4 import BeautifulSoup as Soup
import requests

from .models import *

# Create your views here.
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

    def varrerPage(self, cat, total: int, url: str):
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
                try:
                    ctgObject = Categoria.objects.get(nome=self.category[cat])
                    # dsc = self.get_description(dic[1][i])
                    # embed = self.get_embed(dic[1][i])
                    # print(ctgObject)
                    search = Movies.objects.filter(link=dic[1][i]).exists()
                    if not search:
                        filme = Movies(
                            fonte='redecanais',
                            categoria=ctgObject,
                            nome=dic[0][i],
                            # embed=embed,
                            # description=dsc,
                            link=dic[1][i],
                            image=dic[2][i],
                        )
                        filme.save()
                    else:
                        continue
                except:
                    continue
    
    def get_description(self, url: str):
        html = requests.get(url=url).text
        soup = Soup(html, 'lxml')

        description = soup.find('div', itemprop='description')
        return description.p.text

    def get_embed(self, url: str):
        html = requests.get(url=url).text
        soup = Soup(html, 'lxml')

        embed = soup.find('iframe')
        return 'https://redecanais.wf'+embed['src']

    def page_total(self, n, cat):
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

        self.varrerPage(cat=cat, total=total, url=url)


# var = Varredura()
# var.categoria()
# total = var.links
# for i in range(0, len(total)):
#     print('\nCATEGORIA: ' + var.category[i] + '\n')
#     var.page_total(n=i)
# saida = var.get_description('https://redecanais.wf/venom-tempo-de-carnificina-dublado-2021-1080p_85f3217d9.html')
# print(saida)
# print(var.get_embed('https://redecanais.wf/venom-tempo-de-carnificina-dublado-2021-1080p_85f3217d9.html'))

def movie(request, nome):
    category = Categoria.objects.all()

    search = request.GET.get('search')
    if search:
        movies = Movies.objects.filter(nome__icontains=search)
        return render(request, 'main/query.html', {'movies': movies, 'category': category})

    movie = Movies.objects.get(nome=nome)

    var = Varredura()
    try:
        description = var.get_description(movie.link)
        embed = var.get_embed(movie.link)

    except:
        return redirect(movie.link)

    return render(request, 'main/movie.html', {
        'movie': movie,
        'category': category,
        'description': description,
        'embed': embed,
    })


def updateList(request):
    var = Varredura()
    var.categoria()
    total = var.links
    for i in range(0, len(total)):
        var.page_total(n=i, cat=i)
    return redirect('main:index')

# def query(request):
#     category = Categoria.objects.all()
#     search = request.GET.get('search')
#     movies = Movies.objects.filter(nome_icontains=search)

#     return render(request, 'main/query.html', {'movies', movies, 'category', category})

def index(request):
    categoria = Categoria.objects.all()
    last_added = Movies.objects.all().order_by('-added')[:8]

    search = request.GET.get('search')
    if search:
        movies = Movies.objects.filter(nome__icontains = search)
        return render(request, 'main/query.html', {'movies': movies, 'category': categoria})

    comedia_obj = Categoria.objects.get(nome='Comédia')
    comedia = Movies.objects.filter(categoria=comedia_obj).order_by('-added')[:8]
    
    return render(request, 'main/index.html', {
        'category': categoria,
        'last_added': last_added,
        'comedia': comedia,
        })

def todosFilmes(request):
    movies = Movies.objects.all()
    category = Categoria.objects.all()

    search = request.GET.get('search')
    if search:
        movies = Movies.objects.filter(nome__icontains = search)
        return render(request, 'main/query.html', {'movies': movies, 'category': category})

    return render(request, 'main/all_movies.html', {'movies': movies ,'category': category})

def listaCategoria(request, categoria):
    cat = Categoria.objects.get(nome=categoria)
    movies = Movies.objects.filter(categoria=cat)
    category = Categoria.objects.all()

    search = request.GET.get('search')
    if search:
        movies = Movies.objects.filter(nome__icontains = search)
        return render(request, 'main/query.html', {'movies': movies, 'category': category})

    return render(request, 'main/list_category.html', {'movies': movies, 'categoria': categoria, 'category': category})

def about(request):
    categoria = Categoria.objects.all()
    return render(request, 'main/about.html', {'category': categoria})