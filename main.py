import pandas as pd
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from validation import Movie


def get_pages():
    pages = []
    for x in range(1, 2432):
        page = f'https://yts.mx/browse-movies?page={x}'
        pages.append(page)
    return pages


pages = get_pages()


def get_movie(page):
    response = requests.get(page).text
    soup = BeautifulSoup(response, 'html.parser')
    movies_tags = soup.find_all('div', {'class', 'browse-movie-wrap'})
    movies = []
    for movie_tag in movies_tags:
        movie_soup = BeautifulSoup(str(movie_tag), 'html.parser')

        # extract the title
        title = movie_soup.find('a', class_='browse-movie-title').text.strip()
        if title[0] == "[":
            title = title[5:]

        # extract the year
        year = movie_soup.find('div', class_='browse-movie-year').text.strip()

        # extract the genre
        genre_list = [h4.text for h4 in movie_soup.find_all('h4')[1:-1]]  # exclude the rating h4
        genre = '- '.join(genre_list)

        # extract the rating
        rating = movie_soup.find('h4', class_='rating').text.strip().split('/')[0].strip()

        # extract the link
        link = movie_soup.find('a', class_='browse-movie-link')['href']

        # create a dictionary with the extracted data
        data = {
            'title': title,
            'year': year,
            'genre': genre,
            'rating': rating,
            'link': link,
        }

        movie = Movie(**data)
        movies.append(dict(movie))
    df = pd.DataFrame(movies)
    df.to_csv('ytx_movies', mode='a', index=False, header=False)
    print(df)


with ThreadPoolExecutor() as executor:
    executor.map(get_movie, pages)
