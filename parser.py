import requests
import csv
from bs4 import BeautifulSoup as bs

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
count = 1
while count <=3:

    base_url = 'https://www.film.ru/movies?page=' + str(count)


    def movie_parser(base_url, head):
        movies = []
        session = requests.Session()
        request = session.get(base_url, headers=head)
        if request.status_code == 200:

            soup = bs(request.content, 'lxml')
            divs = soup.find('div', class_='rating infinite_scroll').find_all('a')

            for div in divs:
                try:
                    title = div.find("strong").text
                    img = div.find('img').get('src')
                    rate = div.find('span', class_='rate').find('strong')
                    movies.append({
                        'title': title,
                        'img': img,
                        'rate': rate
                    })
                except:
                    pass
            print(movies)
        else:
            print('ERROR')
        return movies
    count += 1

    def file_writer(movies):
        with open('parser.csv', 'a') as file:
            data =csv.writer(file)
            data.writerow( ('Название фильма', 'SRC', 'Рейтинг')  )
            for mv in movies:
                data.writerow( (mv['title'], mv['img'], mv['rate'] ) )


    movies = movie_parser(base_url, head)
    file_writer(movies)
