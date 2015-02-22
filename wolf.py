import urllib2
import urllib
import httplib
import re
import sys
from xml.etree import ElementTree as etree
 
class wolfram(object):
    def __init__(self, appid):
        self.appid = appid
        self.base_url = 'http://api.wolframalpha.com/v2/query?'
        self.headers = {'User-Agent':None}
 
    def _get_xml(self, ip):
        url_params = {'input':ip, 'appid':self.appid}
        data = urllib.urlencode(url_params)
        req = urllib2.Request(self.base_url, data, self.headers)
        xml = urllib2.urlopen(req).read()
        return xml
 
    def _xmlparser(self, xml):
        data_dics = {}
        tree = etree.fromstring(xml)
        #retrieving every tag with label 'plaintext'
        for e in tree.findall('pod'):
            if(sys.argv[1] == 'plot'):
                print('test1')
                if e.attrib.get("title") == 'Plot' or e.attrib.get("title") == 'Plots':
                    print('test2')
                    for item in [ef for ef in list(e) if ef.tag=='subpod']:
                        print('test3')
                        for it in [i for i in list(item) if i.tag=='img']:
                            print('test4')
                            if it.tag=='img':
                                return it
                                # data_dics[e.get('title')] = it

            elif(sys.argv[1] == 'compute'):
                if e.attrib.get("title") == 'Result' or e.attrib.get("title") == 'Decimal approximation' or e.attrib.get("title") == 'Exact result':
                    for item in [ef for ef in list(e) if ef.tag=='subpod']:
                        for it in [i for i in list(item) if i.tag=='plaintext']:
                            if it.tag=='plaintext':
                                return it
                            # data_dics[e.get('title')] = it
            elif(sys.argv[1] == "chemName"):
                if e.attrib.get("title") == 'Input interpretation':
                    for item in [ef for ef in list(e) if ef.tag=='subpod']:
                        for it in [i for i in list(item) if i.tag=='img']:
                            if it.tag=='img':
                                return it
            elif(sys.argv[1] == "chemProperties"):
                if e.attrib.get("title") == 'Basic properties':
                    for item in [ef for ef in list(e) if ef.tag=='subpod']:
                        for it in [i for i in list(item) if i.tag=='img']:
                            if it.tag=='img':
                                return it
            elif(sys.argv[1] == "chemStruct"):
                if e.attrib.get("title") == 'Structure diagram':
                    for item in [ef for ef in list(e) if ef.tag=='subpod']:
                        for it in [i for i in list(item) if i.tag=='img']:
                            if it.tag=='img':
                                return it
               
        return 0
 
    def search(self, ip):
        mode = sys.argv[1]
        if(mode =='Plots'): 
            mode = 'Plot'
        xml = self._get_xml(ip)
        result_dics = self._xmlparser(xml)
        
        element = result_dics

        if element == 0:
            print("/images/none.png")
            exit()


        if(mode == 'compute'):
              # m = re.search(r"(.*\.[0-9]{2})", element.text)
            # print(m.group(1))
            print(element.text.encode('utf-8'))
        else:
            imgURL = (element.attrib.get("src"))
            print(imgURL.encode('utf-8'))
            # urllib.urlretrieve(imgURL, mode + '.jpg')

 
if __name__ == "__main__":
    appid = 'RR8GTK-8EVGK6Y5Y3'
    query = ' '.join(sys.argv[2:])
    w = wolfram(appid)
    w.search(query)




