# import urllib
# import re
# from lxml import html

# url = "http://api.wolframalpha.com/v2/query?appid=RR8GTK-8EVGK6Y5Y3&input=y%3Dx^2&format=image,plaintext"
# page = html.fromstring(urllib.urlopen(url).read())



# toSearch = html.tostring(page)


# print(toSearch)
# match = re.search(r"(Plot)", toSearch)

# refinedString = toSearch[match.start(1):]


# imgStart = refinedString[(re.search(r"(<img src=\")", refinedString).start(1)+len("<img src=\"")):]

# imgURL = imgStart[:re.search((r"(\")"), imgStart).start(1)]

# print(imgURL)
# imgURL = imgURL.replace("&amp;","&")
# print(imgURL)

# urllib.urlretrieve(imgURL, "toDisplay.jpg")





        

# import wolframalpha
# import sys

# client = wolframalpha.Client('RR8GTK-8EVGK6Y5Y3')
# res = client.query('y=x')
# for pod in res.pods:
#   for a in pod:
#       if '<img src' in a:
#           print a



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
                if e.attrib.get("title") == 'Plot' or e.attrib.get("title") == 'Plots':
                    for item in [ef for ef in list(e) if ef.tag=='subpod']:
                        for it in [i for i in list(item) if i.tag=='img']:
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
            elif(sys.argv[1] == "chem"):
                if e.attrib.get("title") == 'Result' or e.attrib.get("title") == 'Decimal approximation' or e.attrib.get("title") == 'Exact Result':
                    for item in [ef for ef in list(e) if ef.tag=='subpod']:
                        for it in [i for i in list(item) if i.tag=='plaintext']:
                            if it.tag=='plaintext':
                                return it

    
        return data_dics
 
    def search(self, ip):
        xml = self._get_xml(ip)
        result_dics = self._xmlparser(xml)
        
        element = result_dics
        # if 'Plot' in result_dics.keys():
        #   element = result_dics['Plot']
        # elif 'Plots' in result_dics.keys():
        #   element = result_dics['Plots']
        # else: 
        #   print("sorry no graph")
        #   exit()
        if(sys.argv[2]=='Plot' or sys.argv[2]=='Plots'):
            imgURL = (element.attrib.get("src"))
            print(imgURL)
            urllib.urlretrieve(imgURL, "toDisplay.jpg")
        else:
            # m = re.search(r"(.*\.[0-9]{2})", element.text)
            # print(m.group(1))
            print(element.text)

 
if __name__ == "__main__":
    appid = 'RR8GTK-8EVGK6Y5Y3'
    query = ' '.join(sys.argv[2:])
    w = wolfram(appid)
    w.search(query)







# # import urllib2
# # import sys
# # import urllib
# # import httplib
# # from xml.etree import ElementTree as etree

# # class wolfram(object):
# #     def __init__(self, appid):
# #         self.appid = appid
# #         self.base_url = 'http://api.wolframalpha.com/v2/query?'
# #         self.headers = {'User-Agent':None}
# #     def _get_xml(self, ip):
# #         url_params = {'input':ip, 'appid':self.appid}
# #         data = urllib.urlencode(url_params)
# #         req = urllib2.Request(self.base_url, data, self.headers)
# #         xml = urllib2.urlopen(req).read()
# #         return xml
# #     def _xmlparser(self, xml):
# #         data_dics = {}
# #         tree = etree.fromstring(xml)
# #         #retrieving every tag with label 'plaintext'
# #         for e in tree.findall('pod'):
# #             for item in [ef for ef in list(e) if ef.tag=='subpod']:
# #                 for it in [i for i in list(item) if i.tag=='plaintext']:
# #                     if it.tag=='plaintext':
# #                         mykey = e.get('title')
# #                         if mykey not in data_dics.keys():
# #                              data_dics[mykey] = [it.text]
# #                         else:
# #                             prev = data_dics[mykey]
# #                             data_dics[mykey] = prev + [it.text]
# #         return data_dics
# #     def search(self, ip):
# #         xml = self._get_xml(ip)
# #         result_dics = self._xmlparser(xml)
# #         #return result_dics
# #         #print result_dics
# #         print result_dics['Result']

# # if __name__ == "__main__":
# #     appid = sys.argv[0]
# #     query = sys.argv[1]
# #     w = wolfram(appid)
# #     w.search(query)
