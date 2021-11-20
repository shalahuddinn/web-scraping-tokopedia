from bs4 import BeautifulSoup
import csv
import time
import urllib.parse

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def get_all_products_links(browser):
    MAX_LINKS = 100
    num_links = 0
    for i in range(1, 3):
        url = 'https://www.tokopedia.com/p/handphone-tablet/handphone?page={}'.format(
            i)

        browser.get(url)
        ScrollNumber = 2
        for i in range(1, ScrollNumber):
            browser.execute_script("window.scrollTo(1,2000)")
            time.sleep(1)

        soup = BeautifulSoup(browser.page_source, 'html.parser')
        with open('links.txt', 'a') as f1:
            for links in soup.find_all('div', {'class': 'css-bk6tzz e1nlzfl3'}):
                if num_links < MAX_LINKS:
                    link = links.find('a').get('href')
                    # format the link if it is an ads link
                    if 'https://ta.tokopedia.com' in link:
                        link = (link.split('r=')[1]).split('%3Fsrc')[0]
                        link = urllib.parse.unquote(link)
                    f1.write(link)
                    f1.write('\n')
                    num_links += 1
                else:
                    break


def get_specific_products_data(writer):
    with open('links.txt', 'r') as f2:
        for line in f2:
            browser.get(line)
            # wait until all ajax has been loaded
            time.sleep(5)

            soup = BeautifulSoup(browser.page_source, 'html.parser')
            productName = soup.find(
                'h1', {'data-testid': 'lblPDPDetailProductName'}).text
            description = soup.find(
                'div', {'data-testid': 'lblPDPDescriptionProduk'}).text
            imageDiv = soup.find(
                'div', 'css-1y5a13')
            imageLink = imageDiv.img.get('src')
            price = soup.find(
                'div', {'data-testid': 'lblPDPDetailProductPrice'}).text
            ratingSpan = soup.find(
                'span', {'data-testid': 'lblPDPDetailProductRatingNumber'})
            rating = ratingSpan.text
            merchantA = soup.find(
                'a', {'data-testid': 'llbPDPFooterShopName'})
            merchant = merchantA.h2.text
            writer.writerow([productName, description,
                            imageLink, price, rating, merchant])


if __name__ == "__main__":
    # clear file
    file = open("links.txt", "w")
    file.close()
    # clear file
    file = open("results.csv", "w")
    file.close()
    # prepare the browser
    browser = webdriver.Chrome(ChromeDriverManager().install())
    get_all_products_links(browser)
    kepala = ['Name of Product', 'Description',
              'Image Link', 'Price', 'Rating', 'Merchant']
    with open('results.csv', 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(kepala)
        get_specific_products_data(writer)
    browser.close()
