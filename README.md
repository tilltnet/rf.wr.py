rf.wr.py 0.5-alpha
========

raumfeld web remote in python

![Screenshot](/images/features.png)

rf.wr is a small webserver that let's you control the playback of your raumfeld system through a browser. You can submit URIs of audio-streams and -files, favorites of currently playing content can be set (These favorites differ from the one in the official Raumfeld App!) and there is a rudimentary support for podcast playback. **Update(11.01.2015): The newest version includes a Music Zone Manager and supports http commands for building and changing music zones.** You might want to run rf.wr on a small embedded linux machine as the raspberry pi or possibly your router (basically every system that can run python code should be compatible).

rf.wr.py uses [PyRaumfeld](https://github.com/maierp/PyRaumfeld) and [bottle.py](http://bottlepy.org/docs/dev/index.html) (with gevent as the server engine).

Install (for 0.5alpha2)
-------
*Notice:* Starting with 0.5 rf.wr [binaries for different systems are available](https://github.com/tilltnet/rf.wr.py/tree/master/zip). For now, only Windows 64-bit and GNU/Linux 64-bit versions are provided, for all other platforms follow the instructions for manual installation below.

*These instructions should basically work on most GNU/Linux and MacOSX systems. With python installed it is possible to run rf.wr on a Windows machine (use packaged binaries or use/install python2.7).*

You need to have python2.7 at least and git needs to be installed for the following instructions.

The libraries bottly.py, gevent, gevent-websocket and PyRaumfeld are required to run the server. If you installed raumfeld-python or PyRaumfeld before unistall it with 'pip uninstall raumfeld'. Then run the following commands to install the libraries.

    pip install pysimplesoap bottle gevent gevent-websocket
    pip install git+git://github.com/tilltnet/PyRaumfeld

Create a folder in your home directory, download and unzip the files to it:

    mkdir ~/rfwr
    cd ~/rfwr
    wget https://github.com/tilltnet/rf.wr.py/blob/master/zip/rfwrpy0.5alpha2.zip
    unzip rfwrpy0.5alpha2.zip

Manually downloading and unzipping the zip File via the github website will work just as well.

Execute
-------
If you are using the pre-built executables:
 - on Windows unzip zip-file to a folder and execute rfwr.exe; grant Firewall Access; done (but: There is a bug in the windows version where it sometimes fails to find the raumfeld system; if that happens wait a bit and try again and please report anything helpful to me!)
 - on GNU/Linux: unzip zip-file to a folder; make 'rfwr.sh' executable (chmod +x rfwr.sh); run './rfwr.sh' (use nohup as shown below, if needed)

If you have manually installed rf.wr follow these steps and are still in the folder run:

	python2.7 rfwr.py &

Or, if you want to start the server in the background and possible through ssh, use:

	nohup python2.7 rfwr.py &

"It works!" Then open the browser on any machine in your local network and point it to

[http://your.machine:8080/player](http://your.machine:8080/player)

replacing your.machine with the IP or name address of your server. For me it is:

[http://musicbox.local:8080/player](http://musicbox.local:8080/player)

"It's not working!" If you encounter dependency errors go back to pip installing the missing packages. The used libraries are not that exotic and should be already available on most systems. If nothing helps, report a bug.

Commands
--------

This is a list of commands, that can be invoked through http get and post
requests, but first of all the following command gives you a gui to access all
features:

```
/player
```

This is the default address and most of the commands and functions can be accessed through its UI. You can send simple control commands (play, pause, volume, etc.), set/ play favorites and access the podcast functionality. The music zone management has
a seperate UI.

###Simple control

```
/play
/pause
/next
/previous
/playURI - GET - let's you enter URI to stream
/vol/<no> - Set volume with <no> ranging between 0 and 100 (careful!).
/info - Shows current transport info (CurrentURI, CurrentURIMetaData, TrackURI, TrackMetaData).
/track/<no> - Play specified track no. of the current playlist.
```
###Music Zones

```
/zones - Let's you choose and modify your music zones.
/zone/<no> - Set the 'Active' zone. <no> is a number (see /zones to get music zone numbers).
/new_zone/<room-name> - Create a new room by providing the name of the room to use.
/add_room/<room-name> - Add a room to the active music zone.
/drop_room/<room-name> - Drop a room from the active music zone.
```

###Favorites

```
/addfav - Add a favorite.
/setfav/<no> - Overwrite a previously set favorite.
/fav/<no> - Play a favorite.
/playPodcast and /addPodcast - HTTP POST METHOD - accept 'feed_url' parameter
/playPodcast/<no>
/delPodcast/<no>
```

###Special
```
/comehome - Checks if playback has STOPPED, if so it sends the command to play a stream and welcomes the user home.
```

##To Do List
- Room Profiles OR: command that creates zones with /room1/room2/room3
- Alarm Clock/ Sleep Timer Feature
- Media Library support
- gpodder.net as podcast search?!
