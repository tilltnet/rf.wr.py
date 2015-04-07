rf.wr.py 0.5-beta
========

rf.wr is a remote for the raumfeld multi-room audio system. It runs as a server in your local network and is accessed through a browser or other http capable clients.

![Screenshot](/images/features2.png)

rf.wr provides almost all functions of the official raumfeld app to every device connected to your local network that has a web browser installed. In addition it allows you to playback external streams, audio files and podcasts.

rf.wr.py uses [PyRaumfeld](https://github.com/maierp/PyRaumfeld) and [bottle.py](http://bottlepy.org/docs/dev/index.html) (with gevent as the server engine).

Install (for 0.5beta)
-------
*Notice:* Starting with 0.5 rf.wr [binaries for different systems are available](https://github.com/tilltnet/rf.wr.py/tree/master/zip). (For now, only Windows 64-bit and GNU/Linux 64-bit versions are provided, for all other platforms follow the instructions for manual installation below.)

*These instructions should basically work on most GNU/Linux and MacOSX systems. With python installed it is possible to run rf.wr on a Windows machine (use packaged binaries or use/install python2.7).*

You need to have python2.7 at least and git needs to be installed for the following instructions.

The libraries bottly.py, gevent, gevent-websocket and PyRaumfeld are required to run the server. If you installed raumfeld-python or PyRaumfeld before unistall it with 'pip uninstall raumfeld'. Then run the following commands to install the libraries.

    pip install pysimplesoap bottle gevent gevent-websocket
    pip install git+git://github.com/tilltnet/PyRaumfeld

Create a folder in your home directory, download and unzip the files to it:

    mkdir ~/rfwr
    cd ~/rfwr
    wget https://github.com/tilltnet/rf.wr.py/blob/master/zip/rfwrpy0.5beta.zip
    unzip rfwrpy0.5alpha2.zip

Manually downloading and unzipping the zip File via the github website will work just as well.

Execute
-------

###*Execute Manually*
If you have manually installed rf.wr follow these steps in a console pointed at the rfwr folder:

	python2.7 rfwr.py &

Or, if you want to start the server in the background and possibly through ssh, use:

	nohup python2.7 rfwr.py &


###*Windows* (pre-built executables)

 - unzip the file to a folder and execute rfwr.exe
 - grant Firewall Access.

There is a bug in the windows version where it sometimes fails to find the raumfeld system. Best way to fix it, is to place a file named 'host_ip' in the rf.wr folder and put the IP address of your raumfeld host in that file. Like that:

'.../rfwr/host_ip'

    192.168.0.22

###*GNU/Linux* (pre-built executables)

- unzip zip-file to a folder
- make 'rfwr.sh' executable (chmod +x rfwr.sh)
- run './rfwr.sh' (use nohup as shown below, if needed)


##When the server is up
- open the browser on any machine in your local network and point it to

  [http://your.rfwrhost:8080/player](http://your.machine:8080/player)

  replacing your.rfwrhost with the IP or name address of your server. For me it is:

  [http://musicbox.local:8080/player](http://musicbox.local:8080/player)

  If rf.wr runs on the same machine you are accessing it from it's:

  [http://localhost:8080/player](http://localhost:8080/player):

If you encounter dependency errors go back to pip installing the missing packages. The used libraries are not that exotic and should be already available on most systems. If nothing helps, report a bug.

Commands
--------

This is a list of commands, that can be invoked through http get and post
requests. First of all the following command gives you a gui to access all
features:

```
/player
```

This is the default address and most of the commands and functions can be accessed through its UI. You can send simple control commands (play, pause, volume, etc.), browse media, access the podcast functionality, manage the music zones etc.

###Control and Queue

```
/play
/pause
/play_pause
/next
/previous
/playURI - let's you enter URI to stream
/track/<no> - Play specified track no. of the current playlist.
/play_id/<object id> - Play any content from the raumfeld MediaServer
/queue/next/<container id> - commands to add music to the current queue
/queue/last/<container id>
/queue/track_next/<item id>
/queue/track_last/<item id>
```
###Volume
```
/vol/<no> - Set volume with <no> ranging between 0 and 100 (careful!).
/volbar - Simple UI for controlling room volumes in the active music zone.
/vol_room/<room-name>/<no> - Set the room volume of a certain room.
/mute - Mutes the active musix zone.
```
###Maintanance
````
/conf - This page let's you configure some options for the /player page.
/info - Shows current transport info and gives access to the raumfeld settings.
```

###MediaServer

```
/media - Browse music on the raumfeld MediaServer (including TuneIn, WiMP, Line-In)
/media/<object id> - Browse directly to a certain location on the server
/search/<object id> - Open a search dialoge for a certain location.

```
###Music Zones

```
/zones - Let's you choose and modify your music zones.
/zone/<no> - Set the 'Active' zone. <no> is a number (see /zones to get music zone numbers).
/new_zone/<room-name> - Create a new room by providing the name of the room to use.
/add_room/<room-name> - Add a room to the active music zone.
/drop_room/<room-name> - Drop a room from the active music zone.
```

###Favorites and Podcasts
(these are the shortcuts on the /player startpage)
```
/addfav - Add a favorite.
/setfav/<no> - Overwrite a previously set favorite.
/fav/<no> - Play a favorite.
/playPodcast and /addPodcast - HTTP POST METHOD - accepts 'feed_url' parameter
/playPodcast/<no>
/delPodcast/<no>
```

###Special
```
/comehome - Checks if playback has STOPPED, if so it sends the command to play the first favorite/ shortcut and welcomes the user home.
```

##To Do List
- Room Profiles OR: command that creates zones with /room1/room2/room3
- Alarm Clock/ Sleep Timer Feature
- gpodder.net as podcast search?!
