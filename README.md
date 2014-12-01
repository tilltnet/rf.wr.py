rf.wr.py
========

raumfeld web remote in python

![Screenshot](/rfwr.jpg)

rf.wr.py is a small webserver that let's you control the playback of your raumfeld system through a browser. You can also submit URIs of audio-streams. You might want to run it on a small embedded linux machine as the raspberry pi or possibly your router.

rf.wr.py uses [raumfeld-python](https://github.com/tfeldmann/python-raumfeld) (with minor changes) and [bottle.py](http://bottlepy.org/docs/dev/index.html).

Install
-------
You need to have python2.7 at least and git needs to be installed.

The libraries bottly.py and raumfeld-python are required to run the server. If you installed raumfeld-python before unistall it with 'pip uninstall raumfeld'.

    pip install bottle
    pip install git+git://github.com/tilltnet/python-raumfeld
    
Execute
-------
Copy the rf.wr.py and the images folder to any folder on your computer and run it with:
    
    python2.7 rfwr.py &

Then open the browser on any machine in your local network and point it to 

[http://your.machine:8080/player](http://your.machine:8080/player)

replacing your.machine with the IP or name address of your server. For me it is:

[http://musicbox.local:8080/player](http://musicbox.local:8080/player)

Commands
--------
This is a list of commands, that can be invoked. Most of the commands can be accessed through /player.
		
	/play
	/pause
	/next
	/previous
	/comehome - checks if playback has STOPPED, if so it sends the command to play a stream and welcomes the user home
	/playURI - GET - let's you enter URI to stream
	/drwissen - plays the radio station DRadio Wissen
	/recentArtists - plays a random mix of recent artists 
