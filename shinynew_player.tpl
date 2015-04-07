%from bottle import request
%from urlparse import urlparse
%import random
%import urllib
%##album_art = 'albumArtURI'
%##album_art = 'cached_art'
<!DOCTYPE html>
<html>
    <head>
        <title>rf.wr</title>
         <link rel="stylesheet" href="static/normalize.css">
         <link rel="stylesheet" href="static/rfwr.css">
         <link rel="stylesheet" href="/static/browse_search.css">
         <link rel="icon" href="/images/favico_play.png">
         <script src="/static/rfwr.js"></script>

         <style type="text/css">
          #cover_seekbar{float: right; width: 300px; height: 454px; margin-top: 2px;}

        </style>
    </head>

    %r = lambda: random.randint(100,155)
    %hex_rgb = '#%02X%02X%02X' % (int(r()),r(),r())

    <body bgcolor="{{hex_rgb}}" onload="fix_grid(); fix_controls_height();" onresize="fix_grid()">

      <div class="container">

      <!-- Controls -->
        <div class="control">
          <iframe id="iframe_control" src="/ctct" width="149px" height="950px" scrolling="no" frameborder="0" onload="fix_controls_height();"></iframe>
        </div>

      <!-- grids-->
        <div id="grids">
          <!-- Last Played -->
          <div class="main">
            <div style="background-color: grey; width: 30px; position: absolute; left: -30px">
              <p style="margin: 148px 0px 0px 10px; transform: rotate(270deg);
                transform-origin: left top 0; width: 140px;">
                  {{folder_name}}
                </p>
            </div>


            <div>
            <!-- Cover Seekbar -->
            <div id="cover_seekbar">
                 <iframe id="iframe_seekbar" src="/sbsb" width="300px" height="452px" scrolling="no" frameborder="0"></iframe>
            </div>


            <!-- Recently Played -->
              %i = 0
              %for child in children:
                    <div class = "cover" style="background-image: url({{child[album_art]}});">
                      <!-- Link -->
                        <a href="#" onclick="click_cover('play_id', '{{str(i) + '/' + child['id']}}'); return false;"><span></span></a>
                      <!-- Corner Click -->
                      %if child['class'] != 'object.container' and child['class'] != 'object.container.favoritesContainer':
                        <div class="cv_corner_button">
                              <a href="#"  onclick="corner_click('{{child['id']}}'); return false;"><img width="25" height="25" src="/images/browse_corner.png"></a>
                        </div>
                      %end
                      <!-- Cover Text -->
                      <div class="cover_text">
                          <a href="#" onclick="click_cover('play_id', '{{str(i) + '/' + child['id']}}'); return false;">{{child['title']}}</a>
                      </div>
                    </div>
                      <!-- Context Menu-->
                      <!-- musicTrack/ audioBroadcast.radio-->
                      %if child['class'] == 'object.item.audioItem.musicTrack' or child['class'] == 'object.item.audioItem.audioBroadcast.radio':
                        <div class="cv_context" id="{{child['id']}}">
                            <a href="#" onclick="click_cover('play_id', '{{str(i) + '/' + child['id']}}'); setTimeout(function() {corner_click('{{child['id']}}')}, 1000); return false;">
                              <img src="/images/browse_play.png" width="45">
                            </a>
                            <a href="#" onclick="click_cover('queue', '{{'track_next/' + child['id']}}'); setTimeout(function() {corner_click('{{child['id']}}')}, 1000); return false;">
                              <img src="/images/browse_play_next.png" width="45">
                            </a>
                            <a href="#" onclick="click_cover('queue', '{{'track_last/' + child['id']}}'); setTimeout(function() {corner_click('{{child['id']}}')}, 1000); return false;">
                              <img src="/images/browse_play_last.png" width="45">
                            </a>
                        </div>
                      <!-- non-Tracks-->
                      %else:
                        <div class="cv_context" id="{{child['id']}}">
                            <a href="#" onclick="click_cover('play_id', '{{str(i) + '/' + child['id']}}'); setTimeout(function() {corner_click('{{child['id']}}')}, 1000); return false;">
                              <img src="/images/browse_play.png" width="45">
                            </a>
                            <a target="media_tab" href="/media/{{child['id']}}">
                              <img src="/images/browse_browse.png" width="45">
                            </a>
                            <a href="#" onclick="click_cover('queue', '{{'next/' + child['id']}}'); setTimeout(function() {corner_click('{{child['id']}}')}, 1000); return false;">
                              <img src="/images/browse_play_next.png" width="45">
                            </a>
                            <a href="#" onclick="click_cover('queue', '{{'last/' + child['id']}}'); setTimeout(function() {corner_click('{{child['id']}}')}, 1000); return false;">
                              <img src="/images/browse_play_last.png" width="45">
                            </a>
                        </div>
                      %end
                    %i = i + 1

                  %end
                </div>
            </div>
          <!-- Favs/ Shortcuts-->
          <!-- label -->
          <div class="main">
            <div style="background-color: grey; width: 30px; position: absolute; left: -30px">
              <p style="margin: 148px 0px 0px 10px; transform: rotate(270deg);
              transform-origin: left top 0; width: 140px;">Shortcuts</p>
            </div>
            %for fav in range(0,len(cover_imgs)):
              <!--- Check if Image is hosted on rf.wr; if True: extract path from url -->
              %_, netloc, path, _, _ ,_ = urlparse(str(cover_imgs[fav]))
              %if netloc == request.get_header('host'):
                %cover_imgs[fav] = path
              %end
              <!-- Cover Image - Corner Button - Cover Text -->
                <div class = "cover" style="background-image: url({{cover_imgs[fav]}});">
                  <a href="#" onclick="click_cover('fav', {{fav+1}}); return false;" ><span></span></a>
                  <div class="corner_button" style=""><a href="/setfav/{{fav+1}}"><img width="20" height="20" src="/images/refresh.png"></a></div>
                  <div class="cover_text">
                    <a href="#" onclick="click_cover('fav', {{fav+1}}); return false;">{{titles[fav]}}</a>
                  </div>
                </div>
            %end
            <!-- Add Shortcuts -->
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

            <!-- Podcasts -->
            <!-- label -->
            <div class = "main">
              <div style="background-color: grey; width: 30px; position: absolute; left: -30px">
                <p style="margin: 148px 0px 0px 10px; transform: rotate(270deg);
                transform-origin: left top 0; width: 140px;">Podcasts</p>
              </div>
              <div style="background-color: grey; width: 30px; height: 100%; left: -30px; position: absolute; top: 148px; z-index: -1;">
                <div style="background-color: #132F90; width: 1px; height: 100%; left: 20px; position: absolute; z-index: -1;"></div>
              </div>

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
              <<!--<div style="height: 50px; position: relative; float: left; width : 100%;"></div>-->
            </div>
        </div>
      </div>
    <!-- Podbar -->
        <div class="podbar">
          <div style="position: relative;">
            <iframe id="iframe_volbar" src="/volbar" width="490px" scrolling="no" frameborder="0"></iframe>
          </div>
          <div style="position: absolute; float:right; right: 5px; top:5px; height: 35px">
            <div style="position: relative; float: left;">
              <form action="/playURI" method="post">
                <p style="color: white; float: left;  top: -15px; position: relative; right: 5px;">External Media</p>
                <div style="float: right; right: 5px;">
                  <input name="URI" type="text" size="15" placeholder="file or stream URL"/>
                  <input value="Play" type="submit" />
                </div>
              </form>
            </div>

            <div style="position: relative; float: left">
              <form action="/addPodcast" method="post" style="">
                <p style="color: white; float: left; top: -15px; position: relative; right: 5px; margin-left: 5px">Podcast</p>
                <div style="float: right; right: 5px;">
                  <input name="feed_url" type="text" size="15" placeholder = "RSS feed URL"/>
                  <input value="+" type="submit" />
                </div>
              </form>
            </div>
          </div>


    </div>
    <script type="text/javascript">
      fix_grid();
    </script>
  </body>
</html>
