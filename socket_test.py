from gevent import monkey; monkey.patch_all()
from bottle import request, Bottle, abort
import xml.etree.ElementTree as ET
import raumfeld
from gevent import queue, sleep

app = Bottle()


zones = raumfeld.discover()

def time_getter():
    try:
        absTime = str(zones[0].trackAbsTime())
        duration = str(zones[0].trackDuration())
    except :
        duration = '00:00:00'
        absTime = '00:00:00'
    return absTime, duration

def data_getter():
    namespaces = {'dc':'http://purl.org/dc/elements/1.1/','upnp':'urn:schemas-upnp-org:metadata-1-0/upnp/','raumfeld':'urn:schemas-raumfeld-com:meta-data/raumfeld/'}
    trackMeta = zones[0].trackMetaData()
    trackMeta_tree = ET.fromstring(unicode(trackMeta).encode('utf8'))
    try:
        track_img = trackMeta_tree[0].find('upnp:albumArtURI', namespaces).text
    except:
        track_img = '/images/audio_www.png'
    try:
        track_title = trackMeta_tree[0].find('dc:title', namespaces).text
    except:
        track_title = 'Unknown'
    try:
        track_album = trackMeta_tree[0].find('upnp:album', namespaces).text
        track_artist = trackMeta_tree[0].find('upnp:artist', namespaces).text
    except:
        track_album = ''
        track_artist = ''
    return track_title, track_img, track_artist, track_album

def ws_maker():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    absTime_old = ''
    old_track_title = '_Old__Title_'

    while 1:
        sleep(0.333333)
        try:
            ws_ms_short = time_getter()
            ws_ms_error_list = ['ws_ms_short Success!']

            try:
                ws_ms_long = data_getter()
                ws_ms_error_list.append('ws_ms_long Success!')
            except:
                ws_ms_long = ['', 'http://lorempixel.com/300/300/nightlife/broken', '','','']

            if old_track_title != ws_ms_long[3]:
                ws_ms = "l|||" + "|||".join(ws_ms_short) + "|||" + "|||".join(ws_ms_long)
                old_track_title = ws_ms_long[3]
                ws_ms_error_list.append(ws_ms)

            else:
                ws_ms = "s|||" + "|||".join(ws_ms_short)
                ws_ms_error_list.append(ws_ms)

            wsock.send(ws_ms)
        except:
            ws_ms_error = ",".join(ws_ms_error_list)
            wsock.send(ws_ms_error)

# This creates a queue object for every request.

@app.route('/websocket')
def handle_websocket():
    body = queue.Queue()
    worker = ws_maker()
    worker.on_data(body.put)
    worker.on_finish(lambda: body.put(StopIteration))
    worker.start()
    return body


from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
server = WSGIServer(("0.0.0.0", 8081), app,
                    handler_class=WebSocketHandler)
server.serve_forever()
