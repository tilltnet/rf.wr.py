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
  <body>
      <!-- Controls -->

    <div class = "controlElement">
      <a href="/play_pause"><img class="controlElementIMG" src="images/{{play_button}}"/></a>
    </div>
    <div class = "controlElement">
      <a href="/next"><img class="controlElementIMG" src="images/skip_shiny.png"/></a>
    </div>
    <div class = "controlElement">
      <a href="/zones_on_off"><img class="controlElementIMG" src="images/zones_shiny.png"/></a>
    </div>


  %if zones_on:
    %if tree[0].tag == 'zones':
            %i = 0
            %for zone in zone_room_names:
            <div class="controlElement" style="background-color: grey;">
                    <div class = "zone_{{active_zone_str_helper[i]}}">
                      <div class="zone_title">
                    Zone {{i}}: {{zone_room_names[i].keys()[0]}} <div align="right" class="activation"><a class="{{active_zone_str_helper[i]}}" href="/zone/{{i}}">{{active_zone_str_helper[i]}}<span></span></a></div>
                      </div>
                      <div class="zone_content">
                    %for room in zone[zone.keys()[0]]:
                        <div class = "room">
                            <a href="/drop_room/{{room}}">-&nbsp;{{room}}</a><a class="room_plus_{{active_zone_str_helper[i]}}"  href="/add_room/{{room}}">[+]</a>

                            </div>
                    %end
                      </div>
                    </div>
                    %i = i + 1
            </div>
            %end

            %if len(tree) > 1:
              <div class="controlElement" style="background-color: grey;">
                  <div class = "unassigned"> Unassigned:
                  %for i in range(0, len(tree[1])):
                      <div class = "room"><a href="/new_zone/{{tree[1][i].attrib['name']}}">{{tree[1][i].attrib['name']}}</a><a href="/add_room/{{tree[1][i].attrib['name']}}">[+]</a></div>
                  %end
                  </div>
              </div>
            %end
            %else:
              <div class="controlElement" style="background-color: grey;">
                  <div class = "unassigned"> Unassigned:
                  %for i in range(0, len(tree[0])):
                      <div class = "room"><a href="/new_zone/{{tree[0][i].attrib['name']}}">{{tree[0][i].attrib['name']}}</a><a href="/add_room/{{tree[0][i].attrib['name']}}">[+]</a></div>
                  %end
                  </div>
              </div>
            %end
          %end



    <div class = "controlElement">
      <a href="/info"><img class="controlElementIMG" src="images/info_shiny.png"/></a>
    </div>

    <div class="controlElementVOL_cont">

    %for i in range(10,74):
    <div id="vol_slice_{{100-i}}" class="controlElementVOL" style="background-color: rgba(0, 0, {{i}}, 0.{{84-i}});"></div>
    %end

    </div>
    <div class="controlElementVOLBAR"><img class="controlElementIMG" src="images/volbar_shiny.png"></div>
    <div class="controlElementVOL_cont">

    %for i in range(10,74):
    <div class="controlElementVOL"><a href="/vol/{{100-i}}"><span></span></a></div>
    %end

    </div>
    <div class="controlElementMUTE" style = "position: relative; top: 260px;">
      <a href="/mute"><img class="controlElementIMG" src="images/mute_shiny.png"/></a>
    </div>
  </div>
  </body>
 </html>
