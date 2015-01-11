rf.wr(.py)
==========

a raumfeld web remote in python

![Screenshot](/rfwr.png)

-	Stream and save audio addresses (mp3, ogg, etc.), favorites and podcasts.
-	Room Management (Update: 11.01.2015).
-	Automation friendly through http commands.

rf.wr is a small webserver that let's you control the playback of your raumfeld system through a browser. You can submit URIs of audio-streams and -files, favorites of currently playing content can be set (These favorites differ from the one in the official Raumfeld App!) and there is a rudimentary support for podcast playback. **Update(11.01.2015): The newest version includes a Music Zone Manager and supports http commands for building and changing music zones.** You might want to run rf.wr on a small embedded linux machine as the raspberry pi or possibly your router.

rf.wr uses [raumfeld-python](https://github.com/tfeldmann/python-raumfeld) (with minor changes) and [bottle.py](http://bottlepy.org/docs/dev/index.html).

Install
-------

*These instructions should basically work on most GNU/Linux and MacOSX Systems. With python installed it is possible to run rf.wr on a Windows machine (untestet!).*

You need to have python2.7 at least and git needs to be installed.

The libraries bottle.py and raumfeld-python are required to run the server. If you installed raumfeld-python before unistall it with 'pip uninstall raumfeld'. Then run the following commands to install both libraries.

```
pip install bottle
pip install git+git://github.com/tilltnet/python-raumfeld
```

Now to download rf.wr: Change to your desired folder.

```
cd /home/user/somewhere/
```

wget and unzip the files from github.

```
wget https://github.com/tilltnet/rf.wr.py/archive/master.zip
unzip master.zip
```

This creates the folder 'rf.wr.py-master'.

Manually downloading and unzipping the zip File via the github website will work just as well.

Execute
-------

Change to the folder you just created with 'cd rf.wr.py-master' and run:

```
python2.7 rfwr.py &
```

Or, if you want to start the server in the background and possible through ssh, use:

```
nohup python2.7 rfwr.py &
```

"It's not working!" If you encounter dependency errors go back to pip installing the missing packages. The used libraries are not that exotic and should be already available on most systems.

"It works!" Then open the browser on any machine in your local network and point it to

[http://your.machine:8080/player](http://your.machine:8080/player)

replacing your.machine with the IP or name address of your server. For me it is:

[http://musicbox.local:8080/player](http://musicbox.local:8080/player)

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
/playPdocast and /addPodcast - HTTP POST METHOD - accept 'feed_url' parameter
```

###Special (These might be dropped soon.)
```
/comehome - Checks if playback has STOPPED, if so it sends the command to play a stream and welcomes the user home.
/drwissen - Plays the radio station DRadio Wissen.
/recentArtists - Plays a random mix of recent artists.
```

##To Do List
- Podcast delete feature
- Room Profiles
- Code Clean-UP!!!
- Expand deployment options.
