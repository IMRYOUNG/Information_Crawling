import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
from itertools import count
from selenium import webdriver
import ssl  #추가


def get_request_url(url, enc='utf-8'):
    
    req = urllib.request.Request(url)

    try:
        ssl._create_default_https_context = ssl._create_unverified_context    #추가
        
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            try:                  
                rcv = response.read()
                ret = rcv.decode(enc)
            except UnicodeDecodeError:
                ret = rcv.decode(enc, 'replace')    
            
            return ret
            
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None
    
def GoobneAddress(result):
    Goobne_URL = 'http://www.goobne.co.kr/store/search_store.jsp'    
    wd = webdriver.Chrome("C:/Users/Administrator/AppData/Local/Programs/Python/Python37-32/webDriver/chromedriver.exe")
    wd.get(Goobne_URL)
    time.sleep(10)

    for page_idx in count():        
        wd.execute_script("store.getList('%s')" % str(page_idx + 1))
        print ("PageIndex [%s] Called" % (str(page_idx + 1)))
        time.sleep(5)
 
        rcv_data = wd.page_source        
        soupData = BeautifulSoup(rcv_data, 'html.parser')        
        for store_list in soupData.findAll('tbody', attrs={'id': 'store_list'}):
            for store_tr in store_list:
                tr_tag = list(store_tr.strings)
                if (tr_tag[0] == '등록된 데이터가 없습니다.'):
                   return result               
                store_name = tr_tag[1]
                if (tr_tag[3] == ''):
                    store_address = tr_tag[5]
                else:
                    store_address = tr_tag[6]
                store_sido_gu = store_address.split()[:2]
                result.append([store_name] + store_sido_gu + [store_address])

        #print(tr_tag)

    return

def cswin_Goobne ():

    result = []

    print('GOOBNE ADDRESS CRAWLING START')
    GoobneAddress(result)
    goobne_table = pd.DataFrame(result, columns=('store', 'sido', 'gungu', 'store_address'))
    goobne_table.to_csv("./goobne.csv", encoding="cp949", mode='w', index=True)

    print('FINISHED')
    



if __name__ == '__main__':
     cswin_Goobne ()

