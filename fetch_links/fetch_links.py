import requests
import xml.etree.ElementTree as ET
r = requests.get('https://www.sec.gov/rss/investor/alerts')
root = ET.fromstring(r.text)
for link in [x.text for x in root.findall('.//channel/item/link')]:
	print(link)

