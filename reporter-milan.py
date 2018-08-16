import os
import re
import pickle
import urllib2
import requests

from bs4 import BeautifulSoup

DOWNLOADS_FOLDER = 'downloads'
LINKS_CACHE_FILE = 'mp3_links_cache'

def get_mp3_links():
    if os.path.exists(LINKS_CACHE_FILE):
        with open(LINKS_CACHE_FILE, 'rb') as handle:
            links = pickle.load(handle)
            return links

    links = []

    for url in get_urls():
        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, 'html.parser')

        for a in soup.find_all('a', href=True):
            if re.findall('http', a['href']) and a['href'].endswith('.mp3'):
                links.append(a['href'])

    save_links_to_cache(links)

    return links

def get_urls():
    urls = []
    base_url = 'http://www.reportermilan.eu/'

    for page in range(1,80):
        urls.append('{}?paged={}'.format(base_url, page))

    return urls

def save_links_to_cache(links):
    with open(LINKS_CACHE_FILE, 'wb') as handle:
        pickle.dump(links, handle)

def download_mp3_file(link):
    filename = link.split('/')[-1]

    if os.path.exists('{}/{}'.format(DOWNLOADS_FOLDER, filename)):
        return filename

    mp3_file = requests.get(link, stream=True)

    with open('{}/{}'.format(DOWNLOADS_FOLDER, filename), 'wb') as handle:
        for chunk in mp3_file.iter_content(chunk_size=1024):
            if chunk:
                handle.write(chunk)
    
    return filename

def main():
    index = 1
    links = get_mp3_links()
    total = len(links)
    
    for link in links:
        filename = download_mp3_file(link)
        print 'File {} downloaded [{}/{}]'.format(filename, index, total)
        index += 1

if __name__ == '__main__':
    main()