<!DOCTYPE html>
  <html>
  <head>
  <link rel="stylesheet" href="static/normalize.css">

    <style type="text/css">

    input[type=range] {
        /*removes default webkit styles*/
        -webkit-appearance: none;

        /*fix for FF unable to apply focus style bug */
        border: 0px solid white;

        /*required for proper track sizing in FF*/
        width: 280px;
    }
    input[type=range]::-webkit-slider-runnable-track {
        width: 280px;
        height: 5px;
        background: #ddd;
        border: none;
        border-radius: 3px;
    }
    input[type=range]::-webkit-slider-thumb {
        -webkit-appearance: none;
        border: none;
        height: 16px;
        width: 16px;
        border-radius: 50%;
        background: goldenrod;
        margin-top: -4px;
    }
    input[type=range]:focus {
        outline: none;
    }
    input[type=range]:focus::-webkit-slider-runnable-track {
        background: #ccc;
    }

    input[type=range]::-moz-range-track {
        width: 280px;
        height: 5px;
        background: #ddd;
        border: none;
        border-radius: 3px;
    }
    input[type=range]::-moz-range-thumb {
        border: none;
        height: 16px;
        width: 16px;
        border-radius: 50%;
        background: goldenrod;
    }

    /*hide the outline behind the border*/
    input[type=range]:-moz-focusring{
        outline: 1px solid white;
        outline-offset: -1px;
    }

    input[type=range]::-ms-track {
        width: 280px;
        height: 5px;

        /*remove bg colour from the track, we'll use ms-fill-lower and ms-fill-upper instead */
        background: transparent;

        /*leave room for the larger thumb to overflow with a transparent border */
        border-color: transparent;
        border-width: 6px 0;

        /*remove default tick marks*/
        color: transparent;
    }
    input[type=range]::-ms-fill-lower {
        background: #777;
        border-radius: 10px;
    }
    input[type=range]::-ms-fill-upper {
        background: #ddd;
        border-radius: 10px;
    }
    input[type=range]::-ms-thumb {
        border: none;
        height: 16px;
        width: 16px;
        border-radius: 50%;
        background: goldenrod;
    }
    input[type=range]:focus::-ms-fill-lower {
        background: #888;
    }
    input[type=range]:focus::-ms-fill-upper {
        background: #ccc;
    }


    *{position: relative;
      font-family: sans-serif;
      color: white;}
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

          pos_hms = track_data[1].split(':')
          pos_s = parseInt(pos_hms[0]) * 3600 + parseInt(pos_hms[1]) * 60 + parseInt(pos_hms[2])

          dur_hms = track_data[2].split(':')
          dur_s = parseInt(dur_hms[0]) * 3600 + parseInt(dur_hms[1]) * 60 + parseInt(dur_hms[2])

          if(dur_s > 0 & sem == 0) {
            document.getElementById("progress_bar").value = pos_s;
            document.getElementById("progress_bar").max = dur_s;

          } else if (sem == 0) {
            document.getElementById("progress_bar").value = 0;
            document.getElementById("progress_bar").max = 0;

          }


            document.getElementById("title").innerHTML = track_data[3];
            document.getElementById("art").src = track_data[4];
            document.getElementById("artist").innerHTML = track_data[5];
            document.getElementById("album").innerHTML = track_data[6];
          

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

    </script>

  </head>
  <body>
  <div style="width: 300px; height: 300px;"><img id="art"></div>
  <div style="width: 300px; height: 150px; margin-top: 4px; background-color:rgba(55, 55, 55, 0.3);" align="center">

    <div>
      <p id="position" style="margin: 0px 0px 0px 0px; padding-left:2px; padding-top:2px;"></p>
      <p id="duration" style="margin: 0px 0px 0px 0px; padding-right:2px; padding-top:2px;"></p>
      <div align="center" stlye="float:left">
        <form id="seekbar" method="get" action="#" style="width: 280px;">
        <input type="range" id="progress_bar" name="seek_pos" min="0" onclick="release_progress_bar();" onmousedown="window.sem = 1;" onmouseup="window.sem = 0;" oninput="show_seek_time()" min="0">
      </form>
      <div align="center" style="position: relative;">
        <div id="artist"></div>
        <div id="title"></div>
        <div id="album"></div>
      </div>

      </div>

    </div>

  </div>
</body>
  </html>
