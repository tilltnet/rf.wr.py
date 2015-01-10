import xml.etree.ElementTree as ET
from bottle import route, run, template, debug
from bottle import get, post, request
import raumfeld
from bottle import static_file
import os
import collections
import urllib2
import re
from urlparse import urlparse
from random import randint

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
        devices = raumfeld.discover(5)
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
                window.location.href = "/zones"

        </script>

        '''


@route('/drop_room/<name>')
def drop_room(name):
        global l_zone
        devices = raumfeld.discover()
        if len(devices) < 1:
                return 'No devices found.'
        hostip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', urlparse(devices[l_zone].location).netloc)

        zones = [device.friendly_name for device in devices]
        print(zones)
        file = urllib2.urlopen('http://' + hostip[0] + ':47365/getZones')
        data = file.read()
        file.close()
        tree = ET.fromstring(data)

        rf_zones = sorted(tree[0].findall('zone'), key = lambda device: device[0].attrib['name'])

        drop_room_base = 'http://' + hostip[0] + ':47365/dropRoomJob?roomUDN='
        rooms = rf_zones[l_zone].findall('room')
        for room in rooms:
            if room.attrib['name'] == str(name):
                udn_to_drop = room.attrib['udn']
        urllib2.urlopen(drop_room_base + udn_to_drop).read()
        return '''
        Room dropped.
        <script language="javascript">
                setTimeout("location.href = '/zones';",1500);
        </script>
        '''

@route('/add_room/<name>')
def add_room(name):
        global l_zone
        devices = raumfeld.discover()
        if len(devices) < 1:
                return 'No devices found.'
        hostip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', urlparse(devices[l_zone].location).netloc)

        file = urllib2.urlopen('http://' + hostip[0] + ':47365/getZones')
        data = file.read()
        file.close()
        tree = ET.fromstring(data)

        if devices[0].model_description == 'Virtual Media Player':
                zones = [device.friendly_name for device in devices]
                _, _, path, _, _, _ = urlparse(devices[l_zone].location)
                _, zone_udn = path.replace('.xml', '').rsplit('/',1)
                rooms = tree[1].findall('room')

        else:
                zone_udn = 'aaaaaaaa-bbbb-cccc-eeee-ffffffffffff'
                rooms = tree[0].findall('room')


        add_room_base = 'http://' + hostip[0] + ':47365/connectRoomToZone?'
        for room in rooms:
            if room.attrib['name'] == str(name):
                udn_to_add = room.attrib['udn']
        urllib2.urlopen(add_room_base + 'zoneUDN=uuid:' + zone_udn + '&roomUDN=' + udn_to_add).read()
        return template('''
        Room added.
        <script language="javascript">
                setTimeout("location.href = '/zones';",1500);
        </script>
        ''')

@route('/new_zone/<name>')
def new_zone(name):
        global l_zone
        devices = raumfeld.discover()
        if len(devices) < 1:
                return 'No devices found.'
        hostip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', urlparse(devices[l_zone].location).netloc)

        file = urllib2.urlopen('http://' + hostip[0] + ':47365/getZones')
        data = file.read()
        file.close()
        tree = ET.fromstring(data)


        if devices[0].model_description == 'Virtual Media Player':
                zones = [device.friendly_name for device in devices]
                zone_udn = 'aaaaaaaa-bbbb-cccc-eeee-' + str(randint(100000000000,9999999999999))
                ass_rooms = [tree[0][i].findall('room') for i in range(0,len(tree[0]))]
                if len(tree) > 1:
                        unass_rooms = tree[1].findall('room')
                        ass_rooms.append(unass_rooms)
                rooms = [room for sublist in ass_rooms for room in sublist]

        else:
                zone_udn = 'aaaaaaaa-bbbb-cccc-eeee-ffffffffffff'
                rooms = tree[0].findall('room')


        add_room_base = 'http://' + hostip[0] + ':47365/connectRoomToZone?'
        for room in rooms:
            if room.attrib['name'] == str(name):
                udn_to_add = room.attrib['udn']
        urllib2.urlopen(add_room_base + 'zoneUDN=uuid:' + zone_udn + '&roomUDN=' + udn_to_add).read()
        return template('''
        New zone created.
        <script language="javascript">
                setTimeout("location.href = '/zones';",2000);
        </script>
        ''')

@route('/zones')
def zones():
        global l_zone
        devices = raumfeld.discover()
        if len(devices) < 1:
                return 'No devices found.'
        zones = [device.friendly_name for device in devices]

        if l_zone > len(devices) - 1:
                l_zone = 0

        hostip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', urlparse(devices[l_zone].location).netloc)

        file = urllib2.urlopen('http://' + hostip[0] + ':47365/getZones')
        data = file.read()
        file.close()
        tree = ET.fromstring(data)
        rf_zones = sorted(tree[0].findall('zone'), key = lambda device: device[0].attrib['name'])
        zone_nos = range(0, len(devices))
        active_zone = [no == l_zone for no in zone_nos]
        active_zone = [re.sub('True', 'Active', str(no)) for no in active_zone]
        active_zone = [re.sub('False', 'Activate', str(no)) for no in active_zone]

        return template('''
        <html>
        <head>
                <title>rf.wr.py</title>
 		<style type="text/css">
 		<!--A{text-decoration:none}-->
                div.activation{
                        align: right;
                }
 		a.Active{
                           pointer-events: none;
                           cursor: default;
                           color: #D4C311;
 		}
 		a.room_Activate{
                           pointer-events: none;
                           cursor: default;
                           color: black;
 		}
 		div{
 			margin: 0px auto; width: 250px;
                        }
 		div.zone_Activate{
                        background-color:#bdbbea;
                        padding: 15px 15px 15px 15px;
                        }

                div.zone_Active{
                        background-color:#bdffea;
                        padding: 15px 15px 15px 15px;
                        border: 1px solid;
                        }
                div.unassigned{
                        background-color:#66FA7F;
                        padding: 15px 15px 15px 15px;
                        }
 		</style>
 	</head>
        <div><h1>Zone Manager <a href="/zones" title="Refresh">&#10226;</a> </h1>
        %if tree[0].tag == 'zones':
                %for i in range(0, len(tree[0])):
                        <div class = "zone_{{active_zone[i]}}">
                        Zone {{i}}: {{zones[i]}} <div align="right" class="activation"><a class="{{active_zone[i]}}" href="/zone/{{i}}">{{active_zone[i]}}</a></div>
                        %for j in range(0, len(tree[0][i])):
                            <div class = "room">
                                <a class="room_{{active_zone[i]}}" href="/drop_room/{{rf_zones[i][j].attrib['name']}}">- {{rf_zones[i][j].attrib['name']}}</a>

                                </div>
                        %end
                        </div>
                %end
                       Active Zone: {{l_zone}}<br>
                %if len(tree) > 1:
                    <div class = "unassigned"> Unassigned:
                    %for i in range(0, len(tree[1])):
                        <div class = "room"><a href="/new_zone/{{tree[1][i].attrib['name']}}">{{tree[1][i].attrib['name']}}</a><a href="/add_room/{{tree[1][i].attrib['name']}}">[+]</a></div>
                    %end
                    </div>
                %end
        %else:
                    <div class = "unassigned"> Unassigned:
                    %for i in range(0, len(tree[0])):
                        <div class = "room"><a href="/new_zone/{{tree[0][i].attrib['name']}}">{{tree[0][i].attrib['name']}}</a><a href="/add_room/{{tree[0][i].attrib['name']}}">[+]</a></div>
                    %end
                    </div>
        %end
        <br><br>
        Usage:
        <ul>
        <li>Choose active zone by clicking on 'Activate'.</li>
        <li>Remove Rooms from active zone by clicking on them.</li>
        <li>Unassigned rooms can be added [+] to the active zone or used to create a new room, by clicking on the name.</li>
        </ul>
        <br><a href="/player">Back to Player</a>
        </div>
        </html>
        ''', zones=zones, l_zone=l_zone, tree=tree, rf_zones = rf_zones, active_zone=active_zone)

@route('/pause')
def pause():
        devices = raumfeld.discover(5)
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
        devices = raumfeld.discover(5)
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
        devices = raumfeld.discover(5)
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
        devices = raumfeld.discover(5)
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
        devices = raumfeld.discover(5)
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
        devices = raumfeld.discover(5)
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

@route('/playPodcast')
def playPodcast():
        with open('podcasts', 'a+') as f:
                podcasts = f.readlines()
        podcasts = [each.replace('\n', '') for each in podcasts]
        podcasts = [each.split(';') for each in podcasts]
        return template('''
                <html>
                <head>
                <script language=javascript>

                %for i in range(0,len(podcasts)):
                function submitPostLink_{{i}}()
                        {
                                document.postlink_{{i}}.submit();
                        }
                %end

                </script>
                </head>
                <body>
                Play latest entry of an RSS Podcast Feed
                        <form action="/playPodcast" method="post">
                                Play: <input name="feed_url" type="text" placeholder = "RSS feed address"/>
                                <input value="Submit" type="submit" />
                        </form>
                        <form action="/addPodcast" method="post">
                                Add: <input name="feed_url" type="text" placeholder = "RSS feed address"/>
                                <input value="Submit" type="submit" />
                        </form>

                %for i in range(0,len(podcasts)):
                        <form action="/playPodcast" name="postlink_{{i}}" method="post"><input type="hidden" name="feed_url" value="{{podcasts[i][1]}}"></form>
                        <a href=# onclick="submitPostLink_{{i}}(); return false;">{{podcasts[i][0]}}</a>
                %end

                </body>
                </html>
        ''', podcasts = podcasts)

@post('/playPodcast')
def playPodcastPost():
        feed_url = request.forms.get('feed_url')
        file = urllib2.urlopen(feed_url)
        data = file.read()
        file.close()
        tree = ET.fromstring(data)
        URI = tree[0].find('item').find('enclosure').attrib['url']
        title = tree[0].find('title').text
        URIMeta = ''.join(['<DIDL-Lite xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dlna="urn:schemas-dlna-org:metadata-1-0/" xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" xmlns:raumfeld="urn:schemas-raumfeld-com:meta-data/raumfeld"><container><dc:title>',title,'</dc:title></container></DIDL-Lite>'])
        devices = raumfeld.discover(5)
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

@post('/addPodcast')
def addPodcast():
        feed_url = request.forms.get('feed_url')
        file = urllib2.urlopen(feed_url)
        data = file.read()
        file.close()
        tree = ET.fromstring(data)
        title = tree[0].find('title').text
        with open('podcasts', 'a+') as f:
                content = f.readlines()

        content = [each.replace('\n', '') for each in content]
        entry = ';'.join([title, feed_url])
        content.append(entry)
        #return template('{{content}}<br>{{type(content)}}', content=content)

        with open('podcasts','w') as f:
                for item in content:
                        f.write("%s\n" % item)
        return '''
        <script language="javascript">
                        window.location.href = "/player"
        </script>
        '''

@route('/play/drwissen')
def drwissen():
        URI = "http://dradio_mp3_dwissen_m.akacast.akamaistream.net/7/728/142684/v1/gnl.akacast.akamaistream.net/dradio_mp3_dwissen_m"
        devices = raumfeld.discover(5)
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
        devices = raumfeld.discover(5)
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
        devices = raumfeld.discover(5)
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
	Favorite has been set.
	<script language="javascript">
    		window.location.href = "/player"
	</script>
	'''

@route('/addfav')
def addfav():
        favs = read_favs()
        URIs = favs[1]
        Meta = favs[2]
        devices = raumfeld.discover(5)
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
        devices = raumfeld.discover(5)
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
        with open('podcasts', 'a+') as f:
                podcasts = f.readlines()
        podcasts = [each.replace('\n', '') for each in podcasts]
        podcasts = [each.split(';') for each in podcasts]
        return template('player', fav_count = fav_count, titles = titles, podcasts = podcasts)


debug(True)
run(host='0.0.0.0', port = 8080, reloader = True)
