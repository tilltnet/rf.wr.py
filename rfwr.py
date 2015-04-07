# -*- coding: UTF-8 -*-
from gevent import monkey; monkey.patch_all()

import xml.etree.ElementTree as ET
from bottle import route, run, template, get, post, request, redirect
import raumfeld
from bottle import static_file, response
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
import pickle

# Set sleep values
ctct_sleep = 2
ws_maker_sleep = 1

# Change execution path to __file__ location.
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Check if cache folder exists; if not create it.
cache_dir = 'art_cache/'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

# Setting up threading stuff and global vars.
updateAvailableEvent = threading.Event()
__active_zoneLock = threading.RLock()
__browseLock = threading.RLock()

active_zone = ""
zones_on =  False
seek_change = False
TState = ''
namespaces = {'dc':'http://purl.org/dc/elements/1.1/','upnp':'urn:schemas-upnp-org:metadata-1-0/upnp/','raumfeld':'urn:schemas-raumfeld-com:meta-data/raumfeld/','':'urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/'}

# Create active_zone_udn file if it does not exist.
if os.path.isfile('active_zone_udn')==False:
    with open('active_zone_udn', 'w') as f:
            f.write('udn')

# Read active_zone_udn from file.
with open('active_zone_udn', 'a+') as f:
        active_zone_udn = f.readlines()[0]

# Save and load python objects to/ from disk
# http://stackoverflow.com/questions/19201290/python-how-to-read-save-dict-to-file
def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f) # pickle.HIGHEST_PROTOCOL <- faster

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

# Create conf.pkl file if it does not exist.
if os.path.isfile('conf.pkl')==False:
    conf_dict = {'cache_player':'1',
             'cache_browse':'0',
             'cache_search':'0',
             'show_setup':'1',
             'folder':'0/My Music/Favorites/RecentlyPlayed',
             'browse_limit':'100',
             'search_limit':'100'}
    save_obj(conf_dict, 'conf')
else:
    conf_dict = load_obj('conf')

# ???
def __updateAvailableCallback():
    global updateAvailableEvent
    updateAvailableEvent.set()

def __resetUpdateAvailableEventThread():
    global updateAvailableEvent
    while True:
        updateAvailableEvent.wait()
        updateAvailableEvent.clear()

# Callback function, called when changes to zones are registered.
def discover_active_zone():
    __active_zoneLock.acquire()
    global active_zone
    active_zone = raumfeld.getZoneByUDN(active_zone_udn)
    if active_zone == None:
        active_zone = raumfeld.getZones()[0]
    sleep(2)
    __active_zoneLock.release()
    return active_zone

# Redirect root to /player.
@route('/')
def index():
        redirect('/player')

# Image and file routes.
@route('/images/<filename:re:.*\.*>')
def send_image(filename):
        return static_file(filename, root='images/')

@route('/art_cache/<filename:re:.*\.*>')
def send_cached_image(filename):
        return static_file(filename, root='art_cache/')

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

@route('/conf')
def conf_():
    return template('''
                    <head>
                        <link rel="stylesheet" href="/static/normalize.css">
                        <link rel="stylesheet" href="/static/rfwr.css">
                        <link rel="icon" href="/images/favico_play.png">
                      </head>
                    <h1>rf.wr Config/ First Time Setup Page</h1>
                    <form action="/conf" method="post">

                        <h2>Cover Caches</h2>
                        <ul>
                            <li>Activating Cover Caches will result in slower initial
                            page loads, while every ensuing page load will be much
                            faster.</li>
                            <li>Caches will take up disk space (on the rf.wr
                            host)!</li>
                        </ul>
                        Player/ Startpage Cache:
                        <input type='radio' name='cache_player' value="1" {{"checked='checked'" if conf_dict['cache_player'] == '1' else ''}}">On
                        <input type='radio' name='cache_player' value="0" {{"checked='checked'" if conf_dict['cache_player'] == '0' else ''}}">Off
                        <br><br>
                        Browse Cache:
                        <input type='radio' name='cache_browse' value="1" {{"checked='checked'" if conf_dict['cache_browse'] == '1' else ''}}">On
                        <input type='radio' name='cache_browse' value="0" {{"checked='checked'" if conf_dict['cache_browse'] == '0' else ''}}">Off
                        <ul>
                            <li>(It is advisable to turn off the browse
                            cache, when exploring a lot of new music.)</li>
                        </ul>
                        <br>
                        Search Cache:
                        <input type='radio' name='cache_search' value="1" {{"checked='checked'" if conf_dict['cache_search'] == '1' else ''}}">On
                        <input type='radio' name='cache_search' value="0" {{"checked='checked'" if conf_dict['cache_search'] == '0' else ''}}">Off
                        <ul>
                            <li>(Only turn on the search cache, if you know why.)</li>
                        </ul>

                        <h2>Media Server</h2>
                        Browse Limit:
                        <input type='text' name="browse_limit" value="{{conf_dict['browse_limit']}}" size="5"></input>
                        <br>
                        Search Limit:
                        <input type='text' name="search_limit" value="{{conf_dict['search_limit']}}" size="5"></input>
                        <br>

                        <h2>Startpage Folder</h2>
                        This folder will be displayed on the /player Page.
                        <input name="folder" type='text' value="{{conf_dict['folder']}}" size="50"></input>
                        <ul>
                            <li>(needs to be valid object id on the raumfeld MediaServer!)</li>
                        </ul>
                        <br>
                        <input type="submit" value="Save Config">
                    </form>
                    <ul style="list-style-type:square">
                        <li>
                            <a href="/info" target="_blank">Raumfeld Info and Settings</a>
                        </li>
                        <li>
                            <a href="/player">Back To Player</a>
                        </li>
                    <ul>
                    ''', conf_dict = conf_dict)

@post('/conf')
def conf_():
    global conf_dict
    conf_dict = {'cache_player' : request.forms.get('cache_player'),
        'cache_browse' : request.forms.get('cache_browse'),
        'cache_search' : request.forms.get('cache_search'),
        'browse_limit' : request.forms.get('browse_limit'),
        'search_limit' : request.forms.get('search_limit'),
        'folder' : request.forms.get('folder'),
        'show_setup' : '0'}
    save_obj(conf_dict, 'conf')
    sleep(2)
    redirect('/player')


### Media Server

def cache_cover_art(albumArtURI, cache_host):
    '''Cache cover art into the global cache dir'''
    file_name = hashlib.md5(albumArtURI).hexdigest() + '.jpg'
    file_path = 'http://' + cache_host + '/' + cache_dir + file_name

    # store in file
    if not os.path.isfile(cache_dir + file_name):
        # Get Picture
        try:
            pic = urllib2.urlopen(albumArtURI)
            with open(cache_dir + file_name, 'wb') as f:
                f.write(pic.read())
        except:
            file_path = albumArtURI
    #return path in dict
    return {'cached_art':file_path}

def didl_to_dict(tree, cache_host = ''):
    '''Returns DIDL Metadata as a list of dicts'''
    container_tts = []
    #tree = ET.fromstring(xml_string)
    for j in range(0, len(tree)):
        container_tt = {}
        for i in range(0,len(tree[j])):
            tag_ = tree[j][i].tag
            text_ = tree[j][i].text
            _, tag_ = tag_.split('}')
            container_tt[tag_] = text_

            if tag_ == 'res':
                container_tt.update(tree[j][i].attrib)
                if 'duration' in container_tt:

                    duration, _ = container_tt['duration'].split('.')
                    duration_split = duration.split(':')
                    if int(duration_split[0]) == 0:
                        duration = ':'.join([duration_split[1], duration_split[2]])
                    container_tt['duration'] = duration
            if tag_ == 'albumArtURI' and cache_host != '':
                container_tt.update(cache_cover_art(container_tt['albumArtURI'], cache_host))

        if 'albumArtURI' not in container_tt:
            container_tt['albumArtURI'] = '/images/audio_www.png'
            container_tt['cached_art'] = '/images/audio_www.png'
        container_tt.update(tree[j].attrib)
        container_tts.append(container_tt)

    return container_tts

def browse_children(id_, count = "0", cache_host = ''):
    children_raw, count_returned = raumfeld.__mediaServer.browse_children(id_, count = count)
    tree = ET.fromstring(unicode(children_raw).encode('utf8'))
    children = didl_to_dict(tree, cache_host)
    return children, count_returned

def search_children(id_, search_criteria, count = conf_dict['search_limit'],  cache_host = ''):
    search_criteria = 'dc:title contains "' + search_criteria + '"'
    children_raw = raumfeld.__mediaServer.search(id_, search_criteria, "*", count)
    tree = ET.fromstring(unicode(children_raw).encode('utf8'))
    children = didl_to_dict(tree, cache_host)
    return children

def browse_meta(id_, fii = '0', cache_host =  ''):
    # Save Child Items/ Elements in xmltree thingy
    #try:
    meta_raw = raumfeld.__mediaServer.browse(id_)
    meta_raw = meta_raw.as_xml()
    meta_raw_tree = ET.fromstring(meta_raw)
    meta_raw = meta_raw_tree[0][0][0].text.encode('utf8')
    tree = ET.fromstring(meta_raw)
    #except:
    #    meta_raw = raumfeld.__mediaServer.browse(id)
    #    tree = ET.fromstring(unicode(meta_raw.as_xml()).encode('ISO-8859-1'))
    #    print('encoding error!?')
    # Extract Metadata
    meta = didl_to_dict(tree, cache_host)[0]



    # Create dlna-playcontainer url
    #id_ = "0/WiMP/MyWiMP/Playlists/6ea344aa-9030-46ca-8cb7-badea0b8108e"


    if 'res' in meta:
        URI_playcontainer = meta['res']
    else:
        if 'id' in meta:
            q_id = urllib.quote(tree[0].attrib['id'], '')
            q_udn = urllib.quote(raumfeld.__mediaServerUDN)
            urn_cd = "urn:upnp-org:serviceId:ContentDirectory"
            q_path = urllib.urlencode({'sid' : urn_cd, 'md' : '0', 'fii' : fii})
            URI_playcontainer = "dlna-playcontainer://" + q_udn + "?cid=" + q_id + "&"+ q_path
        else:
            URI_playcontainer = 'dlna-playcontainer://'

    #print(URI_playcontainer)
    meta.update({'playcontainer' : URI_playcontainer})
    return meta, meta_raw

@route('/play_id/<fii_id:path>')
def play_id(fii_id):
    fii_id_split = fii_id.split('/')
    fii = fii_id_split[0]
    id_split = fii_id_split[1:len(fii_id_split)]
    id_q = [urllib.quote(folder, '+/') for folder in id_split]
    id_q[1] = id_split[1]
    id_ = '/'.join(id_q)
    parent_id = '/'.join(id_q[0:len(id_q)-1])
    print(fii_id, id_, parent_id)
    #try:
    print('---' + id_)

    __browseLock.acquire()
    meta, meta_raw = browse_meta(id_)

    #except:
    #    return 'id not playable'
    if meta['class'] == 'object.container.person.musicArtist':
        all_tracks = browse_children(id_, 1)[0][0]
        meta, meta_raw = browse_meta(all_tracks['id'])
    elif meta['class'] == 'object.item.audioItem.musicTrack':
        meta, meta_raw = browse_meta(parent_id, fii)
    __active_zoneLock.acquire()
    active_zone.play(meta['playcontainer'], meta_raw.decode('UTF-8'))
    __active_zoneLock.release()

    __browseLock.release()

@route('/media/<id_:path>')
def media(id_):
    response.set_header("Cache-Control", "max-age=604800")
    if conf_dict['cache_browse'] == '1':
        host = request.get_header('host')
        album_art = 'cached_art'
    else:
        host = ''
        album_art = 'albumArtURI'
    id_split = id_.split('/')
    id_q = [urllib.quote(folder, '+/') for folder in id_split]
    id_q[1] = id_split[1]
    id_ = '/'.join(id_q)
    folder_up_id = '/'.join(id_q[0:len(id_q)-1])
    #print(id)
    __browseLock.acquire()
    #try:
    children, count_returned = browse_children(id_, count = conf_dict['browse_limit'], cache_host = host)
    print(count_returned)
    #except:
        #children = []
        #children, count_returned = browse_children(id)

        #print("no children")
    try:
        meta, _ = browse_meta(id_, cache_host = host)
    except:
        meta = {'title' : '', 'img' : '', 'album' : '', 'artist' : '', 'playcontainer' : '', 'upnp_class': ''}
        #print("no meta")
    __browseLock.release()
    return template('browse_search', children=children, meta=meta, folder_up_id=folder_up_id, id=id_, album_art = album_art)

@post('/search/<id_:path>')
def search(id_):
    response.set_header("Cache-Control", "max-age=604800")
    if conf_dict['cache_search'] == '1':
        host = request.get_header('host')
        album_art = 'cached_art'
    else:
        host = ''
        album_art = 'albumArtURI'
    search_criteria = request.forms.get('search_criteria')
    id_split = id_.split('/')
    id_q = [urllib.quote(folder, '+/') for folder in id_split]
    id_q[1] = id_split[1]
    id_ = '/'.join(id_q)
    folder_up_id = '/'.join(id_q[0:len(id_q)-1])

    try:
     children = search_children(id_, search_criteria = search_criteria, cache_host = host)
    except:
     children = []

    try:
     meta, _ = browse_meta(id_)
    except:
     meta = {'title' : '', 'img' : '', 'album' : '', 'artist' : '', 'playcontainer' : ''}
     #print("no meta")
    return template('browse_search', children=children, meta=meta, folder_up_id=folder_up_id, id=id_, album_art = album_art)

### Queue Management
@route('/queue/<mode_id:path>')
def q_ueue(mode_id):
    # Preparing mode and id_ vars
    mode_id_split = mode_id.split('/')
    mode = mode_id_split[0]
    id_split = mode_id_split[1:len(mode_id_split)]
    id_q = [urllib.quote(folder, '+/') for folder in id_split]
    id_q[1] = id_split[1]
    id_ = '/'.join(id_q)

    print(mode, id_)
    __active_zoneLock.acquire()
    __browseLock.acquire()
    try:
        queue_location = '0/Zones'
        queues, _ = browse_children(queue_location)
        queue_udn = urllib.quote(active_zone.UDN)
        queue_id = '/'.join([queue_location, queue_udn])

        queue_found = 0
        for queue_ in queues:
            if queue_['id'] == queue_id:
                queue_found = 1

        if queue_found == 0:
            raumfeld.__mediaServer.create_queue(desired_name = queue_udn, container_id = queue_location)
        _, queue_length = browse_children(queue_id)
        meta_raw = active_zone.uri_metadata
        tree = ET.fromstring(unicode(meta_raw).encode('utf8'))
        cur_meta = didl_to_dict(tree)[0]
        next_no = str(int(active_zone.position_info['track']))
        if cur_meta['parentID'].split('/')[1] != 'Zones':
            raumfeld.__mediaServer.remove_from_queue(queue_id, "0", str(queue_length))
            tracks_count = active_zone.media_info['tracks']
            meta, meta_raw = browse_meta(queue_id, str(int(next_no)-1))
            # adding cur playing id in queue
            raumfeld.__mediaServer.add_container(queue_id = queue_id, container_id = cur_meta['id'], end_index = tracks_count, position = "0")

            active_zone.bend(meta['playcontainer'], meta_raw)
            _, queue_length = browse_children(queue_id) # Refresh queue length

        try:
            _, container_length = browse_children(id_)
            end_index = str(int(container_length)-1)
        except Exception, e:
            end_index = 100
            print('container_length failed:' + str(e))

        if mode == 'start':
            raumfeld.__mediaServer.add_container(queue_id = queue_id, container_id = id_, end_index = end_index, position = queue_length)
        elif mode == 'next':
            raumfeld.__mediaServer.add_container(queue_id = queue_id, container_id = id_, end_index = end_index, position = next_no)
        elif mode == 'last':
            raumfeld.__mediaServer.add_container(queue_id = queue_id, container_id = id_, end_index = end_index, position = queue_length)
        elif mode == 'track_next':
            raumfeld.__mediaServer.add_item(queue_id = queue_id, object_id = id_, position = next_no)
        elif mode == 'track_last':
            raumfeld.__mediaServer.add_item(queue_id = queue_id, object_id = id_, position = queue_length)
    except Exception, e:
        print('Something went wrong with that queue operation:' + str(e))
    __browseLock.release()
    __active_zoneLock.release()
    return 'success! or not? check the logs'

### Music Zone Management
@route('/zone/<udn>')
def zone(udn):
        """Change active zone by UDN"""
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
        sleep(ctct_sleep)
        discover_active_zone()
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
        sleep(ctct_sleep)
        redirect('/ctct')

@route('/drop_room/<name>')
def drop_room(name):
        """Drops the room of the provided name"""
        rooms = raumfeld.getRoomsByName(name)
        room = rooms[0]
        raumfeld.dropRoomByUDN(room.UDN)
        sleep(ctct_sleep)
        redirect('/ctct')


@route('/add_room/<name>')
def add_room(name):
        rooms = raumfeld.getRoomsByName(name)
        room = rooms[0]
        zone = discover_active_zone()
        raumfeld.connectRoomToZone(room.UDN, zone.UDN)
        sleep(ctct_sleep)
        redirect('/ctct')

@route('/new_zone/<name>')
def new_zone(name):
        rooms = raumfeld.getRoomsByName(name)
        room = rooms[0]
        raumfeld.connectRoomToZone(room.UDN)
        sleep(ctct_sleep)
        sleep(1)
        redirect('/ctct')

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
        #URI = "http://dradio_mp3_dwissen_m.akacast.akamaistream.net/7/728/142684/v1/gnl.akacast.akamaistream.net/dradio_mp3_dwissen_m"

        __active_zoneLock.acquire()
        TState = str(active_zone.transport_state)


        if str(TState) == "STOPPED" or str(TState) == "PAUSED_PLAYBACK":
                active_zone.mute = False
                active_zone.volume = 50
                no, URIs, Meta, _, _ = read_favs(0)
                favURI = URIs[0]
                favMeta = Meta[0]
                active_zone.play(favURI, favMeta)
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
        __active_zoneLock.acquire()
        active_zone.mute = False
        active_zone.volume = int(no)
        __active_zoneLock.release()

        redirect('/ctct')

@route('/vol_room/<room_no:path>')
def vol_room(room_no):
        room, no = room_no.split('/')
        __active_zoneLock.acquire()
        room_sel = raumfeld.getRoomsByName(room)[0]
        room_sel.volume = int(no)
        #print(room_sel, no, room, room_sel.Name)
        __active_zoneLock.release()

        redirect('/volbar')

@route('/volbar')
def volbar():
        __active_zoneLock.acquire()
        current_volume = active_zone.volume
        try:
            room_volumes = [[room.Name, room.volume] for room in active_zone._rooms]
            room_volumes.append(['All Rooms', current_volume])
        except:
            room_volumes = [{'Rooms failed!':'0'}]
            print('Room volume failed!')
        __active_zoneLock.release()
        return template('volbar', room_volumes=room_volumes)

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

def read_favs(no=1, cache_host = ''):
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
        if conf_dict['cache_player'] == '1':
            cover_imgs = [cache_cover_art(cover_img, cache_host)['cached_art'] for cover_img in cover_imgs]
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
        __active_zoneLock.acquire()

        zones = raumfeld.getZones()
        active_zone_str_helper = [active_zone_udn == zone.UDN for zone in zones]
        active_zone_str_helper = [re.sub('True', 'Active', str(no)) for no in active_zone_str_helper]
        active_zone_str_helper = [re.sub('False', 'Activate', str(no)) for no in active_zone_str_helper]
        unassigned = raumfeld.getUnassignedRooms()

        current_track = active_zone.position_info
        current_media = active_zone.media_info

        track_raw = unicode(current_track['track_metadata']).encode('utf8')
        tree = ET.fromstring(track_raw)
        track_meta = didl_to_dict(tree)[0]
        tree = ET.fromstring(unicode(current_track['track_metadata']).encode('utf8'))
        media_meta = didl_to_dict(tree)[0]
        host_address = raumfeld.hostBaseURL
        host_ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', host_address)[0]

        __active_zoneLock.release()
        return template('info', zones=zones, unassigned=unassigned, active_zone_str_helper=active_zone_str_helper, track_meta = track_meta, media_meta = media_meta, host_ip = host_ip)

### Controls

@route('/ctct')
def ctct():
    __active_zoneLock.acquire()

    # Get Volume
    current_volume = str(active_zone.volume)

    # Get zones if zone management is turned on
    if zones_on:
        zones = raumfeld.getZones()
        active_zone_str_helper = [active_zone_udn == zone.UDN for zone in zones]
        active_zone_str_helper = [re.sub('True', 'Active', str(no)) for no in active_zone_str_helper]
        active_zone_str_helper = [re.sub('False', 'Activate', str(no)) for no in active_zone_str_helper]
        unassigned = raumfeld.getUnassignedRooms()

    else:
        active_zone_str_helper = []
        zones = []
        unassigned = []

    sleep(1)
    TState = str(active_zone.transport_state)
    if str(TState) == "STOPPED" or str(TState) == "PAUSED_PLAYBACK":
            play_button = 'play_shiny.png'
    else:
            play_button = 'pause_shiny.png'

    __active_zoneLock.release()

    return template('controls', play_button=play_button, zones_on=zones_on, zones=zones, unassigned=unassigned, active_zone_str_helper=active_zone_str_helper, current_volume=current_volume)

### Player UI

@route('/player')
def player():
        '''Player UI (for HTML see player.tbl /shinynew_player.tbl)'''
        if conf_dict['show_setup'] == '1':
            redirect('/conf')
        response.set_header("Cache-Control", "max-age=604800")
        print(conf_dict['cache_player'])
        if conf_dict['cache_player'] == '1':
            host = request.get_header('host')
            album_art = 'cached_art'
        else:
            host = ''
            album_art = 'albumArtURI'
        _, URIs, Meta, titles, cover_imgs = read_favs(cache_host = host)
        fav_count = range(1,len(URIs) + 1)
        podcasts = pod_read()
        id_ = conf_dict['folder']
        id_split = id_.split('/')
        folder_name = id_split[len(id_split)-1]
        try:
            children, _ = browse_children(id_, cache_host = host)
        except:
            children = []
        return template('shinynew_player', fav_count = fav_count, titles = titles, podcasts = podcasts, cover_imgs = cover_imgs, children = children, folder_name = folder_name, album_art = album_art)

# Seekbar App

app = Bottle()

def position_getter():
    __active_zoneLock.acquire()
    try:
        info_ = active_zone.position_info
        absTime = str(info_['abs_time'])
        duration = str(info_['track_duration'])
        track_no = str(info_['track'])
        # def cut_zeros(hhmmss):
        #     hhmmss_split = hhmmss.split(':')
        #     if int(hhmmss_split[0]) == 0:
        #         hhmmss = ':'.join([hhmmss_split[1], hhmmss_split[2]])
        #     return hhmmss
        # absTime = cut_zeros(absTime)
        # duration = cut_zeros(duration)
    except :
        duration = '00:00:00'
        absTime = '00:00:00'
        track_no = '0'
    #sleep(2)
    __active_zoneLock.release()
    return absTime, duration, track_no

def data_getter():
    namespaces = {'dc':'http://purl.org/dc/elements/1.1/','upnp':'urn:schemas-upnp-org:metadata-1-0/upnp/','raumfeld':'urn:schemas-raumfeld-com:meta-data/raumfeld/'}

    __active_zoneLock.acquire()
    try:
        trackMeta = active_zone.track_metadata
        #sleep(2)
        trackMeta_tree = ET.fromstring(unicode(trackMeta).encode('utf8'))
    except:
        print('encoding error!?')

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
        if track_album == None:
            track_album = ''
    except:
        track_album = ''
    try:
        track_artist = trackMeta_tree[0].find('upnp:artist', namespaces).text
    except:
        track_artist = ''

    __active_zoneLock.release()
    return track_title, track_img, track_artist, track_album

def check_title_change():
    '''Thread for checking if the currently playing title is different from old_track_title'''
    global TState, cur_track_title, ws_ms, seek_change
    old_tstate = ''

    old_track_title = "__Old_Track_Title___"
    namespaces = {'dc':'http://purl.org/dc/elements/1.1/','upnp':'urn:schemas-upnp-org:metadata-1-0/upnp/','raumfeld':'urn:schemas-raumfeld-com:meta-data/raumfeld/'}

    while 1:
        __active_zoneLock.acquire()

        try:
            trackMeta = active_zone.track_metadata
            trackMeta_tree = ET.fromstring(unicode(trackMeta).encode('utf8'))
            cur_track_title = trackMeta_tree[0].find('dc:title', namespaces).text
            if cur_track_title == None:
                cur_track_title = 'Unknown'
        except:
            cur_track_title = 'Unknown'

        try:
            TState = str(active_zone.transport_state)
        except Exception, e:
            print("TState Unknown:" + str(e))
        #sleep(2)

        __active_zoneLock.release()

        if old_track_title != cur_track_title or seek_change or str(TState) != old_tstate:
            __active_zoneLock.acquire()
            try:
                if str(TState) == "STOPPED" or str(TState) == "PAUSED_PLAYBACK":
                    tstate = "pp"
                else:
                    tstate = "p"
                if tstate == None:
                    tstate = "p"
            except:
                tstate = "p"
            __active_zoneLock.release()

            try:
                track_info = data_getter()
            except Exception, e:
                print('data_getter failed:' + str(e))
                track_info = ['Unknown', 'http://lorempixel.com/g/400/400/', '','','']

            try:
                time_info = position_getter()
            except Exception, e:
                    print('position_getter failed:' + str(e))
                    time_info = ['','','']

            #print(tstate)
            #print(time_info)
            #print(track_info)
            #print(tstate, time_info, track_info)
            try:
                ws_ms = str(tstate) + "|||" + "|||".join(time_info) + "|||" + "|||".join(track_info)
            except Exception, e:
                print('ws_ms error:', str(tstate), time_info, track_info, str(e))

            if seek_change:
                seek_change = False

            old_tstate = TState
            old_track_title = track_info[0]

        #__active_zoneLock.release()
        sleep(5)

def ws_maker():

    #active_zone = copy.copy(raumfeld.getZoneByUDN(active_zone_udn))
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    first_time = True

    ws_ms_old = ''
    while 1:
        try:
            if ws_ms != ws_ms_old or first_time:
                wsock.send(ws_ms)
                ws_ms_old = ws_ms
            if first_time:
                first_time = False
            sleep(ws_maker_sleep)
        except WebSocketError:
            #wsock.close()
            break


mount('/seekbar/', app)

# This creates a queue object for every request.

@app.route('/websocket')
def handle_websocket():
    worker_success = 0
    while worker_success == 0:
        try:
            body = queue.Queue()
            worker = ws_maker()
            worker.on_data(body.put)
            worker.on_finish(lambda: body.put(StopIteration))
            worker.start()
            worker_success = 1
            return body
        except Exception, e:
            print("websocket failed:" + str(e))
            break

@route('/sbsb')
def sbsb():
    '''Seekbar UI'''
    return template('cover_seekbar')

@route('/playlist')
def playlist():
    __active_zoneLock.acquire()
    cur_track = str(int(active_zone.position_info['track']))
    meta_raw = active_zone.uri_metadata
    __active_zoneLock.release()
    tree = ET.fromstring(unicode(meta_raw).encode('utf8'))
    cur_meta = didl_to_dict(tree)[0]
    queue_id = cur_meta['id']


    #queue_location = '0/Zones'
    #queue_udn = urllib.quote(active_zone.UDN)
    #queue_id = '/'.join([queue_location, queue_udn])
    __browseLock.acquire()
    try:
        if (cur_meta['class'] == 'object.container.album.musicAlbum' or cur_meta['class'] == 'object.container.trackContainer' or
            cur_meta['class'] == 'object.container.playlistContainer' or cur_meta['class'] == 'object.container.trackContainer.wimp' or
            cur_meta['class'] == 'object.container.playlistContainer.queue'):
            playlist_items, item_count = browse_children(cur_meta['id'])
        elif cur_meta['class'] == 'object.container.person.musicArtist':
            all_tracks = browse_children(queue_id, 1)[0][0]
            playlist_items, item_count = browse_children(all_tracks['id'])
        elif cur_meta['class'] == 'object.item.audioItem.audioBroadcast.radio':
            playlist_items, item_count = [cur_meta], '0'
        else:
            playlist_items, item_count = browse_children(cur_meta['parentID'])
    except:
        playlist_items, item_count = [cur_meta], '0'
    __browseLock.release()

    return template('playlist', playlist_items = playlist_items, queue_id = queue_id, item_count = item_count, cur_track = cur_track)

raumfeld.registerChangeCallback(discover_active_zone)
raumfeld.debug = True

if os.path.isfile('host_ip')==False:
    raumfeld.init()
else:
    with open('host_ip', 'a+') as f:
        host_ip = f.readlines()[0]
    raumfeld.init(host_ip)

check_title_change_thread = threading.Thread(target=check_title_change)
check_title_change_thread.daemon = True
check_title_change_thread.start()

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
