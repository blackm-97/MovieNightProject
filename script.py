
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

def lookForMovie(mov):
    return 0

# assign required credentials
# assign URL


if __name__ == '__main__':

    user_list = createuserList()
    print(user_list)

    print('Enter the movie title:')
    movie_name = input()
    movie_name = changeNameToHTML(movie_name)
    print(movie_name)

    for user in user_list:
        url_to_scrape = "https://letterboxd.com/" + user + "/film/" + movie_name +"/"

        # create document
        html_document = getHTMLdocument(url_to_scrape)

        # create soap object
        soup = BeautifulSoup(html_document, 'html.parser')

        try:
            review = soup.find(attrs={"name": "description"})
            rating = soup.find(attrs={"name": "twitter:data2"})
            rating = getRating(str(rating.get('content')))
            print(review.get('content'))
            print(rating)
        except:
            print('An error occurred! The username was not found.')
        # print(soup.find('div', 'film-metadata'))

        # find all the anchor tags with "href"
        # attribute starting with "https://"
        # print(soup.prettify())
