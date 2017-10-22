import requests
import random
import string
import subprocess
import os
import platform
import tempfile
import time

LOCAL_URL = 'https://80015935.ngrok.io'
WEB_URL = 'http://pawprint.dirt.io/found'
REQUEST_URL = 'https://eastus.api.cognitive.microsoft.com/vision/v1.0/describe?maxCandidates=1'
API_KEY = '7b86593b414d4a5eb5096115cf2f7d55'


def generate_random(n=8):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


def generate_random(n=8):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


def detect_doggo(url, img_data):
    file_name = generate_random() + '.jpg'
    with open('static/img/' + file_name, 'wb') as f:
        f.write(img_data)
    #
    dog_found = False
    cat_found = False
    #
    # #c = 'detection.bat '+file_name
    # is32bit = (platform.architecture()[0] == '32bit')
    # system32 = os.path.join(os.environ['SystemRoot'],
    #                         'SysNative' if is32bit else 'System32')
    # bash = os.path.join(system32, 'bash.exe')
    #
    # c = 'cd darknet/ && ./darknet detector test cfg/voc.data cfg/tiny-yolo-voc.cfg tiny-yolo-voc.weights ../static/img/'+file_name
    #
    # process = subprocess.Popen('"%s" -c "%s"' % (bash, c,), stdout=subprocess.PIPE, shell=True)
    # stdout = process.communicate()[0]
    # print 'STDOUT:{}'.format(stdout)
    #
    # resp = stdout
    #
    # print resp
    #
    # if 'dog' in resp:
    #     dog_found = True
    # elif 'cat' in resp:
    #     cat_found = True
    #
    # print 'loading...'
    #
    # if dog_found or cat_found:

    r = requests.post(REQUEST_URL,
                      headers={'Content-Type': 'application/octet-stream',
                               'Ocp-Apim-Subscription-Key': '7b86593b414d4a5eb5096115cf2f7d55'},
                      data=img_data).json()
    print r

    if 'dog' in r['description']['tags']:
        dog_found = True
    if 'cat' in r['description']['tags']:
        cat_found = True

    if dog_found or cat_found:
        r = requests.post(WEB_URL, json={'isDogFound': dog_found, 'isCatFound': cat_found, 'url': url, 'image': LOCAL_URL+'/img/'+file_name})
        print r.text
    else:
        os.remove('static/img/'+file_name)
    # else:
    #     print 'Not Found'
    #     os.remove('static/img/'+file_name)