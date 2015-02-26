<html>
    <head>
    <title>rf.wr.py</title>
 <style type="text/css">
 <!--A{text-decoration:none}-->

 div.main{
   float: left;
 }
 div.control{
   float: left;
   width: 148px;
   height: 100%;
   margin-right: 4px;
   margin-left: 2px;
 }
 div.controlElementURI{
 }
 img.controlElementIMG{
   height: auto;
   width: 148px;
 }
 div.controlElementVOL{
   height: 4px;
   width: 148px;
   position: relative;

 }
 div.controlElementVOL:hover{
   background-color:#b3b3b3;
 }
 div.controlElementVOLBAR{
     position: absolute;
     top: 700;
 }
 div.controlElementVOL_cont{
     position: absolute;
     top: 700;
   }
 div.controlElement{
   width: 148px;
   height: 148px;
   margin-top: 2px;
   margin-bottom: 4px;
 }
 div.controlElementMUTE{
   width: 148px;
   height: 40px;
   margin-top: 2px;
   margin-bottom: 4px;
 }
 div.controlElementMUTE:hover, div.controlElement:hover{
    background-color:#ffffff;
 }






            div.activation{
                    align: right;
                  }
            a.Active{
                       pointer-events: none;
                       cursor: default;
                       color: #D4C311;
                      }
            a.room_plus_Active{
                       pointer-events: none;
                       cursor: default;
                       color: #bdffea;
                    }

            div.zone_Activate{
                    background-color:#bdbbea;
                    width: 148px;
                    height: 148px;
                    }

            div.zone_Active{
                    background-color:#bdffea;
                    padding: 2px 2px 2px 2px;
                    border: 1px solid;
                    width: 142px;
                    height: 142px;
                    }

            div.unassigned{
                    background-color:#66FA7F;
                    width: 148px;
                    height: 148px;
                    }
 </style>
</head>
    <div class="control"><h1><a href="/zones" title="Refresh">&#10226;</a> </h1>
    %if tree[0].tag == 'zones':
            %i = 0
            %for zone in zone_room_names:
            <div class="controlElement" style="background-color: grey;">
                    <div class = "zone_{{active_zone_str_helper[i]}}">
                    Zone {{i}}: {{zone_room_names[i].keys()[0]}} <div align="right" class="activation"><a class="{{active_zone_str_helper[i]}}" href="/zone/{{i}}">{{active_zone_str_helper[i]}}</a></div>
                    %for room in zone[zone.keys()[0]]:
                        <div class = "room">
                            <a href="/drop_room/{{room}}">{{room}}</a><a class="room_plus_{{active_zone_str_helper[i]}}"  href="/add_room/{{room}}">[+]</a>

                            </div>
                    %end
                    </div>
                    %i = i + 1
            </div>
            %end
                   Active Zone: {{}}<br>
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
    <br><br>
    Usage:
    <ul>
    <li>Choose active zone by clicking on 'Activate'.</li>
    <li>Remove rooms from any zone by clicking on them or add [+] them to the active zone.</li>
    <li>Unassigned rooms can be added [+] to the active zone or used to create a new room, by clicking on the name.</li>
    </ul>
    <br><a href="/player">Back to Player</a>
    </div>
    </html>
