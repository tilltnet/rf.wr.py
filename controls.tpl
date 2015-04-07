<!DOCTYPE html>
  <html>
        <head>
          <title>rf.wr.py</title>
           <link rel="stylesheet" href="static/normalize.css">
           <link rel="stylesheet" href="static/rfwr.css">
           <style type="text/css">
               #vol_slice_{{current_volume}}{
               /*background-color: rgba(255, 255, 255, 0.9);*/
               border-top: solid 2px;
               border-color: yellow;
               }
           </style>
        </head>
  <body>
      <!-- Controls -->

    <div class = "controlElement">
      <a href="/play_pause"><img class="controlElementIMG" src="images/{{play_button}}"/></a>
    </div>

    <div class = "controlElement_4">
      <div class= "controlElement_small">
        <a href="/previous"><img class="controlElementIMG_small" src="images/small_prev.png"/></a>
      </div>

      <div class= "controlElement_small" style="margin-right: 0px">
        <a href="/next"><img class="controlElementIMG_small" src="images/small_next.png"/></a>
      </div>

      <div class= "controlElement_small">
        <a href="/conf" target="_parent"><img class="controlElementIMG_small" src="images/small_conf.png"/></a>
      </div>

      <div class= "controlElement_small"  style="margin-right: 0px">
        <a href="/zones_on_off"><img class="controlElementIMG_small" src="images/small_zones.png"/></a>
      </div>
    </div>



  %if zones_on:
    %if len(zones) > 0:
            %i = 0
            %for zone in zones:
            <div class="controlElement" style="background-color: grey;">
                    <div class = "zone_{{active_zone_str_helper[i]}}">
                      <div class="zone_title">
                    Zone {{i}}: {{zone.Name}} <div align="right" class="activation"><a class="{{active_zone_str_helper[i]}}" href="/zone/{{zone.UDN}}">{{active_zone_str_helper[i]}}<span></span></a></div>
                      </div>
                      <div class="zone_content">
                    %for room in zone.getRooms():
                        <div class = "room">
                            <a href="/drop_room/{{room.Name}}">-&nbsp;{{room.Name}}</a><a class="room_plus_{{active_zone_str_helper[i]}}"  href="/add_room/{{room.Name}}">[+]</a>

                            </div>
                    %end
                      </div>
                    </div>
                    %i = i + 1
            </div>
            %end
    %end

    %if len(unassigned) > 0:
      <div class="controlElement" style="background-color: grey;">
          <div class = "unassigned"> Unassigned:
          %for i in range(0, len(unassigned)):
              <div class = "room"><a href="/new_zone/{{unassigned[i].Name}}">{{unassigned[i].Name}}</a><a href="/add_room/{{unassigned[i].Name}}">[+]</a></div>
          %end
          </div>
      </div>
    %end
  %end

<div class = "controlElement">
  <a target="media_tab" href="/media/0/My Music"><img class="controlElementIMG" src="images/shiny_mymusic.png"/></a>
</div>
<div class = "controlElement">
  <a target="media_tab" href="/media/0/WiMP"><img class="controlElementIMG" src="images/shiny_wimp.png"/></a>
</div>
<div class = "controlElement">
  <a target="media_tab" href="/media/0/RadioTime"><img class="controlElementIMG" src="images/shiny_tunein.png"/></a>
</div>
<div class = "controlElement">
  <a target="media_tab" href="/media/0/Line In"><img class="controlElementIMG" src="images/shiny_linein.png"/></a>
</div>
<div class = "controlElement">
  <a target="media_tab" href="/media/0/Favorites"><img class="controlElementIMG" src="images/shiny_favorites.png"/></a>
</div>
<!--<div class = "controlElement">
  <a target="media_tab" href="/media/0/My Music"><img class="controlElementIMG" src="images/shiny_podcasts.png"/></a>
</div>-->




  </body>
 </html>
