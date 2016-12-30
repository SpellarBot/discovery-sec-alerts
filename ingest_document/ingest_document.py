import requests
import xml.etree.ElementTree as ET
import flask,json,tempfile
from watson_developer_cloud import DiscoveryV1

app = flask.Flask('Whisk Link Fetcher')

@app.route('/init',methods=['POST'])
def init():
  return flask.Response(response='{}',
                        status=200,
                        mimetype='application/json')

@app.route('/run', methods=['POST'])
def main():
  params = flask.request.get_json()
  if 'username' in params and 'password' in params:
    discovery = DiscoveryV1('2016-12-15',
                            username=params['username'],
                            password=params['password'])
    doc_data = requests.get(params['url'])

    tmpfile = tempfile.NamedTemporaryFile(mode="w+t")
    tmpfile.write(doc_data.text.encode('utf8'))
    tmpfile.flush()
    tmpfile.seek(0)
    
    add_results = discovery.add_document(
      environment_id=params['environment_id'],
      collection_id=params['collection_id'],
      fileinfo=tmpfile)
    dict_result = {'result': add_results }
    json_results = json.dumps(dict_result)
    return flask.Response(response=json_results,
			  status=200,
			  mimetype='application/json')
  else:
    dict_result = {'result': 'No WDS Username/Password' }
    return flask.Response(response=json_results,
			  status=500,
			  mimetype='application/json')
