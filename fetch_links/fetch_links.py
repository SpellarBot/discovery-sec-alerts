import requests
import xml.etree.ElementTree as ET
import flask,json

app = flask.Flask('Whisk Link Fetcher')

@app.route('/init',methods=['POST'])
def init():
  return flask.Response(response='{}',
                        status=200,
                        mimetype='application/json')

@app.route('/run', methods=['POST'])
def main():
  params = flask.request.get_json()
  r = None
  if 'url' in params:
    r = requests.get(params['url'])
  else:
    r = requests.get('https://www.sec.gov/rss/investor/alerts')
          
  root = ET.fromstring(r.text)
  return json.dumps([x.text
                     for x
                     in root.findall('.//channel/item/link')])
