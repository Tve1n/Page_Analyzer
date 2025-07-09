from bs4 import BeautifulSoup


def get_data(text):
    soup = BeautifulSoup(text, 'xml')
    title = soup.find('title').text if soup.find('title') else ''
    h1 = soup.h1.get_text() if soup.h1 else ''
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag.get('content') if description_tag else ''
    return h1, title, description
