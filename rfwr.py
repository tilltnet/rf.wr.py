# -*- coding: UTF-8 -*-
from gevent import monkey; monkey.patch_all()

import xml.etree.ElementTree as ET
from bottle import route, run, template, get, post, request, redirect
import raumfeld
from bottle import static_file
import os
import collections
import urllib
import urllib2
import re
from urlparse import urlparse
from random import randint
import hashlib
import codecs
import string
from bottle import Bottle, abort, mount, default_app
from gevent import queue, sleep
import threading
import copy

# Change execution path to __file__ location.
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setting up threading stuff and global vars.
updateAvailableEvent = threading.Event()
__active_zoneLock = threading.RLock()

active_zone = ""
zones_on =  False
seek_change = False
TState = ''

# Create active_zone_udn file if it does not exist.
if os.path.isfile('active_zone_udn')==False:
    with open('active_zone_udn', 'w') as f:
            f.write('udn')

# Read active_zone_udn from file.
with open('active_zone_udn', 'a+') as f:
        active_zone_udn = f.readlines()[0]

def __updateAvailableCallback():
    global updateAvailableEvent
    updateAvailableEvent.set()

def __resetUpdateAvailableEventThread():
    global updateAvailableEvent
    while True:
        updateAvailableEvent.wait()
        updateAvailableEvent.clear()

def discover_active_zone():
    __active_zoneLock.acquire()
    global active_zone
    active_zone = raumfeld.getZoneByUDN(active_zone_udn)
    if active_zone == None:
        active_zone = raumfeld.getZones()[0]
    sleep(2)
    __active_zoneLock.release()
    return active_zone

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



@route('/zone/<udn>')
def zone(udn):
        global active_zone_udn
        zone = raumfeld.getZoneByUDN(udn)
        if zone != None:
            active_zone_udn = udn
        else:
            zones = raumfeld.getZones()
            zone = zones[0]
            active_zone_udn = zone.UDN

        with open('active_zone_udn', 'w') as f:
                f.write(active_zone_udn)
        redirect('/ctct')

@route('/zone_name/<name>')
def zone_name(name):
        """Partial, unique string contained in the name or whole name of the zone is used to set the active zone"""
        global active_zone_udn
        zones = raumfeld.getZonesByName(name)
        zone = zones[0]
        active_zone_udn = zone.UDN
        with open('active_zone_udn', 'w') as f:
            f.write(active_zone_udn)
        redirect('/ctct')

@route('/drop_room/<name>')
def drop_room(name):
        """Drops the room of the provided name"""
        rooms = raumfeld.getRoomsByName(name)
        room = rooms[0]
        raumfeld.dropRoomByUDN(room.UDN)
        redirect('/ctct')


@route('/add_room/<name>')
def add_room(name):
        rooms = raumfeld.getRoomsByName(name)
        room = rooms[0]
        zone = discover_active_zone()
        raumfeld.connectRoomToZone(room.UDN, zone.UDN)
        redirect('/ctct')

@route('/new_zone/<name>')
def new_zone(name):
        rooms = raumfeld.getRoomsByName(name)
        room = rooms[0]
        raumfeld.connectRoomToZone(room.UDN)
        redirect('/ctct')

@route('/zones')
def zones_fun():
        """Needs to be reworked or deleted"""
        zones = raumfeld.getZones()
        zone = raumfeld.getZoneByUDN(active_zone_udn)
        active_zone_str_helper = [active_zone_udn == zone.UDN for zone in zones]
        active_zone_str_helper = [re.sub('True', 'Active', str(no)) for no in active_zone_str_helper]
        active_zone_str_helper = [re.sub('False', 'Activate', str(no)) for no in active_zone_str_helper]

        return template('zone_manager', zone_room_names=zone_room_names, tree=tree, active_zone_str_helper=active_zone_str_helper)

@route('/zones_on_off')
def zones_on_off():
    global zones_on
    if zones_on:
        zones_on = False
    else:
        zones_on = True
    redirect('/ctct')

### Basic playback control

@route('/play')
def play():
        __active_zoneLock.acquire()
        active_zone.play()
        __active_zoneLock.release()

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

        __active_zoneLock.acquire()
        active_zone.play(URI, URIMeta)
        __active_zoneLock.release()

        redirect('/player')

@route('/pause')
def pause():
        __active_zoneLock.acquire()
        active_zone.pause()
        __active_zoneLock.release()

        redirect('/player')

@route('/next')
def next():
        __active_zoneLock.acquire()
        active_zone.next()
        __active_zoneLock.release()

        redirect('/ctct')


@route('/previous')
def previous():
        __active_zoneLock.acquire()
        active_zone.previous()
        __active_zoneLock.release()

        redirect('/ctct')

@route('/seek/<secs>')
def play_pause(secs):
        m, s = divmod(int(secs), 60)
        h, m = divmod(m, 60)
        hh_mm_ss = "%02d:%02d:%02d" % (h, m, s)

        __active_zoneLock.acquire()
        active_zone.seek(hh_mm_ss)
        __active_zoneLock.release()

        global seek_change
        seek_change = True

@route('/track/<no>')
def track(no):
        __active_zoneLock.acquire()
        active_zone.seek(no, unit='TRACK_NR')
        __active_zoneLock.release()
        redirect('/player')

@post('/track')
def post_track():
        no = request.forms.get('no')
        __active_zoneLock.acquire()
        active_zone.seek(no, unit='TRACK_NR')
        __active_zoneLock.release()
        redirect('/player')

@route('/play_pause')
def play_pause():
        __active_zoneLock.acquire()
        TState = str(active_zone.transport_state)
        if str(TState) == "STOPPED" or str(TState) == "PAUSED_PLAYBACK":
                active_zone.mute = False
                active_zone.play()
        else:
                active_zone.pause()
                sleep(0.3)
        __active_zoneLock.release()
        redirect('/ctct')


@route('/comehome')
def comehome():
        URI = "http://dradio_mp3_dwissen_m.akacast.akamaistream.net/7/728/142684/v1/gnl.akacast.akamaistream.net/dradio_mp3_dwissen_m"

        __active_zoneLock.acquire()
        TState = str(active_zone.transport_state)


        if str(TState) == "STOPPED" or str(TState) == "PAUSED_PLAYBACK":
                active_zone.mute = False
                active_zone.volume = 50
                active_zone.play(URI)
        __active_zoneLock.release()
        return 'Welcome Home!'

### Volume Control

@route('/mute')
def mute():
        __active_zoneLock.acquire()
        active_zone.mute = True
        __active_zoneLock.release()

        redirect('/ctct')

@route('/vol/<no>')
def vol(no):

        if active_zone == 999:
                return err_msg

        __active_zoneLock.acquire()
        active_zone.mute = False
        active_zone.volume = int(no)
        __active_zoneLock.release()

        redirect('/ctct')


### Podcast support

def pod_read():
        with codecs.open('podcasts', 'a+', 'UTF-8') as f:
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

        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        nothing_special = ''.join(c for c in title if c in valid_chars)
        sane_title = re.sub(' ', '', nothing_special)

        ep_title = tree[0].find('item').find('title').text
        host = request.get_header('host')
        try:
            img = tree[0].find('image').find('url').text
            img_file = urllib.URLopener()
            img_file.retrieve(img, u"images/" + sane_title + u".png")
            img = u'http://' + host + u'/images/' + sane_title + u'.png'
            img_path = u'/images/' + sane_title + u'.png'
        except:
            try:
                ns = {u'itunes':u'http://www.itunes.com/dtds/podcast-1.0.dtd'}
                img = tree[0].find(u'itunes:image', ns).attrib[u'href']
                img_file = urllib.URLopener()
                img_file.retrieve(img, u"images/" + sane_title + u".png")
                img = u'http://' + host + u'/images/' + sane_title + u'.png'
                img_path = u'/images/' + sane_title + u'.png'
            except:
                img = u'http://' + host + u'/images/podcast2_www.png'
                img_path = u'/images/podcast2_www.png'
        return tree, title, img, img_path, ep_title

def play_podcast_fun(feed_url):
    tree, title, img, _, ep_title = pod_parse_feed(feed_url)
    URI = tree[0].find('item').find('enclosure').attrib['url']
    URIMeta = u''.join([u'<DIDL-Lite xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dlna="urn:schemas-dlna-org:metadata-1-0/" xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" xmlns:raumfeld="urn:schemas-raumfeld-com:meta-data/raumfeld"><container id="0/" parentID="0/" restricted="1" childCount="1"><raumfeld:totalPlaytime>1:02:20</raumfeld:totalPlaytime><upnp:albumArtURI dlna:profileID="JPEG_TN">',img,u'</upnp:albumArtURI><raumfeld:name>Album</raumfeld:name><upnp:artist>',title,u'</upnp:artist><upnp:album>','Podcast',u'</upnp:album><upnp:class>object.container.album.musicAlbum</upnp:class><dc:date>3000</dc:date><dc:title>',ep_title,u'</dc:title><raumfeld:section>My Music</raumfeld:section></container></DIDL-Lite>'])

    __active_zoneLock.acquire()
    active_zone.play(URI, URIMeta)
    __active_zoneLock.release()

@route('/playPodcast/<no>')
def play_podcast(no):
    no = int(no) - 1
    podcasts = pod_read()
    feed_url = podcasts[no][1]
    play_podcast_fun(feed_url)


@post('/playPodcast')
def playPodcastPost():
        feed_url = request.forms.get('feed_url')
        play_podcast_fun(feed_url)

@post('/addPodcast')
def addPodcast():
        feed_url = request.forms.get('feed_url')
        _, title, img, img_path, _ = pod_parse_feed(feed_url)

        with codecs.open('podcasts', 'a+', 'UTF-8') as f:
                content = f.readlines()

        content = [each.replace('\n', '') for each in content]
        entry = ';'.join([title, feed_url, img, img_path])
        content.append(entry)

        with codecs.open('podcasts','w', 'UTF-8') as f:
                for item in content:
                        f.write('%s\n' % item)
        redirect('/player')

@route('/delPodcast/<no>')
def addPodcast(no):
        no = int(no) - 1
        with codecs.open('podcasts', 'a+', 'UTF-8') as f:
                content = f.readlines()
        content = [each.replace('\n', '') for each in content]
        del content[no]
        with codecs.open('podcasts','w', 'UTF-8') as f:
                for item in content:
                        f.write('%s\n' % item)
        redirect('/player')

### Favorites

def read_favs(no=1):
        with codecs.open('favorites', 'a+', 'UTF-8') as f:
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
                        Meta[i] = u''.join([u'<DIDL-Lite xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dlna="urn:schemas-dlna-org:metadata-1-0/" xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" xmlns:raumfeld="urn:schemas-raumfeld-com:meta-data/raumfeld"><container><dc:title>',URIs[i],u'</dc:title></container></DIDL-Lite>'])

        no = int(no) - 1

        trees = [ET.fromstring(each.encode('UTF-8')) for each in Meta]
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

        if active_zone == 999:
                return err_msg
        active_zone.play(favURI, favMeta)
        redirect('/player')


@route('/setfav/<no>')
def setfav(no):
        no, URIs, Meta, _, _ = read_favs(no)
        if len(URIs) == 0:
                return 'No Favorites have been set yet. Use /addfav to add a favorite.'
        elif len(URIs) <= no:
                return 'This favorite has not been set yet. Use /addfav to add a favorite.'

        __active_zoneLock.acquire()
        URIs[no] = active_zone.uri
        Meta[no] = active_zone.uri_metadata
        __active_zoneLock.release()

        out_list = []
        for i in range(0,len(URIs)):
            out_list.append(URIs[i])
            out_list.append(Meta[i])
        with codecs.open('favorites','w', encoding='UTF-8') as f:
            for item in out_list:
                f.write("%s\n" % item)
        redirect('/player')


@route('/addfav')
def addfav():
        _, URIs, Meta, _, _ = read_favs()

        if active_zone == 999:
                return err_msg

        __active_zoneLock.acquire()
        URIs.append(active_zone.uri)
        Meta.append(active_zone.uri_metadata)
        __active_zoneLock.release()

        out_list = []
        for i in range(0,len(URIs)):
                out_list.append(URIs[i])
                out_list.append(Meta[i])
        with codecs.open('favorites','w', encoding='UTF-8') as f:
                for item in out_list:
                        f.write("%s\n" % item)
        redirect('/player')

@route('/addfav/track')
def addfav_track():
        _, URIs, Meta, _, _ = read_favs()

        __active_zoneLock.acquire()
        URIs.append(active_zone.track_uri)
        Meta.append(active_zone.track_metadata)
        __active_zoneLock.release()

        out_list = []
        for i in range(0,len(URIs)):
                out_list.append(URIs[i])
                out_list.append(Meta[i])
        with codecs.open('favorites','w', encoding='UTF-8') as f:
                for item in out_list:
                        f.write("%s\n" % item)
        redirect('/player')


### Info

@route('/info')
def info():
        zones = raumfeld.getZones()
        __active_zoneLock.acquire()
        curURI = active_zone.uri
        curMeta = active_zone.uri_metadata
        trackURI = active_zone.track_uri
        trackMeta = active_zone.track_metadata
        __active_zoneLock.release()

        namespaces = {'dc':'http://purl.org/dc/elements/1.1/','upnp':'urn:schemas-upnp-org:metadata-1-0/upnp/','raumfeld':'urn:schemas-raumfeld-com:meta-data/raumfeld/'}



        curMeta_tree = ET.fromstring(unicode(trackMeta).encode('utf8'))
        trackMeta_tree = ET.fromstring(unicode(trackMeta).encode('utf8'))
        try:
            curURI_title = curMeta_tree[0].find('dc:title', namespaces).text
        except :
            curURI_titlt = '-'
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

                                Devices / Music Zones:<br>
                                <br><br><a href="/player">Back to Player</a>
                                <br><br>

                        </body>

                </html>
        ''', curURI_img=curURI_img, track_img=track_img, track_artist=track_artist, track_album = track_album, curURI_title=curURI_title, track_title=track_title, curURI=curURI, curMeta=curMeta, trackURI=trackURI, trackMeta=trackMeta)

### Controls

@route('/ctct')
def ctct():
    __active_zoneLock.acquire()
    # Get Volume
    current_volume = str(active_zone.volume)
    # Get zones if zone management is turned on
    if zones_on:
        zones = raumfeld.getZones()
        active_zone_str_helper = [active_zone_udn == active_zone.UDN for zone in zones]
        active_zone_str_helper = [re.sub('True', 'Active', str(no)) for no in active_zone_str_helper]
        active_zone_str_helper = [re.sub('False', 'Activate', str(no)) for no in active_zone_str_helper]
        unassigned = raumfeld.getUnassignedRooms()

    else:
        active_zone_str_helper = []
        zones = []
        unassigned = []
            # Get unassigned rooms
    sleep(0)
    TState = str(active_zone.transport_state)
    if str(TState) == "STOPPED" or str(TState) == "PAUSED_PLAYBACK":
            play_button = 'play_shiny.png'
    else:
            play_button = 'pause_shiny.png'
    sleep(2)
    __active_zoneLock.release()
    return template('controls', play_button=play_button, zones_on=zones_on, zones=zones, unassigned=unassigned, active_zone_str_helper=active_zone_str_helper, current_volume=current_volume)


### Player UI (for HTML see player.tbl /shinynew_player.tbl)

@route('/player')
def player():
        _, URIs, Meta, titles, cover_imgs = read_favs()
        fav_count = range(1,len(URIs) + 1)
        podcasts = pod_read()
        return template('shinynew_player', fav_count = fav_count, titles = titles, podcasts = podcasts, cover_imgs = cover_imgs)

# Seekbar App

app = Bottle()

def time_getter():
    __active_zoneLock.acquire()
    try:
        absTime = str(active_zone.track_abs_time)
        duration = str(active_zone.track_duration)
    except :
        duration = '00:00:00'
        absTime = '00:00:00'
    #sleep(2)
    __active_zoneLock.release()
    return absTime, duration

def data_getter():
    namespaces = {'dc':'http://purl.org/dc/elements/1.1/','upnp':'urn:schemas-upnp-org:metadata-1-0/upnp/','raumfeld':'urn:schemas-raumfeld-com:meta-data/raumfeld/'}

    __active_zoneLock.acquire()
    trackMeta = active_zone.track_metadata
    #sleep(2)
    __active_zoneLock.release()
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

def check_title_change(old_track_title, old_tstate):
    '''check if the currently playing title is different from old_track_title'''
    global TState
    namespaces = {'dc':'http://purl.org/dc/elements/1.1/','upnp':'urn:schemas-upnp-org:metadata-1-0/upnp/','raumfeld':'urn:schemas-raumfeld-com:meta-data/raumfeld/'}

    __active_zoneLock.acquire()

    try:
        trackMeta = active_zone.track_metadata
        trackMeta_tree = ET.fromstring(unicode(trackMeta).encode('utf8'))
        track_title = trackMeta_tree[0].find('dc:title', namespaces).text
    except:
        track_title = 'Unknown'

    try:
        TState = str(active_zone.transport_state)
    except:
        print("TState Unknown")
    #sleep(2)
    __active_zoneLock.release()

    if old_track_title != track_title or str(TState) != old_tstate:
        return True
    return False

def ws_maker():
    global seek_change
    #active_zone = copy.copy(raumfeld.getZoneByUDN(active_zone_udn))
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    absTime_old = ''
    old_track_title = '_Old__Title_'
    old_tstate = ''
    while 1:
        try:
            if check_title_change(old_track_title, old_tstate) or seek_change:
                if str(TState) == "STOPPED" or str(TState) == "PAUSED_PLAYBACK":
                    tstate = "pp"
                else:
                    tstate = "p"

                old_tstate = TState
                sleep(1)
                try:
                    track_info = data_getter()
                except:
                    track_info = ['', 'http://lorempixel.com/g/400/400/broken', '','','']
                time_info = time_getter()
                ws_ms = str(tstate) + "|||" + "|||".join(time_info) + "|||" + "|||".join(track_info)
                old_track_title = track_info[0]
                wsock.send(ws_ms)
                if seek_change:
                    seek_change = False
            sleep(3)
        except WebSocketError:
            wsock.close()
            break

mount('/seekbar/',app)

# This creates a queue object for every request.

@app.route('/websocket')
def handle_websocket():
    body = queue.Queue()
    worker = ws_maker()
    worker.on_data(body.put)
    worker.on_finish(lambda: body.put(StopIteration))
    worker.start()
    return body

@route('/sbsb')
def sbsb():
    return template('cover_seekbar')

raumfeld.registerChangeCallback(discover_active_zone)
raumfeld.debug = True
raumfeld.init()

resetUpdateAvailableEventThread = threading.Thread(target=__resetUpdateAvailableEventThread)
resetUpdateAvailableEventThread.daemon = True
resetUpdateAvailableEventThread.start()

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
host = "0.0.0.0"
port = 8080
server = WSGIServer((host, port), default_app(), handler_class=WebSocketHandler)
print "Server running @ http://%s:%s/" % (host,port)
server.serve_forever()
#debug(True)
#run(host='0.0.0.0', port = 8080, reloader = True)
#run(host='0.0.0.0', port=8080, server='gevent')
