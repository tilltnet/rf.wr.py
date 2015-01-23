<html>
    <head>
    <title>rf.wr.py</title>
 <style type="text/css">
 <!--A{text-decoration:none}-->
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
 div{
   margin: 0px auto; width: 250px;
                    }
 div.zone_Activate{
                    background-color:#bdbbea;
                    padding: 15px 15px 15px 15px;
                    }

            div.zone_Active{
                    background-color:#bdffea;
                    padding: 15px 15px 15px 15px;
                    border: 1px solid;
                    }
            div.unassigned{
                    background-color:#66FA7F;
                    padding: 15px 15px 15px 15px;
                    }
 </style>
</head>
    <div><h1>Zone Manager <a href="/zones" title="Refresh">&#10226;</a> </h1>
    %if tree[0].tag == 'zones':
            %i = 0
            %for zone in zone_room_names:
                    <div class = "zone_{{active_zone[i]}}">
                    Zone {{i}}: {{zone_room_names[i].keys()[0]}} <div align="right" class="activation"><a class="{{active_zone[i]}}" href="/zone/{{i}}">{{active_zone[i]}}</a></div>
                    %for room in zone[zone.keys()[0]]:
                        <div class = "room">
                            <a href="/drop_room/{{room}}">- {{room}}</a><a class="room_plus_{{active_zone[i]}}"  href="/add_room/{{room}}">[+]</a>

                            </div>
                    %end
                    </div>
                    %i = i + 1
            %end
                   Active Zone: {{l_zone}}<br>
            %if len(tree) > 1:
                <div class = "unassigned"> Unassigned:
                %for i in range(0, len(tree[1])):
                    <div class = "room"><a href="/new_zone/{{tree[1][i].attrib['name']}}">{{tree[1][i].attrib['name']}}</a><a href="/add_room/{{tree[1][i].attrib['name']}}">[+]</a></div>
                %end
                </div>
            %end
    %else:
                <div class = "unassigned"> Unassigned:
                %for i in range(0, len(tree[0])):
                    <div class = "room"><a href="/new_zone/{{tree[0][i].attrib['name']}}">{{tree[0][i].attrib['name']}}</a><a href="/add_room/{{tree[0][i].attrib['name']}}">[+]</a></div>
                %end
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
