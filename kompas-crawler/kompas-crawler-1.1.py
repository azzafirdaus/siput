
# coding: utf-8

# In[4]:

from bs4 import BeautifulSoup
from datetime import timedelta, date, datetime
import urllib.request, urllib.parse, re, json, sys

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

#bikin class crawler dengan parameter inputnya adalah url
def kompas_crawler(myurl, namaFile = None):
    #bikin list buat hasil pencarian
    try:
        urllib.request.urlopen(myurl)
    except Exception as e:
        pass
    
    #bikin soup buat parsing html dari url
    soup = BeautifulSoup((urllib.request.urlopen(myurl)).read(), "lxml")

    daftar = []
    documents = []
    
    #url page
    pages = soup.select('a[href*="search/news"]')
    for each_page in pages:
        try:
            urllib.request.urlopen(each_page.get('href'))
        except Exception as e:
            continue
        
        page_soup = BeautifulSoup((urllib.request.urlopen(each_page.get('href'))).read(), "lxml")
        
        page_documents = [x.a['href'] for x in page_soup.find_all('div', attrs={'class' : 'list-latest'}) if ("megapolitan" in x.a['href']) or ("nasional" in x.a['href'])]
        documents.extend(page_documents)
    
    for doc in documents:
        try:
            urllib.request.urlopen(doc+"?page=all")
        except Exception as e:
            continue
        
        #bikin soup buat parsing halaman masing-masing berita
        innerSoup = BeautifulSoup((urllib.request.urlopen(doc+"?page=all")).read(), "lxml")
        
        judul = innerSoup.find('title').get_text()
        konten = innerSoup.find("div", {"class": "kcm-read-text"}).get_text(" ", strip=True)
        #lokasi = cap(konten[0:(konten.find('komp')-1)], 20)

        #bikin dict buat nyimpen data 'Judul' dan 'Konten' suatu berita
        dictBerita = {'Konten': konten, 'Judul': judul}

        #masukin dict berita tersebut ke dalam list daftar
        daftar.append(dictBerita)

    global iterasi
    print("selesai "+ str(iterasi)+ " hari")
    iterasi += 1
    
    return daftar
    
if __name__ == "__main__":    

#     try:
#         datetime.strptime(sys.argv[1], '%Y-%m-%d')
#         datetime.strptime(sys.argv[2], '%Y-%m-%d')
#     except ValueError:
#         print("python kompas_crawler.py 'yyyy-mm-dd' 'yyyy-mm-dd'")
    
#     start_date = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
#     end_date = datetime.strptime(sys.argv[2], '%Y-%m-%d').date()
    
    start = input("tanggal mulai (yyyy-mm-dd): ")
    end = input("tanggal akhir (yyyy-mm-dd): ")
    file = input("nama file: ")
    
    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()
    
    urllib.parse.quote(':')
    iterasi = 1
    docs = []

    Url = "http://megapolitan.kompas.com/search/news/"

    for single_date in daterange(start_date, end_date):
        docs.extend(kompas_crawler(Url+single_date.strftime("%Y-%m-%d")))

    with open(file+'.json', 'w+') as output:
        json.dump(docs, output)


# In[ ]:



