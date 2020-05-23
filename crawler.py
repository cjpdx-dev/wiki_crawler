import re
import urllib.request
import logging
import time
from bs4 import BeautifulSoup

def get_congress_urls():
    
    base_wiki_url = "https://en.wikipedia.org"
    start_url = "https://en.wikipedia.org/wiki/List_of_United_States_Congresses"
    connect_error_msg = 'ERROR: Could not connect to ' + start_url

    urls = []
    page_found = False
    
    try:
        page = urllib.request.urlopen(start_url)
        page_found = True
    except:
        logging.error(connect_error_msg)

    if(page_found == True):
        soup = BeautifulSoup (page, 'html.parser')
        th_elements_str = str(soup.find_all("th"))

        url_pattern = re.compile(r'/wiki/(\d\d\d|\d\d|\d)(st|nd|rd|th)_United_States_Congress')
        url_matches = url_pattern.finditer(th_elements_str)
        
        for match in url_matches:
            urls.append(base_wiki_url + match.group(0))
        
    return urls


def crawl_urls(urls):
    congresses = []
    page_counter = 0
    urls = urls[0:5] # shorter url list for testing

    for url in urls:
        page_found = False
        congress_data = []

        connect_error_msg = 'ERROR: Could not connect to ' + url
        try:
            page = urllib.request.urlopen(url).read()
            page_found = True
            page_counter = page_counter + 1
        except:
            logging.error(connect_error_msg)

        if page_found == True:
            soup = BeautifulSoup(page, 'html.parser')

            # get congress start date
            # four_digit_years = []
            first_paragraph = soup.find('p').findNext('p').findNext('p').get_text()
            print(first_paragraph)
                
            # parse congress members
            table_data = soup.find_all('table', {'role': 'presentation'})
            for table in table_data:
                list_items = table.find_all('li')
                for item in list_items:
                    links = item.find_all('a', href=True)
                    for link in links:
                        congress_data.append(link)

            # filter out links titled "At-large"
            # title=re.compile(r'')
            # filter out any link with a title that has a number?

            congresses.append(congress_data)
            time.sleep(1.0)
        
        print("Pages crawled: " + str(page_counter))
        logging.info("Pages crawled: " + str(page_counter))
        time.sleep(1.0)
        
    time.sleep(1.0)
    return congresses


def main():

    urls = get_congress_urls()

    if urls:
        print(len(urls))
        logging.info("Starting crawling process...")
        congress_data = crawl_urls(urls)
        logging.info("Number of returned pages" + str(len(congress_data)))
        # print(congress_data)
    else:
        print("No URLs found. Exiting...")
        exit()


main()
