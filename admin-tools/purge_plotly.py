import os
import sys
import plotly
import plotly.plotly as py
import json
import requests
from requests.auth import HTTPBasicAuth


def get_pages(username, page_size):
    url = 'https://api.plot.ly/v2/folders/all?user='+username+'&page_size='+str(page_size)
    response = requests.get(url, auth=auth, headers=headers)
    response.raise_for_status()
    if response.status_code != 200:
        print('Received an error: {}'.format(response.status_code))
        return
    page = response.json()
    yield page
    while True:
        resource = page['children']['next'] 
        if not resource:
            break
        response = requests.get(resource, auth=auth, headers=headers)
        if response.status_code != 200:
            print('Received an error: {}'.format(response.status_code))
            break
        page = response.json()
        yield page

        
def permanently_delete_files(username, page_size=500, filetype_to_delete='plot'):
    for page in get_pages(username, page_size):
        for x in range(0, len(page['children']['results'])):
            fid = page['children']['results'][x]['fid']
            response = requests.get('https://api.plot.ly/v2/files/' + fid, auth=auth, headers=headers)
            response.raise_for_status()
            if response.status_code == 200:
                json_res = response.json()
                if json_res['filetype'] == filetype_to_delete:
                    print('Removing {} {}'.format(filetype_to_delete, fid))
                    requests.post('https://api.plot.ly/v2/files/'+fid+'/trash', auth=auth, headers=headers)  # move to trash
                    requests.delete('https://api.plot.ly/v2/files/'+fid+'/permanent_delete', auth=auth, headers=headers)  # permanently delete


username = os.environ.get('PLOTLY_USERNAME')
api_key = os.environ.get('PLOTLY_APIKEY')
print('Working on user {}'.format(username))
print(username, api_key)
auth = HTTPBasicAuth(username, api_key)
headers = {'Plotly-Client-Platform': 'python'}
plotly.tools.set_credentials_file(username=username, api_key=api_key)
permanently_delete_files(username, filetype_to_delete='plot')
permanently_delete_files(username, filetype_to_delete='grid')
