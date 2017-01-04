import requests
import xml.etree.ElementTree as ET

def main(params):
  r = None
  if 'url' in params:
    r = requests.get(params['url'])
  else:
    r = requests.get('https://www.sec.gov/rss/investor/alerts')
          
  root = ET.fromstring(r.text)
  dict_result = {'result':[x.text
                           for x
                           in root.findall('.//channel/item/link')]}
  return dict_result
