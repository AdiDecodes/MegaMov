import requests
from bs4 import BeautifulSoup
import os

url_list = {}
API = 'e97f8232ba51a0a2bd9cb53380ebfb71f0555014'


def search_movies(query):
    movies_list = []
    movies_details = {}
    data = query
    website = BeautifulSoup(requests.get(
        f"https://hdbollyhub.shop/?s={data.replace(' ', '+')}").text, "html.parser")
    movies = website.find_all(
        "a", {'class': 'simple-grid-grid-post-thumbnail-link'})
    for movie in movies:
        if movie:
            movies_details["id"] = f"link{movies.index(movie)}"
            movies_details["title"] = movie.find(
                "img", {'class': 'simple-grid-grid-post-thumbnail-img wp-post-image'}).get("title").replace("Download", "").strip()
            url_list[movies_details["id"]] = movie['href']
        movies_list.append(movies_details)
        movies_details = {}
    return movies_list


def checkURL(url):
    request = requests.get(url)
    return (request.status_code)


def getImage(url):
    def_url = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'
    search_url = def_url + 'q=' + url.replace(' ', '+')
    imgdata = BeautifulSoup(requests.get(search_url).text, "html.parser")
    img = imgdata.find('img', {'class': 'yWs4tf'})['src']
    return img


def get_movie(query):
    flag = False
    movie_details = {}
    movie_page_link = BeautifulSoup(requests.get(
        f"{url_list[query]}").text, 'html.parser')
    if movie_page_link:
        title = movie_page_link.find(
            "img", {'class': 'simple-grid-post-thumbnail-single-img wp-post-image'}).get('title')
        movie_details["title"] = title.replace("Download", "").strip()
        img = movie_page_link.find(
            "img", {'class': 'simple-grid-post-thumbnail-single-img wp-post-image'}).get('src')
        if checkURL(img) != 200:
            flag = True
            movie_details["img"] = getImage(title)
        else:
            flag = False
            movie_details["img"] = img
        links = movie_page_link.find_all(
            "a", {'class': 'maxbutton'})
        final_links = {}
        for i in links:
            url = f"https://urlshortx.com/api?api={API}&url={i['href']}"
            response = requests.get(url)
            link = response.json()
            final_links[f"{i.text}"] = link['shortenedUrl']
        movie_details["links"] = final_links
        if flag:
            movie_details[
                "Note"] = "Note: Please check the given URLS. They may not be working! (Content Recovered from Archives)"
        else:
            movie_details[
                "Note"] = ""
        for key in list(final_links.keys()):
            new_key = key.replace("mkvCinemas.mkv", "MegaMov")
            final_links[new_key] = final_links.pop(key)
        for key in list(final_links.keys()):
            new_key = key.replace("📥", "").strip()
            final_links[new_key] = final_links.pop(key)
    return movie_details
