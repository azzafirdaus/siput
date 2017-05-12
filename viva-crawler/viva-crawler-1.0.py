
# coding: utf-8

# In[1]:

from bs4 import BeautifulSoup
from datetime import timedelta, date, datetime
import urllib.request, urllib.parse, re, json, sys

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

#bikin class crawler dengan parameter inputnya adalah url
def viva_crawler(myurl, namaFile = None):
    try:
        urllib.request.urlopen(myurl)
    except Exception as e:
        pass
    
    #bikin list buat hasil pencarian
    daftar = []
    documents = []
    
    #url page
    for each_page in range(1,4):
        try:
            urllib.request.urlopen(myurl+"?page="+str(each_page))
        except Exception as e:
            continue
        
        page_soup = BeautifulSoup(urllib.request.urlopen(myurl+"?page="+str(each_page)).read(), "lxml")
        
        page_documents = page_soup.find_all('a', href=re.compile("read"), target=False)
        documents.extend(page_documents)
    
    for doc in documents:
        try:
            urllib.request.urlopen(doc.get('href'))
        except Exception as e:
            continue
        
        #bikin soup buat parsing halaman masing-masing berita
        innerSoup = BeautifulSoup((urllib.request.urlopen(doc.get('href'))).read(), "lxml")
        
        judul = innerSoup.find('title').get_text()
        
        konten = innerSoup.find("span", {"itemprop": "description"}).get_text(" ", strip=True)
             
        #bikin dict buat nyimpen data 'Judul' dan 'Konten' suatu berita
        dictBerita = {'Konten': konten, 'Judul': judul}

        #masukin dict berita tersebut ke dalam list daftar
        daftar.append(dictBerita)
 
    global iterasi
    print("selesai hari ke "+ str(iterasi))
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
    file = input("nama file untuk menyimpan: ")
    
    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()
    
    urllib.parse.quote(':')
    iterasi = 1
    docs = []

    Url = "http://www.viva.co.id/indeks/berita/politik/"

    for single_date in daterange(start_date, end_date):
        docs.extend(viva_crawler(Url+single_date.strftime("%Y/%m/%d")))
    
    with open(file+'.json', 'w+') as output:
        json.dump(docs, output)


# In[22]:

angka = 1
for a in docs:
    print(str(angka)+")")
    print(a['Judul'])
    print(a['Konten'])
    angka += 1


# In[25]:

with open('viva_politik(29 Feb - 31 mar).txt', 'w+') as output:
    json.dump(docs, output)


# In[8]:

text = "http://www.viva.co.id/indeks/berita/politik/2016/4/2"

for a in range(1, 4):
    print(text+"?page="+str(a))


# In[24]:

print(len(docs))


# In[ ]:



