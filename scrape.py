import requests
import csv
import time
from bs4 import BeautifulSoup


def scrape_reddit(url="https://old.reddit.com/r/all/"):

    # Headers to mimic a browser visit
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Returns a requests.models.Response object
    page = requests.get(url, headers=headers, )

    soup = BeautifulSoup(page.text, 'html.parser')

    domains = soup.find_all("span", class_="domain")

    for domain in domains:
        if domain != "(self.datascience)":
            continue

        parent_div = domain.parent.parent.parent.parent
        print(parent_div.text)

    counter = 1

    while counter <= 100:

        attrs = {'class': 'thing', 'data-domain': 'self.datascience'}

        for post in soup.find_all('div', attrs=attrs):

            print(post.attrs['data-domain'])

            title = post.find('p', class_="title").text

            author = post.find('a', class_='author').text

            likes = post.find("div", attrs={"class": "score likes"}).text

            if likes == "•":
                likes = "None"

            comments = post.find('a', class_='comments').text.split()[0]

            if comments == "comment":
                comments = 0

            post_line = [counter, title, author, likes, comments]

            with open('output.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(post_line)

            counter += 1

        next_button = soup.find("span", class_="next-button")
        next_page_link = next_button.find("a").attrs['href']
        time.sleep(2)
        page = requests.get(next_page_link, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
