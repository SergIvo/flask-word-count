import requests
from bs4 import BeautifulSoup as bs
import asyncio
import aiohttp

LINK = 'https://www.multitran.com/m.exe?s={}&l1=2&l2=1'

def scrap_from_url(url, proxy = None):
    headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8}', 
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    session = requests.Session()
    if proxy:
        proxy_dict = {'http': proxy, 'https': proxy}
        try:
            response = session.get(url, proxies = proxy_dict, headers = headers)
        except:
            return None
    else:
        response = session.get(url, headers = headers)
    print(response.status_code)
    if response.status_code == 200:
        soup = bs(response.content, 'lxml')
        translation = soup.find('td', attrs = {'class': 'trans'})
        if translation:
            print('Got it. ', translation)
        return translation
    else:
        return None
        
def translate_word(word, proxy = None):
    link = 'https://www.multitran.com/m.exe?s={}&l1=2&l2=1'.format(word)
    translation = scrap_from_url(link, proxy)
    return translation
    
#Further all functions are asynchronios
async def async_scrap(session, url, proxy = None):
    if proxy:
        try:
            response = await session.get(url, proxy = proxy)
        except:
            return None
    else:
        response = await session.get(url)
    print(response.status)
    if response.status == 200:
        result = await response.read()
        return result.decode('utf8')
    else:
        return None

async def async_translate(word, proxy = None):
    headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8}', 
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    link = 'https://www.multitran.com/m.exe?s={}&l1=2&l2=1'.format(word)
    async with aiohttp.ClientSession(headers = headers) as session:
        response = await async_scrap(session, link, proxy)
        return {'word': word, 'translation': response}

def multitran(words, proxy = None):
    ioloop = asyncio.new_event_loop()
    asyncio.set_event_loop(ioloop)
    coros = [async_translate(word) for word in words]
    results = ioloop.run_until_complete(asyncio.gather(*coros))
    ioloop.close()
    translated = []
    for result in results:
        print('Translating "{}"'.format(result['word']))
        soup = bs(result['translation'], 'lxml')
        try:
            contents = soup.find('td', attrs = {'class': 'trans'}).find_all('a')
            result['translation'] = ';\n'.join([tag.text for tag in contents if tag.text])
        except AttributeError:
            result['translation'] = 'Not found'
        translated.append(result)
    return translated
    

if __name__ == '__main__':
    words = "Let's test it".split()
    tr = multitran(words)
    for tran in tr:
        print(tran)
