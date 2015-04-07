%import re
%renderer_ips = []
<!DOCTYPE html>
<html>
  <head>
    <title>rf.info</title>
     <link rel="stylesheet" href="static/normalize.css">
     <link rel="stylesheet" href="static/rfwr.css">
     <link rel="icon" href="/images/favico_info.png">
  </head>
  <body>
    <h1>Device Settings</h1>
    <a target = "" href = "http://{{host_ip}}:47365/settings">[Raumfeld Settings]</a><br>
    %if len(zones) > 0:
      % i = 0
      %for zone in zones:
        <div class="controlElement" style="background-color: grey; width: 300px;">
          <div class = "zone_{{active_zone_str_helper[i]}}" style = "width: 300px;">
            <div class="zone_title" style="width: 300px;">
          Zone {{i}}: {{zone.Name}}
            </div>
            <div class="zone_content" style="width: 300px;">
              %for room in zone.getRooms():
                <div class = "room">
                    -&nbsp;{{room.Name}}
                    %for renderer in room._renderers:
                        %ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', renderer._address)
                        <a target = "" href = "http://{{ip[0]}}:48365/">[Renderer Settings]</a>
                    %end
                </div>
              %end
            </div>
          </div>
          %i = i + 1
        </div>
      %end
    %end
    %if len(unassigned) > 0:
        <div class="controlElement" style="background-color: grey; width: 300px;">
          <div class = "unassigned" style="width: 300px;"> Unassigned:
          %for i in range(0, len(unassigned)):
              <div class = "room">{{unassigned[i].Name}}</div>
          %end
          </div>
      </div>
    %end


    <h1>Track Info</h1>
    %for key, entry in track_meta.iteritems():
      {{key + ': ' + entry}} <br>
    %end
    <br>
    <h1>Media Info</h1>
    %for key, entry in media_meta.iteritems():
      {{key + ': ' + entry}} <br>
    %end



        </body>
</html>
