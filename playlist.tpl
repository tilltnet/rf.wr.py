<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="static/normalize.css">
    <link rel="stylesheet" href="static/stylish_ordered_list.css">



  <script type="text/javascript">
    function load() {
    	var urllocation = location.href;
    	if(urllocation.indexOf("#playing") > -1){
    		window.location.hash="anchor";
    	} else {
    	return false;
    	}
    }

    function click_item(type , no) {
      xmlHttp = new XMLHttpRequest();
      xmlHttp.open( "GET", '/' + type + '/' + no, true);
      xmlHttp.send( null );
      }
  </script>
  </head>

  <body onload='location.href="#playing"'>

    <ol class="betterList">
      %i = 1
      %for item in playlist_items:

      <li
      %if i == int(cur_track):
        id='playing'
      %end
      >
        <a href="#" onclick="click_item('track',{{i}}); return false;" ><span></span>

          <div style="break: none; position: relative; top: -8px; font-size: 11pt; overflow: hidden; white-space: nowrap;">{{item['title']}}</div>
          %if 'artist' in item:
            <p style="font-size: 10pt; position: absolute; top: 8pt;">{{item['artist']}}</p>
          %end
        </a>
      </li>
      %i = i + 1
      %end
    </ol>
    <script type="text/javascript">
      location.href="#playing"
    </script>
  </body>
</html>
