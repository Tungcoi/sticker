from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
import shutil,os, json
import _thread

def xstr(strin):
    return '' if strin is None else str(strin)

def downloadpage(pagenumber):
    site = 'https://tlgrm.eu/stickers?page={}'.format(pagenumber)
    print('parsing page ', site)
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')
    jsondata = {}
    jsondata['android_play_store_link'] = ''
    jsondata['ios_app_store_link'] = ''
    jsondata['sticker_packs'] = []
    for link in soup.find_all('script'):
        if 'window.preloaded_page' in link.text:
            jstext = json.loads(link.text[link.text.find('{'):link.text.rfind(';')])
            for ff in jstext['data']:
                stickerdata = {}
                stickerdata['identifier'] = ''.join(e for e in ff['uuid'] if e.isalnum())
                stickerdata['name'] = xstr(ff['name_en']).rstrip()
                stickerdata['publisher'] = xstr(ff['author'])
                stickerdata['tray_image_file'] = 'thumb128.png'
                stickerdata['publisher_email'] = ''
                stickerdata['publisher_website'] = ''
                stickerdata['privacy_policy_website'] = ''
                stickerdata['license_agreement_website'] = ''
                stickerdata['stickers'] = []
                count = ff['count']

                for i in range(count):
                    sticker = {}
                    sticker['image_url'] = 'http://s.tcdn.co/{}/{}/{}/{}.png'.format(ff['uuid'][:3], ff['uuid'][3:6] ,ff['uuid'], i+1)
                    sticker['image_file'] = ''
                    sticker['emojis'] = []
                    stickerdata['stickers'].append(sticker)
                jsondata['sticker_packs'].append(stickerdata)
            break
    with open('contents.json', 'w') as content:
        json.dump(jsondata,content, sort_keys=True, indent=4, separators=(',', ': '))


def main():
    for pagecount in range(1):
        downloadpage(pagecount + 1)
        
    
if __name__ == "__main__":
    main()