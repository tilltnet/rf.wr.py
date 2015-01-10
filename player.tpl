<!DOCTYPE html>
 <html>
 	<head>
 		<title>rf.wr.py</title>
 		<style
type="text/css">
 		<!--A{text-decoration:none}-->
 		div{
 			margin: 0px auto;
width: 642px;
 		}
     td.foot{font-size: 9pt;}
 		</style>
		                <script language=javascript>

                %for i in range(0,len(podcasts)):
                function submitPostLink_{{i}}()
                        {
                                document.postlink_{{i}}.submit();
                        }
                %end

                </script>
 		<link rel="icon" href="/images/play.png">
</head>
 	<body>
 	<div>
 		<table cellpadding="0" border="0" cellspacing="0"
bgcolor = "#c4f0fc">
 			<tr>
 				<td><a href="/previous"><img alt=""
src="images/playprevpausenext_0_0.png" style="width: 196px; height: 155px;
border-width: 0px"
 				  name="0_0"
 				  onmouseout="exchange(this,
'images_playprevpausenext', 0);"
 				  onmouseover="exchange(this,
'images_playprevpausenext', 1);"
 			/></a></td>

				<td><a href="/play"><img alt="" src="images/playprevpausenext_0_1.png"
				style="width: 124px; height: 155px; border-width: 0px"
   name="0_1"
				onmouseout="exchange(this, 'images_playprevpausenext', 0);"
				onmouseover="exchange(this, 'images_playprevpausenext', 1);"
 			/></a></td>

				<td><a href="/pause"><img alt="" src="images/playprevpausenext_0_2.png"
				style="width: 123px; height: 155px; border-width: 0px"
   name="0_2"
				onmouseout="exchange(this, 'images_playprevpausenext', 0);"
				onmouseover="exchange(this, 'images_playprevpausenext', 1);"
 			/></a></td>

				<td><a href="/next"><img alt="" src="images/playprevpausenext_0_3.png"
				style="width: 199px; height: 155px; border-width: 0px"
    name="0_3"
				onmouseout="exchange(this, 'images_playprevpausenext', 0);"
				onmouseover="exchange(this, 'images_playprevpausenext', 1);"
				/></a></td>
 </tr>
  		</table>
  		<table width = "642" bgcolor =
				"#c4f0fc">
  			<tr>
 <td align = "center">
  	<br>
  	<form
				action="/playURI" method="post">
 URI: <input name="URI" type="text" size="30" placeholder="address to file or stream"/>
				<input value="Play"
 type="submit" />
  	</form>
  	<br>

  </td>
  			</tr>
  		</table>

				<table width = "642" bgcolor = "#c4f0fc">
					<tr><td width="300"  valign="top">
					<b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Favorites</b>
  			<ul>
  			%for fav in fav_count:
  <li><a href="/fav/{{fav}}">{{titles[fav-1]}}</a> - <a href="/setfav/{{fav}}">Set</a></li>
  			%end
				<li><a href="/addfav">Add Favorite</a><br><br></li>

  			</ul>
  			</td>
				<td valign="top">
				<b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Podcasts</b>
				<ul>

                %for i in range(0,len(podcasts)):
                        <form action="/playPodcast" name="postlink_{{i}}" method="post"><input type="hidden" name="feed_url" value="{{podcasts[i][1]}}"></form>
                      <li>  <a href=# onclick="submitPostLink_{{i}}(); return false;">{{podcasts[i][0]}}</a></li>
                %end
								<form action="/addPodcast" method="post">
												<li>Add: <input name="feed_url" type="text" placeholder = "RSS feed address"/>
												<input value="+" type="submit" /></li>
								</form>
				</ul>
				</td>
				</tr>
				</table>
  		<table width = "642" bgcolor = "#c4f0fc">
  		<tr>
				<td><br><a
 href="/zones">Music Zone Manager</a></td>
  			<td align =
				"right"><br><a
 href="/info">Show Info</a></td></tr>
  		</table>
  		<table
				cellpadding="0"
 border="0" cellspacing="0">
  		  <tr>
  			<td><img alt=""
				src="images/vol_0_0.png" style="width: 63px; height: 98px; border-width:
				0px"
  		name="0_0"

		/></td>

			<td><a href="/vol/25"><img alt="" src="images/vol_0_1.png" style="width:
			41px; height: 98px; border-width: 0px"
 		name="0_1"
			onmouseout="exchange(this, 'images_vol', 0);"
   onmouseover="exchange(this,
			'images_vol', 1);"
 		/></a></td>

			<td><a href="/vol/30"><img alt="" src="images/vol_0_2.png" style="width:
			42px; height: 98px; border-width: 0px"
 		name="0_2"
			onmouseout="exchange(this, 'images_vol', 0);"
   onmouseover="exchange(this,
			'images_vol', 1);"
 		/></a></td>

			<td><a href="/vol/35"><img alt="" src="images/vol_0_3.png" style="width:
			42px; height: 98px; border-width: 0px"
 		name="0_3"
			onmouseout="exchange(this, 'images_vol', 0);"
   onmouseover="exchange(this,
			'images_vol', 1);"
 		/></a></td>

			<td><a href="/vol/40"><img alt="" src="images/vol_0_4.png" style="width:
			41px; height: 98px; border-width: 0px"
 		name="0_4"
			onmouseout="exchange(this, 'images_vol', 0);"
   onmouseover="exchange(this,
			'images_vol', 1);"
 		/></a></td>

			<td><a href="/vol/45"><img alt="" src="images/vol_0_5.png" style="width:
			42px; height: 98px; border-width: 0px"
 		name="0_5"
			onmouseout="exchange(this, 'images_vol', 0);"
   onmouseover="exchange(this,
			'images_vol', 1);"
 		/></a></td>

			<td><a href="/vol/50"><img alt="" src="images/vol_0_6.png" style="width:
			43px; height: 98px; border-width: 0px"
 		name="0_6"
			onmouseout="exchange(this, 'images_vol', 0);"
   onmouseover="exchange(this,
			'images_vol', 1);"
 		/></a></td>

			<td><a href="/vol/55"><img alt="" src="images/vol_0_7.png" style="width:
			44px; height: 98px; border-width: 0px"
 		name="0_7"
			onmouseout="exchange(this, 'images_vol', 0);"
   onmouseover="exchange(this,
			'images_vol', 1);"
 		/></a></td>

			<td><a href="/vol/60"><img alt="" src="images/vol_0_8.png" style="width:
			40px; height: 98px; border-width: 0px"
 		name="0_8"
			onmouseout="exchange(this, 'images_vol', 0);"
   onmouseover="exchange(this,
			'images_vol', 1);"
 		/></a></td>

			<td><a href="/vol/65"><img alt="" src="images/vol_0_9.png" style="width:
			42px; height: 98px; border-width: 0px"
 		name="0_9"
			onmouseout="exchange(this, 'images_vol', 0);"
   onmouseover="exchange(this,
			'images_vol', 1);"
 		/></a></td>

			<td><a href="/vol/70"><img alt="" src="images/vol_0_10.png" style="width:
			43px; height: 98px; border-width: 0px"
 		name="0_10"
			onmouseout="exchange(this, 'images_vol', 0);"
   onmouseover="exchange(this,
			'images_vol', 1);"
 		/></a></td>

			<td><a href="/vol/75"><img alt="" src="images/vol_0_11.png" style="width:
			41px; height: 98px; border-width: 0px"
 		name="0_11"
			onmouseout="exchange(this, 'images_vol', 0);"
   onmouseover="exchange(this,
			'images_vol', 1);"
 		/></a></td>

			<td><a href="/vol/80"><img alt="" src="images/vol_0_12.png" style="width:
			42px; height: 98px; border-width: 0px"
 		name="0_12"
			onmouseout="exchange(this, 'images_vol', 0);"
   onmouseover="exchange(this,
			'images_vol', 1);"
 		/></a></td>

			<td><a href="/vol/85"><img alt="" src="images/vol_0_13.png" style="width:
			42px; height: 98px; border-width: 0px"
 		name="0_13"
			onmouseout="exchange(this, 'images_vol', 0);"
   onmouseover="exchange(this,
			'images_vol', 1);"
 		/></a></td>

			<td><a href="/vol/90"><img alt="" src="images/vol_0_14.png" style="width:
			34px; height: 98px; border-width: 0px"
 		name="0_14"
			onmouseout="exchange(this, 'images_vol', 0);"
   onmouseover="exchange(this,
			'images_vol', 1);"
 		/></a></td>

		</tr>

		</table>
    <table width = "642" bgcolor = "#eeeeee">
    <tr>
      <td><br></td>
      <td class="foot" align = "right"><a href="https://github.com/tilltnet/rf.wr.py/blob/master/LICENSE">License / GPL</a> - <a href="https://github.com/tilltnet/rf.wr.py">github</a></td></tr>
    </table>
 </div>

<script language="javascript" type="text/javascript">
 /* Made with GIMP */

/* Preload images: */
     images_vol = new Array();

    images_vol["0_0_plain"] = new  Image();
 images_vol["0_0_plain"].src =
    "images/vol_0_0.png";
 images_vol["0_0_hover"] = new  Image();
    images_vol["0_0_hover"].src = "images/vol_0_0_hover.png";
    images_vol["0_1_plain"] = new  Image();
 images_vol["0_1_plain"].src =
    "images/vol_0_1.png";
 images_vol["0_1_hover"] = new  Image();
    images_vol["0_1_hover"].src = "images/vol_0_1_hover.png";
    images_vol["0_2_plain"] = new  Image();
 images_vol["0_2_plain"].src =
    "images/vol_0_2.png";
 images_vol["0_2_hover"] = new  Image();
    images_vol["0_2_hover"].src = "images/vol_0_2_hover.png";
    images_vol["0_3_plain"] = new  Image();
 images_vol["0_3_plain"].src =
    "images/vol_0_3.png";
 images_vol["0_3_hover"] = new  Image();
    images_vol["0_3_hover"].src = "images/vol_0_3_hover.png";
    images_vol["0_4_plain"] = new  Image();
 images_vol["0_4_plain"].src =
    "images/vol_0_4.png";
 images_vol["0_4_hover"] = new  Image();
    images_vol["0_4_hover"].src = "images/vol_0_4_hover.png";
    images_vol["0_5_plain"] = new  Image();
 images_vol["0_5_plain"].src =
    "images/vol_0_5.png";
 images_vol["0_5_hover"] = new  Image();
    images_vol["0_5_hover"].src = "images/vol_0_5_hover.png";
    images_vol["0_6_plain"] = new  Image();
 images_vol["0_6_plain"].src =
    "images/vol_0_6.png";
 images_vol["0_6_hover"] = new  Image();
    images_vol["0_6_hover"].src = "images/vol_0_6_hover.png";
    images_vol["0_7_plain"] = new  Image();
 images_vol["0_7_plain"].src =
    "images/vol_0_7.png";
 images_vol["0_7_hover"] = new  Image();
    images_vol["0_7_hover"].src = "images/vol_0_7_hover.png";
    images_vol["0_8_plain"] = new  Image();
 images_vol["0_8_plain"].src =
    "images/vol_0_8.png";
 images_vol["0_8_hover"] = new  Image();
    images_vol["0_8_hover"].src = "images/vol_0_8_hover.png";
    images_vol["0_9_plain"] = new  Image();
 images_vol["0_9_plain"].src =
    "images/vol_0_9.png";
 images_vol["0_9_hover"] = new  Image();
    images_vol["0_9_hover"].src = "images/vol_0_9_hover.png";
    images_vol["0_10_plain"] = new  Image();
 images_vol["0_10_plain"].src =
    "images/vol_0_10.png";
 images_vol["0_10_hover"] = new  Image();
    images_vol["0_10_hover"].src = "images/vol_0_10_hover.png";
    images_vol["0_11_plain"] = new  Image();
 images_vol["0_11_plain"].src =
    "images/vol_0_11.png";
 images_vol["0_11_hover"] = new  Image();
    images_vol["0_11_hover"].src = "images/vol_0_11_hover.png";
    images_vol["0_12_plain"] = new  Image();
 images_vol["0_12_plain"].src =
    "images/vol_0_12.png";
 images_vol["0_12_hover"] = new  Image();
    images_vol["0_12_hover"].src = "images/vol_0_12_hover.png";
    images_vol["0_13_plain"] = new  Image();
 images_vol["0_13_plain"].src =
    "images/vol_0_13.png";
 images_vol["0_13_hover"] = new  Image();
    images_vol["0_13_hover"].src = "images/vol_0_13_hover.png";
    images_vol["0_14_plain"] = new  Image();
 images_vol["0_14_plain"].src =
    "images/vol_0_14.png";
 images_vol["0_14_hover"] = new  Image();
    images_vol["0_14_hover"].src = "images/vol_0_14_hover.png";

	images_playprevpausenext = new Array();

    images_playprevpausenext["0_0_plain"] = new  Image();
    images_playprevpausenext["0_0_plain"].src =
    "images/playprevpausenext_0_0.png";
 images_playprevpausenext["0_0_hover"] =
    new  Image();
 images_playprevpausenext["0_0_hover"].src =
    "images/playprevpausenext_0_0_hover.png";
    images_playprevpausenext["0_1_plain"] = new  Image();
    images_playprevpausenext["0_1_plain"].src =
    "images/playprevpausenext_0_1.png";
 images_playprevpausenext["0_1_hover"] =
    new  Image();
 images_playprevpausenext["0_1_hover"].src =
    "images/playprevpausenext_0_1_hover.png";
    images_playprevpausenext["0_2_plain"] = new  Image();
    images_playprevpausenext["0_2_plain"].src =
    "images/playprevpausenext_0_2.png";
 images_playprevpausenext["0_2_hover"] =
    new  Image();
 images_playprevpausenext["0_2_hover"].src =
    "images/playprevpausenext_0_2_hover.png";
    images_playprevpausenext["0_3_plain"] = new  Image();
    images_playprevpausenext["0_3_plain"].src =
    "images/playprevpausenext_0_3.png";
 images_playprevpausenext["0_3_hover"] =
    new  Image();
 images_playprevpausenext["0_3_hover"].src =
    "images/playprevpausenext_0_3_hover.png";

function exchange (image, images_array_name, event)
   {
     name = image.name;
images = eval (images_array_name);

    switch (event)
   {
     case 0:
       image.src = images[name +
    "_plain"].src;
       break;
     case 1:
       image.src = images[name +
    "_hover"].src;
       break;
     case 2:
       image.src = images[name +
    "_clicked"].src;
       break;
     case 3:
       image.src = images[name +
    "_hover"].src;
       break;
   }

  }
 </script>
		</body>
 </html>
