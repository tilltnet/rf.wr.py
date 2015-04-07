// Fix Grid
function fix_grid() {
  var grid_width = document.getElementById('grids').offsetWidth;
  var covers_per_row = Math.floor(grid_width / 150);
  console.log(covers_per_row);
  var perfect_grid_width = covers_per_row * 150 + covers_per_row;
  var perfect_cover_seekbar_margin = grid_width - perfect_grid_width - (covers_per_row - 3);
  //console.log(perfect_grid_width);

  document.getElementById('cover_seekbar').setAttribute("style", "margin-right:" + perfect_cover_seekbar_margin + "px");
}

// Click Cover
function click_cover(type , no) {
  xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "GET", '/' + type + '/' + no, true);
  xmlHttp.send( null );
  }


// Context Menu Trigger
var last_child_id = "";

function corner_click(child_id) {
    if (document.getElementById(child_id).style.display == 'block') {
      document.getElementById(child_id).style.display = 'none';
    } else {
      document.getElementById(child_id).style.display = 'block';
    }
    console.log(document.getElementById(child_id).style.display);
    if (last_child_id != "" & last_child_id != child_id) {
      document.getElementById(last_child_id).style.display = 'none';
    } else if (last_child_id == child_id) {
      console.log(document.getElementById(child_id).style.display);

      console.log(document.getElementById(child_id).style.display);
    }
    window.last_child_id = child_id;
}

// Fix Controls Height
function fix_controls_height() {
  iframe = document.getElementById('iframe_control');
  innerDoc = iframe.contentDocument || iframe.contentWindow.document;
  controlElement_count = innerDoc.getElementsByClassName("controlElement").length;
  perfect_height = (controlElement_count + 1) * 150 + 30;
  document.getElementById('iframe_control').setAttribute("height",perfect_height)
  //console.log(perfect_height + " : " + controlElement_count);
}

//Cover Seekbar
function show_hide_playlist() {
    if(window.show_playlist == 0) {
      document.getElementById("playlist_div").style.display = 'block';
      load_playlist(window.track_no);
      window.show_playlist = 1;
    } else {
      document.getElementById("playlist_div").style.display = 'none';
      window.show_playlist = 0;
      document.getElementById('playlist').src = '#';
    }
}
