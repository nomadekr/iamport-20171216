import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askdjango.settings')

import requests
from bs4 import BeautifulSoup
from django.core.files import File

import django
django.setup()

from shop.models import Item


def trim(s):
    return ' '.join(s.split())


def main():
    params = dict(
        query='닌텐도스위치',
        cat_id='',
        frm='NVSHATC'
    )

    url = 'https://search.shopping.naver.com/search/all.nhn'
    res = requests.get(url, params=params)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup.select('.goods_list ._itemSection'):
        name = trim(tag.select('.tit')[0].text)
        amount = trim(tag.select('.price .num')[0].text).replace(',', '')
        img_url = tag.select('.img > img')[0]['data-original']
        img_name = os.path.basename(img_url.split('?')[0])
        img_res = requests.get(img_url, stream=True)

        item = Item(name=name, amount=amount)
        item.photo.save(img_name, File(img_res.raw))
        item.save()

        print('saved #{}'.format(item.pk))


if __name__ == '__main__':
    main()
