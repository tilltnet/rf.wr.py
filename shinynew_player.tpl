%from bottle import request
%from urlparse import urlparse
%import random
%import urllib
<!DOCTYPE html>
<html>
    <head>
        <title>rf.wr.py</title>
         <link rel="stylesheet" href="static/normalize.css">
         <link rel="stylesheet" href="static/rfwr.css">

         <style type="text/css">
          #cover_seekbar{float: right; width: 300px; height: 454px; margin-top: 2px;}

        </style>

        <script language="javascript">
            function click_cover(type , no) {
              xmlHttp = new XMLHttpRequest();
              xmlHttp.open( "GET", '/' + type + '/' + no, true);
              xmlHttp.send( null );
              }
            function fix_grid() {
              var grid_width = document.getElementById('grids').offsetWidth;
              var covers_per_row = Math.floor(grid_width/150);
              console.log(covers_per_row);
              var perfect_grid_width = covers_per_row * 150 + covers_per_row;
              var perfect_cover_seekbar_margin = grid_width - perfect_grid_width - (covers_per_row - 3);
              console.log(perfect_grid_width);

              document.getElementById('cover_seekbar').setAttribute("style", "margin-right:" + perfect_cover_seekbar_margin + "px");
            }
            function fix_controls_height() {
              iframe = document.getElementById('iframe_control');
              innerDoc = iframe.contentDocument || iframe.contentWindow.document;
              controlElement_count = innerDoc.getElementsByClassName("controlElement").length;
              perfect_height = (controlElement_count + 2) * 150 + 15;
              document.getElementById('iframe_control').setAttribute("height",perfect_height)
              console.log(perfect_height + " : " + controlElement_count);
            }
        </script>

        <link rel="icon" href="/images/play.png">




    </head>
    %r = lambda: random.randint(100,155)
    %hex_rgb = '#%02X%02X%02X' % (int(r()),r(),r())
    <body bgcolor="{{hex_rgb}}" onload="fix_grid(); fix_controls_height();" onresize="fix_grid()">
      <div class="container">

      <!-- Controls -->

        <div class="control">
          <iframe id="iframe_control" src="/ctct" width="149px" height="950px" scrolling="no" frameborder="0" onload="fix_controls_height();"></iframe>
        </div>

        <div id="grids">


    <div class="main">

        <!-- Cover Seekbar -->
        <div id="cover_seekbar">
             <iframe id="iframe_seekbar" src="/sbsb" width="300px" height="452px" scrolling="no" frameborder="0"></iframe>
        </div>

      <!-- Cover Grid -->


            %for fav in range(0,len(cover_imgs)):
              <!--- Check if Image is hosted on rf.wr; if True: extract path from url -->
              %_, netloc, path, _, _ ,_ = urlparse(str(cover_imgs[fav]))
              %if netloc == request.get_header('host'):
                %cover_imgs[fav] = path
              %end

                <div class = "cover" style="background-image: url({{cover_imgs[fav]}});">

                  <!-- Link -->
                  <a href="#" onclick="click_cover('fav', {{fav+1}}); return false;" ><span></span></a>
                  <div class="corner_button" style="position:relative; height: 20px; width: 20px; left: 128px; padding: 0px 0px 0px 0px; z-index: 2;"><a href="/setfav/{{fav+1}}"><img width="20" height="20" src="/images/refresh.png"></a></div>

                  <div class="cover_text">

                        <!-- Link -->
                    <a href="#" onclick="click_cover('fav', {{fav+1}}); return false;">{{titles[fav]}}</a>
                  </div>
                </div>
            %end
            <div class = "cover" style="background-color: rgba(0,0,0,0.0);">

              <div style="background-image: url(); background-color: rgba(0,0,0,0.0); background-size: 148px 74px; height: 74px; width: 148px">
                <a href="/addfav/track"><img class="addFav" src="/images/add_fav_track.png" style="height: 74px; width: 148px"></a>
              </div>

              <div style="background-color: rgba(0,0,0,0.0); background-size: 148px 74px; height: 74px; width: 148px">
                  <a href="/addfav"><img class="addFav" src="/images/add_fav_list.png" style="height: 74px; width: 148px"></a>

              </div>

              <div class="cover_text">
                <a href="/addfav"></a></div>
            </div>
</div>



<div class = "main">
          %for i in range(0,len(podcasts)):
          <div class = "cover" style="background-image: url({{urllib.quote(podcasts[i][3], '/')}}); background-size: 148px 148px; height: 148px; width: 148px">
              <!-- Link -->
              <div class="corner_button" style="position:relative; height: 20px; width: 20px; left: 128px; padding: 0px 0px 0px 0px; z-index: 2;"><a href="/delPodcast/{{i+1}}"><img width="20" height="20" src="/images/delete.png"></a></div>
            <a href="#" onclick="click_cover('playPodcast', {{i+1}}); return false;"><span></span></a>

            <div class="cover_text">

              <!-- Link -->
            <a href=# onclick="click_cover('playPodcast', {{i+1}}); return false;">{{podcasts[i][0]}}</a>
              </div>
            </div>
          %end

      </div>
      </div>

<div class="podbar">
    <div style="float:left; margin-left: 20%; margin-right: 20%">

      <form action="/playURI" method="post" style="margin-top: 4px;">
      External Media <input name="URI" type="text" size="15" placeholder="file or stream URL"/><input value="Play" type="submit" />
    </form></div>
<div><form action="/addPodcast" method="post" style="margin-top: 4px;">
  Podcast <input name="feed_url" type="text" size="15" placeholder = "RSS feed URL"/>
  <input value="+" type="submit" />
</form>
</div>
</div>

    </body>
</html>
