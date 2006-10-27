<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta name="Keywords" content="Asterisk, VoIP, destar, python"/>
	<title>DeStar :: Management Interface for the Asterisk PBX</title>
	<link rel="stylesheet" type="text/css" href="layout.css"/>
</head>

<?php
if (isset($HTTP_GET_VARS["c"])) $c=$HTTP_GET_VARS["c"];
else $c=0;

switch ($c) {
        case 0:
                $content="home.php";
                break;
        case 1:
                $content="screenshots.php";
                break;
        case 2:
                $content="download.php";
                break;
        case 3:
                $content="documentation.php";
                break;
        case 4:
                $content="resources.php";
                break;
        case 5:
                $content="about.php";
                break;
/*        case 6:
               $content="demo.php";
                break;
*/
}
?>

<body>
<h1 id="nameheader"><a href="http://destar.berlios.de" class="header">De<em>Star</em></a></h1>
<h3 id="subheader">Management Interface for the Asterisk PBX.</h3>
<br/><br/>
<div id="navigation" class="nav">
<ul>
<li><a href="index.php">Home</a></li>
<li><a href="manual/images/">Screenshots</a></li>
<li><a href="index.php?c=2">Download</a></li>
<li><a href="index.php?c=3">Documentation</a></li>
<li><a href="index.php?c=4">Resources & Support</a></li>
<li><a href="index.php?c=5">About</a></li>
<li><a href="manual/">User Manual</a></li>
<!--<li><a href="index.php?c=6">Demo</a></li>-->
</ul>
<a href="http://developer.berlios.de/projects/destar/">
<img src="http://developer.berlios.de/bslogo.php?group_id=2112" width="124" height="32" border="0" alt="BerliOS Logo" /></a>
<br/>
<a href="https://developer.berlios.de/project/make_donation.php?group_id=2112"><img src="http://developer.berlios.de/images/x-click-but7.gif" align="top" border="0" width="72" height="29" alt="[Donate to DeStar]"></a>

</div>

<div id="content">

<?php include $content; ?>

</div>

</body>
</html>
