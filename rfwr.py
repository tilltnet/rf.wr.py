# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from bottle import route, run, template, debug, get, post, request, redirect
import raumfeld
from bottle import static_file
import os
import collections
import urllib
import urllib2
import re
from urlparse import urlparse
from random import randint

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Define your default music zone here. The zones are alpahbetically sorted by
# names (0 = A-Zone, 1 = B-Zone)
l_zone = 0

if os.path.isfile('active_zone_udn')==False:
    with open('active_zone_udn', 'w') as f:
            f.write('udn')

with open('active_zone_udn', 'a+') as f:
        active_zone_udn = f.readlines()[0]

# Error message (No music zones)
err_msg = 'No music zones found. There might be a network connection problem or you need to create <a href="/zones">zones</a>.'

def discover_active_zone():
        global l_zone
        zones = raumfeld.discover()
        if len(zones) < 1:
                return 999, 999
        if l_zone > len(zones) - 1:
                l_zone = len(zones)-1
        _, _, path, _, _, _ = urlparse(zones[l_zone].location)
        _, active_zone_udn_test = path.replace('.xml', '').rsplit('/',1)

        if active_zone_udn != active_zone_udn_test:
            found = False
            for i in range(0, len(zones)):
                _, _, path, _, _, _ = urlparse(zones[i].location)
                _, zone_udn = path.replace('.xml', '').rsplit('/',1)
                if zone_udn == active_zone_udn:
                    l_zone = i
                    found = True
            if found == False:
                l_zone = 0

        active_zone = zones[l_zone]
        _, _, path, _, _, _ = urlparse(active_zone.location)
        _, zone_udn = path.replace('.xml', '').rsplit('/',1)

        if active_zone_udn != active_zone_udn_test:
            with open('active_zone_udn', 'w') as f:
                    f.write(zone_udn)
        return active_zone, zones

@route('/images/<filename:re:.*\.*>')
def send_image(filename):
        return static_file(filename, root='images/')

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

@route('/')
def index():
        redirect('/player')


### Music Zone Management

def get_zones(devices):
        global l_zone

        # Extract Raumfeld host IP-Address out of the device location and
        hostip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', urlparse(devices[l_zone].location).netloc)

        # Invoke /getZones on the Raumfeld host and read xml response as tree.
        # the structure of tree is <zones><zone><room><///><unassigned><room><//>
        # When all rooms are unassigned <zones> and sublevels are dropped.
        file = urllib2.urlopen('http://' + hostip[0] + ':47365/getZones')
        data = file.read()
        file.close()
        tree = ET.fromstring(data)

        return tree, hostip

def zone_management(devices):
        # zones contains all Raumfeld music zones as RaumfeldDevices(). Can be
        # used to extract zone names and change the target zone.
        if devices[0].model_description == 'Virtual Media Player':
            zone_room_names = [{zone.friendly_name:zone.friendly_name.split(', ')} for zone in devices]
        else:
            zone_room_names = []

        # Extract zones (including all sublevels) of tree and sort it alpahbetically by zone name.
        tree, _ = get_zones(devices)
        #rf_zones = sorted(tree[0].findall('zone'), key = lambda device: device[0].attrib['name'])
        # Extract zones (including all sublevels) of tree and sort it alpahbetically by zone name.
        # rf_zones = tree[0].findall('zone')
        # i = 0
        # for zone in tree[0].findall('zone'):
        #     zone = sorted(zone, key = lambda room: room.attrib['name'])
        #     rf_zones[i] = ET.Element(zone)
        #     print(i)
        #     i = i + 1
        # rf_zones = sorted(rf_zones, key = lambda zones: zones.findtext('name'))
        #zones = [{zone.friendly_name:zone.friendly_name.split(',')} for zone in devices]
        return zone_room_names, tree

def room_management(devices):
        tree, hostip = get_zones(devices)
        add_room_base = 'http://' + hostip[0] + ':47365/connectRoomToZone?zoneUDN='
        drop_room_base = 'http://' + hostip[0] + ':47365/dropRoomJob?roomUDN='

        # Generate partially random UDN for a room to be created.
        zone_udn = 'aaaaaaaa-bbbb-cccc-eeee-' + str(randint(100000000000,9999999999999))

        # Collect all rooms (in zones and unassigned).
        # Checks if there are valid music zones present, if not it is assumed that all rooms are unassigned (see else).
        if devices[0].model_description == 'Virtual Media Player':
                ass_rooms = [tree[0][i].findall('room') for i in range(0,len(tree[0]))]
                if len(tree) > 1:
                        unass_rooms = tree[1].findall('room')
                        ass_rooms.append(unass_rooms)
                rooms = [room for sublist in ass_rooms for room in sublist]

        else:
                rooms = tree[0].findall('room') # This extracts all rooms if all rooms are unassigned.

        return rooms, add_room_base, drop_room_base, zone_udn

@route('/zone/<no>')
def zone(no):
        global l_zone
        global active_zone_udn
        l_zone = int(no)
        zones = raumfeld.discover()
        if len(zones) < 1:
            print 'No devices found.'
        _, _, path, _, _, _ = urlparse(zones[int(no)].location)
        _, zone_udn = path.replace('.xml', '').rsplit('/',1)
        with open('active_zone_udn', 'w') as f:
                f.write(zone_udn)
        active_zone_udn = zone_udn
        redirect('/zones')

def zone_select_by_name(name):
        global l_zone
        global active_zone_udn
        zones = raumfeld.discover()
        if len(zones) < 1:
            print 'No devices found.'
        found = False
        for i in range(0, len(zones)):
            if zones[i].friendly_name == name:
                l_zone = i
                found = True
        if found == False:
            l_zone = 0
        _, _, path, _, _, _ = urlparse(zones[l_zone].location)
        _, zone_udn = path.replace('.xml', '').rsplit('/',1)
        with open('active_zone_udn', 'w') as f:
                f.write(zone_udn)
        active_zone_udn = zone_udn
        return found

@route('/zone_name/<name>')
def zone_name(name):
        found = zone_select_by_name(name)
        if found == False:
            return template('Zone "{{name}}" not found. Setting active zone to zero. <a href="/zones">Continue</a>.', name = name)
        redirect('/zones')

@route('/drop_room/<name>')
def drop_room(name):
        _, zones = discover_active_zone()
        if zones == 999:
            return err_msg
        rooms, _, drop_room_base, _ = room_management(zones)
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
        _, zones = discover_active_zone()
        if zones == 999:
            return err_msg
        rooms, add_room_base, _, zone_udn = room_management(zones)
        if zones[0].model_description == 'Virtual Media Player':
                _, _, path, _, _, _ = urlparse(zones[l_zone].location)
                _, zone_udn = path.replace('.xml', '').rsplit('/',1)

        for room in rooms:
            if room.attrib['name'] == str(name):
                udn_to_add = room.attrib['udn']
        urllib2.urlopen(add_room_base + 'uuid:' + zone_udn + '&roomUDN=' + udn_to_add).read()

        return template('''
            Room added.
            <script language="javascript">
                    setTimeout("location.href = '/zones';",1500);
            </script>
        ''')

@route('/new_zone/<name>')
def new_zone(name):
        _, zones = discover_active_zone()
        if zones == 999:
            return err_msg
        rooms, add_room_base, _, zone_udn = room_management(zones)
        for room in rooms:
            if room.attrib['name'] == str(name):
                udn_to_add = room.attrib['udn']
        urllib2.urlopen(add_room_base + 'uuid:' + zone_udn + '&roomUDN=' + udn_to_add).read()

        return template('''
            New zone created.
            <script language="javascript">
                    setTimeout("location.href = '/zones';",2000);
            </script>
        ''')

@route('/zones')
def zones():
        global l_zone
        _, zones = discover_active_zone()
        if zones == 999:
            return err_msg
        zone_room_names, tree = zone_management(zones)

        zone_nos = range(0, len(zones))
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
 		a.room_plus_Active{
                           pointer-events: none;
                           cursor: default;
                           color: #bdffea;
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
                %i = 0
                %for zone in zone_room_names:
                        <div class = "zone_{{active_zone[i]}}">
                        Zone {{i}}: {{zone_room_names[i].keys()[0]}} <div align="right" class="activation"><a class="{{active_zone[i]}}" href="/zone/{{i}}">{{active_zone[i]}}</a></div>
                        %for room in zone[zone.keys()[0]]:
                            <div class = "room">
                                <a href="/drop_room/{{room}}">- {{room}}</a><a class="room_plus_{{active_zone[i]}}"  href="/add_room/{{room}}">[+]</a>

                                </div>
                        %end
                        </div>
                        %i = i + 1
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
        <li>Remove rooms from any zone by clicking on them or add [+] them to the active zone.</li>
        <li>Unassigned rooms can be added [+] to the active zone or used to create a new room, by clicking on the name.</li>
        </ul>
        <br><a href="/player">Back to Player</a>
        </div>
        </html>
        ''', zone_room_names=zone_room_names, l_zone=l_zone, tree=tree, active_zone=active_zone)


### Basic playback control

@route('/play')
def play():
        active_zone, _ = discover_active_zone()
        if active_zone == 999:
                return err_msg
        active_zone.play()
        redirect('/player')

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

        _, netloc, path, _, _, _ = urlparse(URI)

        if netloc.startswith('www.'):
            netloc = re.sub('www.', '', netloc)

        artist = netloc[0:20]

        ext = [".mp4", ".mp3", ".ogg", ".wmv", ".wav", ".m4a" ]

        if path.endswith(tuple(ext)):
            path = re.sub('.([^.]+)$', '', path)

        tmp = path.split('/')
        path = tmp[len(tmp)-1]
        album = path[0:20]

        title = ' '.join([album, artist])

        host = request.get_header('host')
        coverURI = 'http://' + host + '/images/audio_www.png'
        URIMeta = ''.join(['<DIDL-Lite xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dlna="urn:schemas-dlna-org:metadata-1-0/" xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" xmlns:raumfeld="urn:schemas-raumfeld-com:meta-data/raumfeld"><container id="0/" parentID="0/" restricted="1" childCount="1"><raumfeld:totalPlaytime>1:02:20</raumfeld:totalPlaytime><upnp:albumArtURI>',coverURI,'</upnp:albumArtURI><raumfeld:name>Album</raumfeld:name><upnp:artist>',artist,'</upnp:artist><upnp:album>',album,'</upnp:album><upnp:class>object.container.album.musicAlbum</upnp:class><dc:date>3000</dc:date><dc:title>',title,'</dc:title><raumfeld:section>My Music</raumfeld:section></container></DIDL-Lite>'])

        active_zone, _ = discover_active_zone()
        if active_zone == 999:
                return err_msg

        active_zone.playURI(URI, URIMeta)
        redirect('/player')

@route('/pause')
def pause():
        active_zone, _ = discover_active_zone()
        if active_zone == 999:
                return err_msg
        active_zone.pause()
        redirect('/player')

@route('/next')
def next():
        active_zone, _ = discover_active_zone()
        if active_zone == 999:
                return err_msg
        active_zone.next()
        redirect('/player')


@route('/previous')
def previous():
        active_zone, _ = discover_active_zone()
        if active_zone == 999:
                return err_msg
        active_zone.previous()
        redirect('/player')

@route('/play_pause')
def play_pause():
        active_zone, _ = discover_active_zone()
        if active_zone == 999:
                return err_msg
        TState = active_zone.curTransState
        if str(TState) == "STOPPED" or str(TState) == "PAUSED_PLAYBACK":
                active_zone.mute = False
                active_zone.play()
        else:
                active_zone.pause()
        redirect('/player')


@route('/comehome')
def comehome():
        URI = "http://dradio_mp3_dwissen_m.akacast.akamaistream.net/7/728/142684/v1/gnl.akacast.akamaistream.net/dradio_mp3_dwissen_m"
        active_zone, _ = discover_active_zone()
        if active_zone == 999:
                return err_msg
        TState = active_zone.curTransState
        if str(TState) == "STOPPED" or str(TState) == "PAUSED_PLAYBACK":
                active_zone.mute = False
                active_zone.volume = 50
                active_zone.playURI(URI)
                return 'Welcome Home!'

@route('/play/drwissen') # deprecated, use /fav/<no> instead.
def drwissen():
        URI = "http://dradio_mp3_dwissen_m.akacast.akamaistream.net/7/728/142684/v1/gnl.akacast.akamaistream.net/dradio_mp3_dwissen_m"
        devices = raumfeld.discover()
        if len(devices) > 0:
                speaker = devices[l_zone]
                speaker.playURI(URI)
        redirect('/player')

### Volume Control

@route('/mute')
def mute():
        active_zone, _ = discover_active_zone()
        if active_zone == 999:
                return err_msg
        active_zone.mute = True
        redirect('/player')

@route('/vol/<no>')
def vol(no):
        active_zone, _ = discover_active_zone()
        if active_zone == 999:
                return err_msg
        active_zone.mute = False
        active_zone.volume = int(no)

        redirect('/player')


### Podcast support

def pod_read():
        with open('podcasts', 'a+') as f:
                podcasts = f.readlines()
        podcasts = [each.replace('\n', '') for each in podcasts]
        podcasts = [each.split(';') for each in podcasts]

        return podcasts

def pod_parse_feed(feed_url):
        file = urllib2.urlopen(feed_url)
        data = file.read()
        file.close()
        tree = ET.fromstring(data)
        title = tree[0].find('title').text
        try:
            img = tree[0].find('image').find('url').text
            img_file = urllib.URLopener()
            img_file.retrieve(img, "images/" + title + ".png")
            img = 'http://' + host + '/images/' + title + '.png'
            img_path = '/images/' + title + '.png'
        except:
            host = request.get_header('host')
            try:
                ns = {'itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd'}
                img = tree[0].find('itunes:image', ns).attrib['href']
                img_file = urllib.URLopener()
                img_file.retrieve(img, "images/" + title + ".png")
                img = 'http://' + host + '/images/' + title + '.png'
                img_path = '/images/' + title + '.png'
            except:
                img = 'http://' + host + '/images/podcast2_www.png'
                img_path = '/images/podcast2_www.png'
        return tree, title, img, img_path

@post('/playPodcast')
def playPodcastPost():
        feed_url = request.forms.get('feed_url')
        tree, title, img, _ = pod_parse_feed(feed_url)
        URI = tree[0].find('item').find('enclosure').attrib['url']
        #URIMeta = ''.join(['<DIDL-Lite xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dlna="urn:schemas-dlna-org:metadata-1-0/" xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" xmlns:raumfeld="urn:schemas-raumfeld-com:meta-data/raumfeld"><container><dc:title>',title,'</dc:title></container></DIDL-Lite>']).encode('utf8')

        active_zone, _ = discover_active_zone()
        if active_zone == 999:
                return err_msg
        active_zone.playURI(URI)

        redirect('/player')

@post('/addPodcast')
def addPodcast():
        feed_url = request.forms.get('feed_url')
        _, title, img, img_path = pod_parse_feed(feed_url)

        with open('podcasts', 'a+') as f:
                content = f.readlines()

        content = [each.replace('\n', '') for each in content]
        entry = ';'.join([title, feed_url, img, img_path])
        content.append(entry)

        with open('podcasts','w') as f:
                for item in content:
                        f.write('%s\n' % item.encode('utf8'))
        redirect('/player')


### Favorites

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
        namespaces = {'dc': 'http://purl.org/dc/elements/1.1/', 'upnp':'urn:schemas-upnp-org:metadata-1-0/upnp/'}
        titles = [tree[0].find('dc:title', namespaces).text for tree in trees]
        cover_imgs = [tree[0].find('upnp:albumArtURI', namespaces).text for tree in trees]

        return no, URIs, Meta, titles, cover_imgs

@route('/fav/<no>')
def fav(no):
        no, URIs, Meta, _, _ = read_favs(no)
        if len(URIs) == 0:
                return 'No Favorites have been set yet. Use /addfav to add a favorite.'
        elif len(URIs) <= no:
                return 'This favorite has not been set yet. Use /addfav to add a favorite.'
        favURI = URIs[no]
        favMeta = Meta[no]
        active_zone, _ = discover_active_zone()
        if active_zone == 999:
                return err_msg
        active_zone.playURI(favURI, favMeta)
        redirect('/player')


@route('/setfav/<no>')
def setfav(no):
        no, URIs, Meta, _, _ = read_favs(no)
    	if len(URIs) == 0:
    		return 'No Favorites have been set yet. Use /addfav to add a favorite.'
    	elif len(URIs) <= no:
    		return 'This favorite has not been set yet. Use /addfav to add a favorite.'

        active_zone, _ = discover_active_zone()
        if active_zone == 999:
                return err_msg
    	URIs[no] = active_zone.currentURI()
    	Meta[no] = active_zone.currentURIMetaData()

    	out_list = []
    	for i in range(0,len(URIs)):
    		      out_list.append(URIs[i])
    		      out_list.append(Meta[i])
    	with open('favorites','w') as f:
    		      for item in out_list:
      			             f.write("%s\n" % item)
        redirect('/player')


@route('/addfav')
def addfav():
        _, URIs, Meta, _, _ = read_favs()
        active_zone, _ = discover_active_zone()
        if active_zone == 999:
                return err_msg
        URIs.append(active_zone.currentURI())
        Meta.append(active_zone.currentURIMetaData())
        out_list = []
        for i in range(0,len(URIs)):
                out_list.append(URIs[i])
                out_list.append(Meta[i])
        with open('favorites','w') as f:
                for item in out_list:
                        f.write("%s\n" % item)
        redirect('/player')


### Info

@route('/info')
def info():
        devices = raumfeld.discover()
        if len(devices) > 0:
                speaker = devices[l_zone]
                curURI = speaker.currentURI()
                curMeta = speaker.currentURIMetaData()
                trackURI = speaker.trackURI()
                trackMeta = speaker.trackMetaData()

                namespaces = {'dc':'http://purl.org/dc/elements/1.1/','upnp':'urn:schemas-upnp-org:metadata-1-0/upnp/','raumfeld':'urn:schemas-raumfeld-com:meta-data/raumfeld/'}

                curMeta_tree = ET.fromstring(str(curMeta))
                trackMeta_tree = ET.fromstring(str(trackMeta))
                try:
                    curURI_title = curMeta_tree[0].find('dc:title', namespaces).text
                except :
                    curURU_titlt = '-'
                try:
                    track_title = trackMeta_tree[0].find('dc:title', namespaces).text
                except :
                    track_title = '-'
                try:
                    track_album = trackMeta_tree[0].find('upnp:album', namespaces).text

                except:
                        track_album = '-'
                try:
                    track_artist = trackMeta_tree[0].find('upnp:artist', namespaces).text
                except:
                        track_artist = '-'
                try:
                    track_img = trackMeta_tree[0].find('upnp:albumArtURI', namespaces).text
                except :
                        track_img = '-'
                try:
                    curURI_img = curMeta_tree[0].find('upnp:albumArtURI', namespaces).text
                except :
                    curURI_img = '-'
        else:
                return 'No devices found.'

        print(type(curURI))
        return template('''
                <html>
                        <body>
                                <h1>Track and Playlist Info</h1>
                                <img src="{{track_img}}"><br>
                                <img src="{{curURI_img}}"><br>
                                Track: {{track_title}} <br>
                                Artist: {{track_artist}} <br>
                                Album: {{track_album}} <br>
                                Playlist: {{curURI_title}}<br><br>

                                CurrentURI:<br> {{curURI}} <br> <br>
                                CurrentMetaData:<br> {{curMeta}}<br> <br>

                                TrackURI:<br> {{trackURI}} <br> <br>
                                TrackMetaData:<br> {{trackMeta}}<br> <br>

                                Devices / Music Zones:<br> {{devices}}
                                <br><br><a href="/player">Back to Player</a>
                                <br><br>

                        </body>

                </html>
        ''', curURI_img=curURI_img, track_img=track_img, track_artist=track_artist, track_album = track_album, curURI_title=curURI_title, track_title=track_title, curURI=curURI, curMeta=curMeta, trackURI=trackURI, trackMeta=trackMeta, devices=devices)

### Player UI (for HTML see player.tbl)

@route('/player')
def player():
        _, URIs, Meta, titles, cover_imgs = read_favs()
        fav_count = range(1,len(URIs) + 1)
        podcasts = pod_read()
        return template('shinynew_player', fav_count = fav_count, titles = titles, podcasts = podcasts, cover_imgs = cover_imgs)

@route('/shinynew')
def player():
        _, URIs, Meta, titles, cover_imgs = read_favs()
        fav_count = range(1,len(URIs) + 1)
        podcasts = pod_read()
        return template('shinynew_player', fav_count = fav_count, titles = titles, podcasts = podcasts, cover_imgs = cover_imgs)

debug(True)
run(host='0.0.0.0', port = 8080, reloader = True)
