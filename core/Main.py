from bs4 import BeautifulSoup as Soup
import requests

html = requests.get(url="https://redecanais.wf/").text

soup = Soup(html, "lxml")

section_main = soup.find_all("div", class_="col-md-12")

i = 0
for movie in section_main:
    i += 1
    title_link = movie.find('a', class_="ellipsis")
    img = movie.find('img', class_="img-responsive")

    print("\nTitle: ", title_link.text,"\nLink: ", title_link['href'],"\nImg: ", img['data-echo'])

print("\ntotal: ", i)
    # print(
    #     f'''
    #         Nome: {title_link.text}
    #         Link: {title_link['href']}
    #         Img: {img['data-echo']}
    #     '''
    # )