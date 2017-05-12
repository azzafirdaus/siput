
# coding: utf-8

# In[2]:

from pymongo import MongoClient
import pymongo, re, json

# function stopwords buat misahin antara stopwords dan lexicon
def stopwords_remove(document):
    stopwords = [line.strip() for line in open("stopwords_list_tala.txt", 'r')]
    
    list_words = [x for x in re.split('\W+', str.lower(document)) if not (x.isdigit())]
    
    for word in list_words:
        if word in stopwords:
            list_words = list(filter((word).__ne__, list_words))
            
    list_words = list(filter(('').__ne__, list_words))
    return list_words        
        
# buat masukin term ke mongodb lexicon beserta frekuensinya
def insert_lexicon(lists):
    for word in set(lists):
        db.terms.update_one({'Term': word}, {'$inc':{'DF':1}}, upsert=True)
        
if __name__ == "__main__":   
    print("Selamat datang!")
    print("Pastikan server mongo anda sudah berjalan")
    
    client = MongoClient()
    db = client.word_df
    collection = db.terms
    
    file = input("file data yang akan di masukan: ")
    docs = json.loads(open(file).read())
    
    for doc in docs:
        removed = stopwords_remove(doc['Konten'])
        insert_lexicon(removed)
        
    print("Data telah berhasil dimasukkan ke dalam mongo")
    print("Nama Database: word_df")
    print("Nama Collection: terms")


# In[ ]:



