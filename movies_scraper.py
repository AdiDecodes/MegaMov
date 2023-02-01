import requests
from bs4 import BeautifulSoup
import os

url_list = {}
API = 'e97f8232ba51a0a2bd9cb53380ebfb71f0555014'


def search_movies(query):
    movies_list = []
    movies_details = {}
    website = BeautifulSoup(requests.get(
        f"https://hdbollyhub.shop/?s={query.replace(' ', '+')}").text, "html.parser")
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


def get_movie(query):
    movie_details = {}
    movie_page_link = BeautifulSoup(requests.get(
        f"{url_list[query]}").text, 'html.parser')
    if movie_page_link:
        title = movie_page_link.find(
            "img", {'class': 'simple-grid-post-thumbnail-single-img wp-post-image'}).get('title')
        print(title)
        movie_details["title"] = title.replace("Download", "").strip()
        img = movie_page_link.find(
            "img", {'class': 'simple-grid-post-thumbnail-single-img wp-post-image'}).get('src')
        if checkURL(img) != 200:
            movie_details["img"] = "https://t3.ftcdn.net/jpg/03/45/05/92/360_F_345059232_CPieT8RIWOUk4JqBkkWkIETYAkmz2b75.jpg"
        else:
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
        for key in list(final_links.keys()):
            new_key = key.replace("mkvCinemas.mkv", "MegaMov")
            final_links[new_key] = final_links.pop(key)
        for key in list(final_links.keys()):
            new_key = key.replace("📥", "").strip()
            final_links[new_key] = final_links.pop(key)
    return movie_details
