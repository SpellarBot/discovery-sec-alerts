import requests
import xml.etree.ElementTree as ET
import flask,json,tempfile, time
from watson_developer_cloud import DiscoveryV1
import couchdb

def filter_known_urls(db_url, target_urls):
    """
        @param db_url: The url of the CouchDB Server
        @param target_urls: the list of urls to ingest
        @return the list of unknown urls
    """
    couch = couchdb.Server(db_url)

    if not('sec' in couch):
        couch.create('sec')

    db = couch['sec']
    res = []
    for i in target_urls:
        # we shouldnt overload the server
        if not(i in db):
            res.append(i)
        time.sleep(.300)
    return res

def mark_urls_known(db_url, target_urls):
    couch = couchdb.Server(db_url)

    if not('sec' in couch):
        couch.create('sec')

    db = couch['sec']
    for i in target_urls:
        db[i] = dict(type='Fetch',url=i)
        # one write per second seems reasonable
        time.sleep(1)

    return len(target_urls)

class download_to_temp:

    def __init__(self, url):
        self.url = url
    def __enter__(self):
        doc_data = requests.get(self.url)

        self.tmpfile = tempfile.NamedTemporaryFile()
        self.tmpfile.write(doc_data.text.encode('utf8'))
        self.tmpfile.flush()
        self.tmpfile.seek(0)
        return self.tmpfile
    def __exit__(self, *exc_info):
        self.tmpfile.close()

app = flask.Flask('Whisk Link Fetcher')

@app.route('/init',methods=['POST'])
def init():
  return flask.Response(response='{}',
                        status=200,
                        mimetype='application/json')

@app.route('/run', methods=['POST'])
def main():
    full_params = flask.request.get_json()
    if not('value' in full_params):
        full_params['result'] = 'Params Malformed'
        json_results = json.dumps(full_params)
        return flask.Response(response=json_results,
                              status=500,
                              mimetype='application/json')

    params = full_params['value']

    if 'username' in params and 'password' in params:
        discovery = DiscoveryV1('2016-12-15',
                                username=params['username'],
                                password=params['password'])

        added = []
        added_results = []
        for i in filter_known_urls(params['db_url'], params['result']):
            with download_to_temp(i) as tmpfile:
                add_result = discovery.add_document(
                    environment_id=params['environment_id'],
                    collection_id=params['collection_id'],
                    fileinfo=tmpfile)
                added.append(i)
                added_results.append(i)

        mark_urls_known(params['db_url'],added)

        dict_results = {'result': added_results }
        json_results = json.dumps(dict_results)
        return flask.Response(response=json_results,
			                  status=200,
                              mimetype='application/json')
    else:
        params['result'] = 'No WDS Username/Password'
        json_results = json.dumps(params)
        return flask.Response(response=json_results,
			                  status=500,
                              mimetype='application/json')
