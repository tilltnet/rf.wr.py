%from bottle import request
%from urlparse import urlparse
%import random
%import urllib

%##album_art = 'albumArtURI'
%##album_art = 'cached_art'
<!DOCTYPE html>
<html>
    <head>
        <title>rf.media</title>
         <link rel="stylesheet" href="/static/normalize.css">
         <link rel="stylesheet" href="/static/rfwr.css">
         <link rel="stylesheet" href="/static/browse_search.css">

         <link rel="icon" href="/images/favico_media.png">
         <script src="/static/rfwr.js"></script>
         <script language="javascript">
            var last_child_id = "";

         </script>
    </head>
    %r = lambda: random.randint(100,155)
    %hex_rgb = '#%02X%02X%02X' % (int(r()),r(),r())
    <body bgcolor="{{hex_rgb}}">
      <div class="container">

        <!-- Controls -->
        <div class="control">
          <iframe id="iframe_control" src="/ctct" width="149px" height="950px" scrolling="no" frameborder="0" onload="fix_controls_height();"></iframe>
        </div>
        <div id="grids">


          <div class="main">

            <!-- vertical meta['title']; grey colum; blue line-->
            <div style="background-color: grey; width: 30px; position: absolute; left: -30px">
              <p style="margin: 148px 0px 0px 10px; transform: rotate(270deg);
              transform-origin: left top 0; width: 140px;">{{meta['section']}}</p>
            </div>
            <div style="background-color: grey; width: 30px; height: 100%; left: -30px; position: absolute; top: 148px; z-index: -1;">
              <div style="background-color: #132F90; width: 1px; height: 100%; left: 20px; position: absolute; z-index: -1;"></div>
            </div>

            <!-- Title & Search Bar-->
            <div class = "cover" style="background-image: url(/images/shiny_tile_half.png); background-color: rgba(0,0,0,0.0); width: 300px;">
              <!-- Folder Up; Title; Play Folder-->
              <div style="width: 280px; top: 5px; left: 15px; position: absolute; z-index: 1;">

                    %if len(id.split('/')) > 2:
                      <p style="float: left;"><a href="/media/{{folder_up_id}}" ><img width="40" height="40" src="/images/browse_folder_up.png"></a></p>
                    %end

                    %if meta['class'] == 'object.container.trackContainer' or meta['class'] == 'object.container.album.musicAlbum' or meta['class'] == 'object.container.trackContainer.wimp' or meta['class'] == 'object.container.person.musicArtist'   or meta['class'] == 'object.container.playlistContainer':
                      <p style="float: left; margin-left: 5px"><a href="#" onclick="click_cover('play_id', '0/{{meta['id']}}'); return false;"><img width="40" height="40" src="/images/browse_play_folder.png"></a></p>
                    %end
                    <div style="float: left; margin-left: 15px; margin-top: 10px;">
                      <div style="width: 170px; font-size: 14pt;">{{meta['title']}}</div>
                      %id_split = meta['id'].split('/')
                      %parent_id_split = id_split[0:len(id_split)-1]
                      %if meta['title'] != 'Search' and parent_id_split[len(parent_id_split)-1] != 'Search':
                        %search_link = '/'.join([id_split[0], id_split[1], 'Search'])

                        <div style="width: 170px; font-size: 10pt;"><a href="/media/{{search_link}}">Search {{meta['section']}}</a></div>
                      %end
                    </div>
              </div>

              <!-- Search -->
              %if parent_id_split[len(parent_id_split)-1] == 'Search' or (meta['title'] == 'Search' and meta['section'] == 'RadioTime'):
              <div class="search_form" style="top: 90px; left: 45px; position: relative;">
                <form action="/search/{{id}}" method="post" style="margin-top: 4px;">
                 <input name="search_criteria" type="text" size="28" placeholder = "Search..."/>
                 <input value="Go!" type="submit" />
                </form>
              </div>
              %end
            </div>

            <!-- listview -->
            %i = 1
            %if meta['class'] == 'object.container.trackContainer' or meta['class'] == 'object.container.album.musicAlbum' or meta['class'] == 'object.container.trackContainer.wimp'  or meta['class'] == 'object.container.playlistContainer':
              <div class = "cover" style="background-image: url({{meta[album_art]}});"></div>
              <div style="position: relative; width: 453px;">
                <ol style="display: inline-block; width: 453px;">
                  %for child in children:
                      <li>
                        %if meta['class'] != 'object.container.album.musicAlbum':
                          <p class="lv_art">
                            <img src="{{child[album_art]}}" width="50px">
                          </p>
                        %end
                        <div class="lv_div">
                          <p class="lv_title">
                            {{child['title']}}</p>
                          <p class="lv_artist">
                            {{child['artist']}} - {{child['duration']}}</p>
                        </div>
                        <p class="lv_context">
                          %if child['class'] == 'object.item.audioItem.musicTrack' or child['class'] == 'object.item.audioItem.audioBroadcast.radio':
                                <a href="#" onclick="click_cover('play_id', '{{str(i) + '/' + child['id']}}'); return false;">
                                  <img src="/images/browse_play.png" width="45">
                                </a>
                                <a href="#" onclick="click_cover('queue', '{{'track_next/' + child['id']}}');return false;">
                                  <img src="/images/browse_play_next.png" width="45">
                                </a>
                                <a href="#" onclick="click_cover('queue', '{{'track_last/' + child['id']}}');return false;">
                                  <img src="/images/browse_play_last.png" width="45">
                                </a>

                          <!-- non-Tracks-->
                          %else:
                                <a href="#" onclick="click_cover('play_id', '{{str(i) + '/' + child['id']}}'); return false;">
                                  <img src="/images/browse_play.png" width="45">
                                </a>
                                <a href="/media/{{child['id']}}">
                                  <img  src="/images/browse_browse.png" width="45">
                                </a>
                                <a href="#" onclick="click_cover('queue', '{{'next/' + child['id']}}'); return false;">
                                  <img src="/images/browse_play_next.png" width="45">
                                </a>
                                <a href="#" onclick="click_cover('queue', '{{'last/' + child['id']}}'); return false;">
                                  <img src="/images/browse_play_last.png" width="45">
                                </a>
                          %end
                        </p>
                      </li>
                    %i = i + 1
                  %end
                </ol>
              </div>
            %else:


              <!-- Children Start-->
              %i = 0
              %for child in children:
                <div class = "cover" style="background-image: url({{child[album_art]}});">

                  <!-- Link -->
                  %if child['class'] != 'object.item.audioItem.musicTrack' and child['class'] != 'object.item.audioItem.audioBroadcast.radio':
                    <a href="/media/{{child['id']}}"  ><span></span></a>
                  %else:
                    <a href="#" onclick="corner_click('{{child['id']}}'); return false;"><span></span></a>
                  %end

                  <!-- Corner Click -->
                  %if child['class'] != 'object.container' and child['class'] != 'object.container.favoritesContainer':
                    <div class="cv_corner_button">
                          <a href="#"  onclick="corner_click('{{child['id']}}'); return false;"><img width="25" height="25" src="/images/browse_corner.png"></a>
                    </div>
                  %end

                  <!-- Cover Text -->
                  <div class="cover_text">
                    %if child['class'] != 'object.item.audioItem.musicTrack' and child['class'] != 'object.item.audioItem.audioBroadcast.radio':
                      <a href="/media/{{child['id']}}"  >{{child['title']}}</a>
                    %else:
                      <a href="#" onclick="corner_click('{{child['id']}}'); return false;">{{child['title']}}</a>
                    %end
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
                        <a href="/media/{{child['id']}}">
                          <img  src="/images/browse_browse.png" width="45">
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
          %end
        </div>
      </div>

    </body>
</html>
