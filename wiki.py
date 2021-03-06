from bs4 import BeautifulSoup
import mechanize
import urlparse
import sys
import wikipedia
import re

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import textwrap

br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_equiv(False)
br.addheaders = [('User-agent', 'Mozilla/5.0')] 
br.open('http://www.google.com/')   
br.select_form(name='f') 
query = "+".join(sys.argv[1:len(sys.argv)]) + 'wikipedia'

br.form['q'] = query
data = br.submit()
soup = BeautifulSoup(data.read())
urls = [urlparse.parse_qs(urlparse.urlparse(l['href']).query)['q'][0] for l in soup.select('.r a')]

for i in range(0,len(urls)):
    if 'wikipedia' in urls[i]:
        wikiPageURL = urls[i]
        break
    
if not wikiPageURL:
	print("Couldn't find anything for you!")
	exit()

match = re.search(r"(wiki/)",wikiPageURL)
wikiPage = wikiPageURL[match.start(1)+len("wiki/"):]

# info = textwrap.wrap(wikipedia.summary(wikiPage, sentences = 3), width = 60)

print(wikipedia.summary(wikiPage,sentences = 3).encode('utf-8'))



# font = ImageFont.load_default()
# img=Image.new("RGBA", (600,600),(255,0,0,0))
# draw = ImageDraw.Draw(img)

# margin = offset = 40
# for line in info:
#     draw.text((margin, offset), line, font=font, fill="#aa0000")
#     offset += font.getsize(line)[1]

# draw = ImageDraw.Draw(img)
# img.save("a_test.png", "GIF", transparency = 0)