<!DOCTYPE html>
  <html>
  <head>
    <link rel="stylesheet" href="static/normalize.css">
    <link rel="stylesheet" href="static/stylish_ordered_list.css">
    <link rel="stylesheet" href="static/stylish_range_bar.css">
    <script src="/static/rfwr.js"></script>

    <style type="text/css">
    *{position: relative;
      font-family: "Century Gothic",Calibri,sans-serif;}
    #position{float: left; font-size: 9pt;}
    #duration{float: right; font-size: 9pt;}
    #artist{top: 2px;}
    #title{top: 2px; font-size: 14pt;}
    #album{top: 2px;}
    #art{width: 300px; height: auto;}
    </style>

    <script type="text/javascript">
      var host = location.host;
      var ws = new WebSocket("ws://" + host + "/seekbar/websocket");
      var sem = 0;
      var pos_calc_var = 0;
      var track_no = '0'
      var show_playlist = 0;

      function show_hide_playlist() {
          if(window.show_playlist == 0) {
            document.getElementById("playlist_div").style.display = 'block';
            load_playlist(window.track_no);
            window.show_playlist = 1;
          } else {
            document.getElementById("playlist_div").style.display = 'none';
            window.show_playlist = 0;
            document.getElementById('playlist').src = '#';
          }
      }

      function load_playlist(track_no) {
        var iframe = document.getElementById('playlist');
        iframe.src = '/playlist';
        setTimeout(function() {document.getElementById("playlist_div").scrollTop = (parseInt(track_no) - 1) * 46;}, 3500);
        setTimeout(function() {document.getElementById("playlist_div").scrollTop = (parseInt(track_no) - 1) * 46;}, 6500);
        }

      function new_ws() {
        var host = location.host;
        window.ws = new WebSocket("ws://" + host + "/seekbar/websocket");
      }
      ws.onopen = function() {
          console.log("Connection Opened");
          setInterval(function() {ws.send("Ping!");}, 36000)
          setInterval(function() {console.log("Ping!");}, 36000)
        }
      ws.onmessage = function (evt) {

          if (typeof pos_calc_var != 'undefined'){
            clearInterval(pos_calc_var);
          }

          console.log("The following data was received:" + evt.data);
          var track_data = evt.data.split('|||');

          if (sem == 0) {
            document.getElementById("position").innerHTML = track_data[1];
          }

          document.getElementById("duration").innerHTML = track_data[2];

          pos_hms = track_data[1].split(':');
          pos_s = parseInt(pos_hms[0]) * 3600 + parseInt(pos_hms[1]) * 60 + parseInt(pos_hms[2]);

          dur_hms = track_data[2].split(':');
          dur_s = parseInt(dur_hms[0]) * 3600 + parseInt(dur_hms[1]) * 60 + parseInt(dur_hms[2]);

          if(dur_s > 0 & sem == 0) {
            document.getElementById("progress_bar").value = pos_s;
            document.getElementById("progress_bar").max = dur_s;

          } else if (sem == 0) {
            document.getElementById("progress_bar").value = 0;
            document.getElementById("progress_bar").max = 0;

          }


            document.getElementById("title").innerHTML = track_data[4];
            document.getElementById("art").src = track_data[5];
            document.getElementById("artist").innerHTML = track_data[6];
            document.getElementById("album").innerHTML = track_data[7];



            window.track_no = track_data[3];
            if(window.show_playlist == 1) {
              window.load_playlist(track_data[3]);
            }


          function calc_pos() {
            if (track_data[0] == "p") {
              pos_s = pos_s + 1
            }

            if(dur_s > 0 & sem == 0){
              document.getElementById("progress_bar").value = pos_s;
            }

            if (dur_s >= pos_s & sem == 0) {
              document.getElementById("position").innerHTML = secs_to_hhmmss(pos_s);
            }
          }
          pos_calc_var = setInterval(calc_pos, 1000);
      }

      ws.onclose = function(){
        console.log("Connection Closed");
      }

      ws.onerror = function(evt){
        console.log("The following error occurred: " + evt.data);
      }

      function release_progress_bar() {
        no = document.getElementById("progress_bar").value
        xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", '/seek/' + no, true);
        xmlHttp.send( null );
      }

      function show_seek_time() {
        secs = document.getElementById("progress_bar").value;
        secs_to_hhmmss(secs);
        document.getElementById("position").innerHTML = hhmmss;
      }

      function secs_to_hhmmss(secs) {
        hh = parseInt( secs / 3600 ) % 24;
        mm = parseInt( secs / 60 ) % 60;
        ss = secs % 60;
        hhmmss = (hh < 10 ? "0" + hh : hh) + ":" + (mm < 10 ? "0" + mm : mm) + ":" + (ss  < 10 ? "0" + ss : ss);
        return hhmmss;
      }

      //Reszize Playlist iframe according to it's content (http://stackoverflow.com/questions/9975810/make-iframe-automatically-adjust-height-according-to-the-contents-without-using)
      function resizeIframe(obj) {
        obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
      }

    </script>

  </head>
  <body>
    <div style="width: 300px; height: 300px;"><img id="art">
    </div>
    <div style="width: 300px; height: 150px; margin-top: 4px; background-color:rgba(55, 55, 55, 0.3);" align="center">
      <div>
        <p id="position" style="margin: 0px 0px 0px 0px; padding-left:2px; padding-top:2px; color: white;"></p>
        <p id="duration" style="margin: 0px 0px 0px 0px; padding-right:2px; padding-top:2px; color: white;"></p>
        <div align="center" stlye="float:left">
          <form id="seekbar" method="get" action="#" style="width: 280px;">
            <input type="range" id="progress_bar" name="seek_pos" min="0" onclick="release_progress_bar();" onmousedown="window.sem = 1;" onmouseup="window.sem = 0;" oninput="show_seek_time()" min="0">
          </form>
          <div style="position: absolute; left: 135px; top: 115px;">
            <a href="#" onclick="show_hide_playlist(); return false;"><img src="/images/icon_playlist.png" width="30px"></a>
          </div>
          <div align="center" style="position: relative; color: white; height: 70px; overflow: hidden; top: -5px;">
            <div id="artist"></div>
            <div id="title"></div>
            <div id="album"></div>
          </div>

        </div>
      </div>
    </div>

    <!-- Playlist overlay -->
    <div id="playlist_div" style="top: 0px; width:300px; height: 415px; position: absolute; background-color: rgba(218, 165, 32, 0.96); overflow-y:scroll; overflow-x:hidden; display: none;">
      <iframe id="playlist" width="300px" height="454px" width="300px" height="454px" scrolling="no" frameborder="0"
          onload="javascript:resizeIframe(this);"></iframe>
    </div>
  <script type="text/javascript">

  </script>
  </body>
</html>
