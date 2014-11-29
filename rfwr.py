from bottle import route, run, template
from bottle import get, post, request
import raumfeld
from bottle import static_file
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

@route('/images/<filename:re:.*\.png>')
def send_image(filename):
    return static_file(filename, root='images/', mimetype='image/png')


@route('/')
def index():
	return '''
	<script language="javascript">
    		window.location.href = "/player"
	</script>
	'''

@route('/pause')
def pause():
	devices = raumfeld.discover()
	if len(devices) > 0:
		speaker = devices[0]
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
		speaker = devices[0]
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
		speaker = devices[0]
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
		speaker = devices[0]
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
		speaker = devices[0]
		speaker.play()
	else:
		return 'No devices found.'
	return '''
	<script language="javascript">
    		window.location.href = "/player"
	</script>
	'''

@route('/playURI')
def play():
	return '''
		<form action="/playURI" method="post">
		    URI: <input name="URI" type="text" />
		    <input value="Submit" type="submit" />
		</form>
	'''

@post('/playURI')
def do_play():
	URI = request.forms.get('URI')
	devices = raumfeld.discover()
	if len(devices) > 0:
		speaker = devices[0]
		speaker.playURI(URI)
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
		speaker = devices[0]
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
		speaker = devices[0]
		speaker.playURI(URI)
	else:
		return 'No devices found.'
	return '''
	<script language="javascript">
    		window.location.href = "/player"
	</script>
	'''

@route('/player')
def player():
	return '''
		<html>
			<head>
			<title>rf.wr.py</title>
				<style type="text/css"><!--A{text-decoration:none}--></style>
			</head>
			<body>		
				<h1>
				<a href="/previous"><img alt="prev" src="/images/prev.png"></a><a href="/play"><img alt="play" src="/images/play.png"></a><a href="/pause"><img alt="pause" src="/images/pause.png"></a><a href="/next"><img alt="next" src="/images/next.png"></a>   
				</h1>
				<br>
				<form action="/playURI" method="post">
				    URI: <input name="URI" type="text" />
				    <input value="Submit" type="submit" />
				</form>
				<br><a href="/play/drwissen">Dradio Wissen</a>
				<br><a href="/play/recentArtists">Zuletzt gehoerte Kuenstler</a>
			</body>
	'''

run(host='0.0.0.0', port = 8080)
