<html>
  <head>
  <title>rf.volbar</title>
  <link rel="stylesheet" href="static/stylish_range_bar.css">

  <script type="text/javascript">
  function set_room_volume() {
    document.getElementById('volbar').value = document.getElementById('room_select').value;
  }

  function send_room_volume() {
    no = document.getElementById('volbar').value;
    room_sel = document.getElementById('room_select').selectedIndex;
    room_urls = ['/vol'
        %for i in range(1,len(room_volumes)):
          ,'/vol_room/{{room_volumes[len(room_volumes)-i-1][0]}}'
        %end
        ]
    console.log(room_urls[room_sel]);
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", room_urls[room_sel] + '/' + no, true);
    xmlHttp.send( null );
    setTimeout(function() { location.reload(); }, 3000);
  }
  </script>
  </head>

  <body onload="set_room_volume();" style="top: -12px; position: relative;">
     <select style="position: relative; color: #000000; font-size: 12pt; font-family: 'Century Gothic',Calibri,sans-serif;" id="room_select" name="room_select" onchange="set_room_volume();">
       %for i in range(0,len(room_volumes)):
          <option value="{{room_volumes[len(room_volumes)-i-1][1]}}">{{room_volumes[len(room_volumes)-i-1][0]}}</option>
       %end
     </select>
     <img src="/images/vol_unmute.png" width="30px" style="position: relative; top: 7px">
      <input type="range" id="volbar" onchange="send_room_volume();">

  </body>
</html>
