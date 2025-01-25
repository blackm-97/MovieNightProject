
# import necessary libraries
from bs4 import BeautifulSoup
import requests
import re

def getRating(star_rating):
    if star_rating[-1] == '½':
        return len(star_rating) - 0.5
    return len(star_rating)

# function to extract html document from given url
def getHTMLdocument(url):

    # request for HTML document of given url
    response = requests.get(url)

    # response will be provided in JSON format
    return response.text

#Changes movie name to HTML format
def changeNameToHTML(mov_name):
    mov_name = mov_name.replace(' ', '-')
    mov_name = mov_name.lower()
    return mov_name

def createuserList():
    new_list = []
    file = open('users.txt', 'r')
    for line in file:
        new_list.append(line.strip())
    return new_list

# assign required credentials
# assign URL


if __name__ == '__main__':

    user_list = createuserList()
    print(user_list)
    movie_name = 'placeholder'

    while movie_name:
        print('Please enter the movie name. If there are two movies with the same name, insert the data afterwards.')
        print('Keep the textbox blank to stop the program')
        movie_name = input()
        movie_name = changeNameToHTML(movie_name)

        # Tests that movie exists
        movie_test_doc = getHTMLdocument("https://letterboxd.com/film/" + movie_name + "/")
        soup = BeautifulSoup(movie_test_doc, 'html.parser')

        genre_list = []
        flag = False

        film_stats = ''

        try:
            name = soup.find(attrs={"property": "og:title"}).get('content')
            review = soup.find(attrs={"name": "description"})
            year = soup.find(attrs={"id": "film-page-wrapper"})
            year = year.find(attrs={"class": "releaseyear"}).a.string
            genres = soup.find(attrs={"id": "film-page-wrapper"})
            genres = genres.find(attrs={"id": "tab-genres"})
            genres = genres.find(attrs={"class": "text-sluglist capitalize"}).find_all('a')
            for genre in genres:
                genre_list.append(genre.string)

            runtime = soup.find(attrs={"class": "text-link text-footer"}).contents[0].strip()
            runtime = runtime[0:7]
            print(name)
            print("Genres: " + str(genre_list))
            print("Runtime: " + runtime)
            film_stats += name[:-7] + ', ' + year
            if len(genre_list) > 0 and genre_list[0]:
                film_stats += ", " + genre_list[0]
            if len(genre_list) > 1 and genre_list[1]:
                film_stats += ", " + genre_list[1]
            # print(year)
            film_stats += ", " + runtime.split()[0]
            print()
            flag = True
        except:
            print("Failed to find movie")
        review = soup.find(attrs={"name": "description"})

        total_score = 0.0
        total_reviews = 0.0
        score_list = []

        # If movie exists, continue
        if flag:
            for user in user_list:
                url_to_scrape = "https://letterboxd.com/" + user + "/film/" + movie_name + "/reviews/"

                # create document
                html_document = getHTMLdocument(url_to_scrape)

                # create soap object
                soup = BeautifulSoup(html_document, 'html.parser')



                try:
                    film_details = soup.find(attrs={"class": "viewings-list"})
                    count = str(film_details).count('<li class="film-detail">')

                    if count == 1:
                        url_to_scrape = "https://letterboxd.com/" + user + "/film/" + movie_name + "/"

                        # create document
                        html_document = getHTMLdocument(url_to_scrape)

                        # create soap object
                        soup = BeautifulSoup(html_document, 'html.parser')
                    elif count > 1:
                        url_to_scrape = "https://letterboxd.com/" + user + "/film/" + movie_name + "/" + str(count - 1) + "/"

                        # create document
                        html_document = getHTMLdocument(url_to_scrape)

                        # create soap object
                        soup = BeautifulSoup(html_document, 'html.parser')
                    else:
                        raise Exception("Failed to find review")

                    review = soup.find(attrs={"name": "description"})
                    rating = soup.find(attrs={"name": "twitter:data2"})
                    rating = getRating(str(rating.get('content')))
                    print('User: ' + user)
                    print('Rating: ' + str(rating))
                    print(review.get('content'))
                    print()
                    total_reviews += 1
                    total_score += float(rating)
                    score_list.append(rating)
                except:
                    print('User: ' + user)
                    print('User did not enter any rating')
                    print()
                    score_list.append(None)
                # print(soup.find('div', 'film-metadata'))
            if total_reviews != 0:
                print("Total Score:")
                print(total_score / total_reviews)
                print()
                film_stats += ", " + str(total_score / total_reviews)
                print("Film Stats:")
                print(film_stats)
                print("Scores List:")
                print(score_list)
            else:
                print('No reviews found')
