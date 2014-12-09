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
		window.setInterval(function() window.location.href = "/player", 7000);
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
	return template(
		'''
		<html>
			<head>
				<title>rf.wr.py</title>
				<style type="text/css"><!--A{text-decoration:none}--></style>
				<link rel="icon" href="/images/play.png">
			</head>
			<body>

<table cellpadding="0" border="0" cellspacing="0">
  <tr>
    <td><a href="/prev"><img alt=" " src="images/playprevpausenext_0_0.png" style="width: 196px;  height: 155px; border-width: 0px;"></td>
    <td><a href="/play"><img alt=" " src="images/playprevpausenext_0_1.png"  style="width: 124px; height: 155px; border-width: 0px;"></a></td>
    <td><a href="/pause"><img alt=" " src="images/playprevpausenext_0_2.png"  style="width: 123px; height: 155px; border-width: 0px;"></a></td>
    <td><a href="/next"><img alt=" " src="images/playprevpausenext_0_3.png" style="width: 199px;  height: 155px; border-width: 0px;"></td>
</tr>

</table>

				
				<table cellpadding="0" border="0" cellspacing="0">
				  <tr>
				    <td><img alt=" " src="images/slice_0_0.gif" style="width: 63px;  height: 98px; border-width: 0px;"></td>
				    <td><a href="/vol/25"><img alt=" " src="images/slice_0_1.gif"  style="width: 41px; height: 98px; border-width: 0px;"></a></td>
				    <td><a href="/vol/30"><img alt=" " src="images/slice_0_2.gif"  style="width: 42px; height: 98px; border-width: 0px;"></a></td>
				    <td><a href="/vol/35"><img alt=" " src="images/slice_0_3.gif"  style="width: 42px; height: 98px; border-width: 0px;"></a></td>
				    <td><a href="/vol/40"><img alt=" " src="images/slice_0_4.gif"  style="width: 41px; height: 98px; border-width: 0px;"></a></td>
				    <td><a href="/vol/45"><img alt=" " src="images/slice_0_5.gif"  style="width: 42px; height: 98px; border-width: 0px;"></a></td>
				    <td><a href="/vol/50"><img alt=" " src="images/slice_0_6.gif"  style="width: 43px; height: 98px; border-width: 0px;"></a></td>
				    <td><a href="/vol/55"><img alt=" " src="images/slice_0_7.gif"  style="width: 44px; height: 98px; border-width: 0px;"></a></td>
				    <td><a href="/vol/60"><img alt=" " src="images/slice_0_8.gif"  style="width: 40px; height: 98px; border-width: 0px;"></a></td>
				    <td><a href="/vol/65"><img alt=" " src="images/slice_0_9.gif"  style="width: 42px; height: 98px; border-width: 0px;"></a></td>
				    <td><a href="/vol/70"><img alt=" " src="images/slice_0_10.gif"  style="width: 43px; height: 98px; border-width: 0px;"></a></td>
				    <td><a href="/vol/75"><img alt=" " src="images/slice_0_11.gif"  style="width: 41px; height: 98px; border-width: 0px;"></a></td>
				    <td><a href="/vol/80"><img alt=" " src="images/slice_0_12.gif"  style="width: 42px; height: 98px; border-width: 0px;"></a></td>
				    <td><a href="/vol/85"><img alt=" " src="images/slice_0_13.gif"  style="width: 42px; height: 98px; border-width: 0px;"></a></td>
				    <td><a href="/vol/90"><img alt=" " src="images/slice_0_14.gif" style="width: 34px;  height: 98px; border-width: 0px;"></a></td>
				</tr>

				</table>
				<br>
				<form action="/playURI" method="post">
				    URI: <input name="URI" type="text" />
				    <input value="Submit" type="submit" />
				</form>
				<br>
				<a href= "/addfav">Add Favorite</a><br>
				<table width = "600"> <tr><td>
				<ul>
				%for fav in fav_count:		
					<li><a href="/fav/{{fav}}">{{titles[fav-1]}}</a> - <a href="/setfav/{{fav}}">Set</a></li>
				%end
				</ul>
				</td></tr></table>
				<br><a href="/zones">Change Music Zone</a>
				<br><a href="/info">Show Info</a>
			</body>	
	''', fav_count = fav_count, titles = titles)
	

#debug(True)
run(host='0.0.0.0', port = 8080)#, reloader = True)
