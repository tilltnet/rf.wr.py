from bottle import route, run, template
from bottle import get, post, request
import raumfeld

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

@route('/play')
def play():
	devices = raumfeld.discover()
	if len(devices) > 0:
		speaker = devices[0]
		speaker.mute = False
		speaker.volume = 60
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
	URI = "dlna-playsingle://uuid%3A4f0d7a8e-680e-493a-9907-6e6cb772f0b4?sid=urn%3Aupnp-org%3AserviceId%3AContentDirectory&iid=0%2FFavorites%2FMyFavorites%2F30"
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
		<title>rf.player</title>
		<style type="text/css"><!--A{text-decoration:none}--></style>
		</head>
		<h1>
		<a href="/previous">&#x2770;&#x2770;</a>
		<a href="/play">    &#x27a4;</a>  
		<a href="/pause">&#x275a;&#x275a;</a>
		<a href="/next">	&#x2771;&#x2771;</a>   </h1> 
		<br> 
		<form action="/playURI" method="post">
		    URI: <input name="URI" type="text" />
		    <input value="Submit" type="submit" />
		</form>
		<br><a href="/play/drwissen">Dradio Wissen</a>
		<br><a href="/play/recentArtists">Zuletzt gehoerte Kuenstler</a>
	'''

run(host='0.0.0.0', port = 8080)
