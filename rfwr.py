import xml.etree.ElementTree as ET
from bottle import route, run, template, debug
from bottle import get, post, request
import raumfeld
from bottle import static_file
import os
import collections

### Define your music zone here. The zones are alpahbetically sorted by names (0 = A-Zone, 1 = B-Zone)
l_zone = 0

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def read_favs(no=1):
	with open('favorites', 'a+') as f:
	    	content = f.readlines()
	alternater = 0
	counter = 0
	URIs = []
	Meta = []
	for line in content:
		if alternater == 0:
			URIs.append(line)
			alternater = 1
		else:
			Meta.append(line)
			alternater = 0
		counter = counter + 1
	URIs = [each.replace('\n', '') for each in URIs]
	Meta = [each.replace('\n', '') for each in Meta]

	for i in range(1,len(URIs)):
		if Meta[i] == '':
			Meta[i] = ''.join(['<DIDL-Lite xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dlna="urn:schemas-dlna-org:metadata-1-0/" xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" xmlns:raumfeld="urn:schemas-raumfeld-com:meta-data/raumfeld"><container><dc:title>',URIs[i],'</dc:title></container></DIDL-Lite>'])

	no = int(no) - 1

	trees = [ET.fromstring(each) for each in Meta]
	namespaces = {'dc': 'http://purl.org/dc/elements/1.1/'}
	titles = [tree[0].find('dc:title', namespaces).text for tree in trees]

	return no, URIs, Meta, titles

@route('/vol/<no>')
def vol(no):
	devices = raumfeld.discover()
	if len(devices) > 0:
		speaker = devices[l_zone]
		speaker.mute = False
		speaker.volume = int(no)
	else:
		return 'No devices found.'
	return '''
	Volume set.
	<script language="javascript">
    		window.location.href = "/player"

	</script>
	'''

@route('/images/<filename:re:.*\.*>')
def send_image(filename):
        return static_file(filename, root='images/', mimetype='image/png')

@route('/')
def index():
	return '''
	<script language="javascript">
    		window.location.href = "/player"
	</script>
	'''

@route('/zone/<no>')
def zone(no):
	global l_zone
	l_zone = int(no)
	return '''
	<script language="javascript">
    		window.location.href = "/player"

	</script>

	'''

@route('/zones')
def zones():
	global l_zone
	devices = raumfeld.discover()
	zones = [device.friendly_name for device in devices]
	print(zones)
	return template('''
	<html>
	Active Zone: {{l_zone}}<br>
	%for i in range(0,len(zones)):
		{{i}}: <a href="/zone/{{i}}">{{zones[i]}}</a><br>
	%end
	</html>
	''', zones=zones, l_zone=l_zone)



@route('/pause')
def pause():
	devices = raumfeld.discover()
	if len(devices) > 0:
		speaker = devices[l_zone]
		speaker.pause()
	else:
		return 'No devices found.'
	return '''
	<script language="javascript">
    		window.location.href = "/player"
	</script>
	'''

@route('/next')
def next():
	devices = raumfeld.discover()
	if len(devices) > 0:
		speaker = devices[l_zone]
		speaker.next()
	else:
		return 'No devices found.'
	return '''
	<script language="javascript">
    		window.location.href = "/player"
	</script>
	'''

@route('/previous')
def next():
	devices = raumfeld.discover()
	if len(devices) > 0:
		speaker = devices[l_zone]
		speaker.previous()
	else:
		return 'No devices found.'
	return '''
	<script language="javascript">
    		window.location.href = "/player"
	</script>
	'''

@route('/comehome')
def comehome():
	URI = "http://dradio_mp3_dwissen_m.akacast.akamaistream.net/7/728/142684/v1/gnl.akacast.akamaistream.net/dradio_mp3_dwissen_m"
	devices = raumfeld.discover()
	if len(devices) > 0:
		speaker = devices[l_zone]
		TState = speaker.curTransState
		if str(TState) == "STOPPED" or str(TState) == "PAUSED_PLAYBACK":
			speaker.mute = False
			speaker.volume = 50
			speaker.playURI(URI)
			player()
			return 'Welcome Home!'
	else:
		return 'No devices found.'

@route('/play')
def play():
	devices = raumfeld.discover()
	if len(devices) > 0:
		speaker = devices[l_zone]
		speaker.play()
	else:
		return 'No devices found.'
	return '''
	<script language="javascript">
    		window.location.href = "/player"
	</script>
	'''

@route('/playURI')
def playURI():
	return '''
		<form action="/playURI" method="post">
		    URI: <input name="URI" type="text" />
		    <input value="Submit" type="submit" />
		</form>
	'''

@post('/playURI')
def do_playURI():
	URI = request.forms.get('URI')
	URIMeta = ''.join(['<DIDL-Lite xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dlna="urn:schemas-dlna-org:metadata-1-0/" xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" xmlns:raumfeld="urn:schemas-raumfeld-com:meta-data/raumfeld"><container><dc:title>',URI,'</dc:title></container></DIDL-Lite>'])
	devices = raumfeld.discover()
	if len(devices) > 0:
		speaker = devices[l_zone]
		speaker.playURI(URI, URIMeta)
	else:
		return 'No devices found.'
	return '''
	<script language="javascript">
    		window.location.href = "/player"
	</script>
	'''

@route('/play/drwissen')
def drwissen():
	URI = "http://dradio_mp3_dwissen_m.akacast.akamaistream.net/7/728/142684/v1/gnl.akacast.akamaistream.net/dradio_mp3_dwissen_m"
	devices = raumfeld.discover()
	if len(devices) > 0:
		speaker = devices[l_zone]
		speaker.playURI(URI)
	else:
		return 'No devices found.'
	return '''
	<script language="javascript">
    		window.location.href = "/player"
	</script>
	'''

@route('/play/recentArtists')
def recentArtists():
	URI = "dlna-playcontainer://uuid%3A4f0d7a8e-680e-493a-9907-6e6cb772f0b4?sid=urn%3Aupnp-org%3AserviceId%3AContentDirectory&cid=0%2FPlaylists%2FShuffles%2FRecentArtists%2F1800068248%252B%252Bde&md=0&fii=0"
	devices = raumfeld.discover()
	if len(devices) > 0:
		speaker = devices[l_zone]
		speaker.playURI(URI)
	else:
		return 'No devices found.'
	return '''
	<script language="javascript">
    		window.location.href = "/player"
	</script>
	'''

@route('/fav/<no>')
def fav(no):
	favs = read_favs(no)
	no = favs[0]
	URIs = favs[1]
	Meta = favs[2]
	if len(URIs) == 0:
		return 'No Favorites have been set yet. Use /addfav to add a favorite.'
	elif len(URIs) <= no:
		return 'This favorite has not been set yet. Use /addfav to add a favorite.'
	favURI = URIs[no]
	favMeta = Meta[no]
	devices = raumfeld.discover()
	if len(devices) > 0:
		speaker = devices[l_zone]
		speaker.playURI(favURI, favMeta)
	else:
		return 'No devices found.'
	return '''
	<script language="javascript">
    		window.location.href = "/player"
	</script>
	'''

@route('/setfav/<no>')
def setfav(no):
	favs = read_favs(no)
	no = favs[0]
	URIs = favs[1]
	Meta = favs[2]
	if len(URIs) == 0:
		return 'No Favorites have been set yet. Use /addfav to add a favorite.'
	elif len(URIs) <= no:
		return 'This favorite has not been set yet. Use /addfav to add a favorite.'
	devices = raumfeld.discover()
	if len(devices) > 0:
		speaker = devices[l_zone]
		URIs[no] = speaker.currentURI()
		Meta[no] = speaker.currentURIMetaData()
	else:
		return 'No devices found.'
	out_list = []
	for i in range(0,len(URIs)):
		out_list.append(URIs[i])
		out_list.append(Meta[i])
	with open('favorites','w') as f:
		for item in out_list:
  			f.write("%s\n" % item)
	return '''
	<script language="javascript">
		window.setInterval(function() window.location.href = "/player", 10);
	</script>
	'''

@route('/addfav')
def addfav():
	favs = read_favs()
	URIs = favs[1]
	Meta = favs[2]
	devices = raumfeld.discover()
	if len(devices) > 0:
		speaker = devices[l_zone]
		URIs.append(speaker.currentURI())
		Meta.append(speaker.currentURIMetaData())
	else:
		return 'No devices found.'
	out_list = []
	for i in range(0,len(URIs)):
		out_list.append(URIs[i])
		out_list.append(Meta[i])
	with open('favorites','w') as f:
		for item in out_list:
  			f.write("%s\n" % item)
	return '''
	Favorite has been set.
	<script language="javascript">
    		window.location.href = "/player"
	</script>
	'''

@route('/info')
def info():
	devices = raumfeld.discover()
	if len(devices) > 0:
		speaker = devices[l_zone]
		curURI = speaker.currentURI()
		curMeta = speaker.currentURIMetaData()
		trackURI = speaker.trackURI()
		trackMeta = speaker.trackMetaData()
	else:
		return 'No devices found.'

	print(type(curURI))
	return template('''
		<html>
			<body>

				CurrentURI:<br> {{curURI}} <br> <br>
				CurrentMetaData:<br> {{curMeta}}<br> <br>

				TrackURI:<br> {{trackURI}} <br> <br>
				TrackMetaData:<br> {{trackMeta}}<br> <br>

				Devices / Music Zones:<br> {{devices}}
				<br><br><a href="/player">Back to Player</a>
			</body>

		</html>
	''', curURI=curURI, curMeta=curMeta, trackURI=trackURI, trackMeta=trackMeta, devices=devices)

@route('/player')
def player():
	favs = read_favs()
	URIs = favs[1]
	Meta = favs[2]
	fav_count = range(1,len(URIs) + 1)
	titles = favs[3]
	return template('player', fav_count = fav_count, titles = titles)


#debug(True)
run(host='0.0.0.0', port = 8080)#, reloader = True)
