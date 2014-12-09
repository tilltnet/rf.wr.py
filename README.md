rf.wr.py
========

raumfeld web remote in python

![Screenshot](/rfwr.png)

rf.wr.py is a small webserver that let's you control the playback of your raumfeld system through a browser. You can submit URIs of audio-streams and -files, favorites of currently playing content can be set (These favorites differ from the one in the official Raumfeld App!). You might want to run rf.wr.py on a small embedded linux machine as the raspberry pi or possibly your router.

rf.wr.py uses [raumfeld-python](https://github.com/tfeldmann/python-raumfeld) (with minor changes) and [bottle.py](http://bottlepy.org/docs/dev/index.html).

Install
-------
You need to have python2.7 at least and git needs to be installed.

The libraries bottly.py and raumfeld-python are required to run the server. If you installed raumfeld-python before unistall it with 'pip uninstall raumfeld'. Then run the following commands to install both libraries.

    pip install bottle
    pip install git+git://github.com/tilltnet/python-raumfeld
    
Now to download rf.wr.py: Change to your desired folder.

	cd /home/user/somewhere/
	
wget and bzip2 the files from github.

	wget https://github.com/tilltnet/rf.wr.py/archive/master.zip
	unzip master.zip

This creates the folder 'rf.wr.py-master'.

Manually downloading and unzipping the zip File via the github website will work just as well.

Execute
-------
Change to the folder you just created with 'cd rf.wr.py-master' and run:

    python2.7 rfwr.py & 
    
Or, if you want to start the server in the background and possible through ssh, use:
   
   nohup python2.7 rfwr.py &

"It's not working!" If you encounter dependency errors go back to pip installing the missing packages. The used libraries are not that exotic and should be already available on most systems.

"It works!" Then open the browser on any machine in your local network and point it to 

[http://your.machine:8080/player](http://your.machine:8080/player)

replacing your.machine with the IP or name address of your server. For me it is:

[http://musicbox.local:8080/player](http://musicbox.local:8080/player)

Commands
--------
This is a list of commands, that can be invoked.
		
	/player - This is the default address and most of the commands and functions can be accessed through it.
	/play
	/pause
	/next
	/previous
	/playURI - GET - let's you enter URI to stream
	/vol/<no> - Set volume with <no> ranging between 0 and 100 (everything above 90 might be critical!).

	/info - Shows current transport info as CurrentURI, CurrentURIMetaData, TrackURI, TrackMetaData.
	/zones - Let's you choose your music zone.
	/zone/<no> - Lets you set the zone to control.
	/addfav - Add a favorite.
	/setfav - Overwrite a previously set favorite.
	/fav/<no> - Play a favorite.
	
	/comehome - Checks if playback has STOPPED, if so it sends the command to play a stream and welcomes the user home.
	/drwissen - Plays the radio station DRadio Wissen.
	/recentArtists - Plays a random mix of recent artists.
