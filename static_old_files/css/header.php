<!Doctype html>
<html lang="en" class="no-js">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">

<title>Clat Courses</title>

<link href="css/default.css" rel="stylesheet" type="text/css">
<link href="css/strap.css" rel="stylesheet" type="text/css">
<link href="css/fonts.css" rel="stylesheet" type="text/css">
<link href="css/animate.css" rel="stylesheet"  type="text/css">
<link href="css/styles.css" rel="stylesheet"  type="text/css">
<link href="css/login.css" rel="stylesheet"  type="text/css">

<script type="text/javascript" src="js/jquery.min.js"></script>
<script type="text/javascript">

$(document).ready(function() {  $(".sign-btn").click(function(){ $("#logpanel").show(); $("#register").show();$("#login").hide();    });});
$(document).ready(function() {  $(".logid").click(function(){ $("#logpanel").show(); $("#register").hide();$("#login").show();    });});
$(document).ready(function() {  $(".lo1").click(function(){  $("#login").show();$("#register").hide();    });});
$(document).ready(function() {  $(".re1").click(function(){  $("#login").hide();$("#register").show();    });});
$(document).ready(function() {  $(".close-button").click(function(){  $("#logpanel").hide();    });});
$(document).ready(function() {  $("#pu").click(function(){ $("#pop").show(); $("#popup").show();    });});
$(document).ready(function() {  $("#cbutton").click(function(){  $("#pop").hide();    });});
$(document).ready(function() {  $("#cbutton").click(function(){  $("#pop").hide();    });});


$(document).ready(function() {  $("#menu1").click(function(){  $("#drop").slideToggle();    });});




</script>
</head>

<body id="ex3">



<section id="logpanel">
  <div id="register">
    <div class="boss">
      <li class="re1 active">register</li>
      <li class="lo1">login</li>
      <div class="close-button" data-icon="z"></div>
    </div> 
    
    
   
     <div class="login-with facebook" style="margin-top:80px;"> <div class="s" data-icon=";"></div> Register with Facebook</div>
    <div class="login-with gmail"> <div class="s" data-icon="'"></div> Register with Google</div>
  
  
  <h3> OR</h3>
  <a href="register.php" style=" text-decoration:none" ><div class="boss">
        <input type="submit" style="padding:10px 30px !important; margin-left:40px !important" class="ssubmit" name="register" value="Create a new account"/>
      </div></a>
    <!--form action="< ?php echo htmlspecialchars($_SERVER['PHP_SELF'])?>" method="post" id="register_form">
      <div class="boss" style="top:-20px !important ;">
        <div class="text-name">Username</div>
        <input type="text" class="text-sbox" placeholder="Enter username" name="name" id="rname"/>
        <span id="runame" style="color:#F00; display:none; font-size:14px; font-family: Calibri; margin-left:20px;margin-top:5px"></span> </div>
      <div class="boss">
        <div class="text-name">Password</div>
        <input type="password" class="text-sbox" name="password" id="rpassword"/>
        <span style="color:#F00;font-size:13px;font-family: Calibri;  margin-left:20px;margin-top:5px" id="rpwd"></span> </div>
      <div class="boss">
        <div class="text-name">Mobile Number</div>
        <input type="text" class="text-sbox" placeholder="enter mobile number" name="mobile" id="phone"/>
      </div>

      <div class="boss">
        <input type="submit" class="ssubmit" name="register" value="Create a new account"/>
      </div>
    </form-->
  </div>
  
  
  <!--  Login Con   -->
  
  <div id="login">
    <div class="boss">
      <li class="re1" >register</li>
      <li class="lo1 active">login</li>
      <div class="close-button" data-icon="z"></div>
    </div>
        <div class="login-with facebook"> <div class="s" data-icon=";"></div> Login with Facebook</div>
    <div class="login-with gmail"> <div class="s" data-icon="'"></div> Login with Google</div>

  <h3> OR</h3>
    <form  method="post" id="login-ajax" >
      <div class="boss">
        <div class="text-name">Username</div>
        <input type="text" class="text-sbox" placeholder="Enter username"  name="name" id="sname"/>
        <span id="luname" style="color:#F00; display:none; font-size:14px; font-family: Calibri; margin-left:20px;margin-top:5px"></span> </div>
      <div class="boss">
        <div class="text-name">Password</div>
        <input type="password" class="text-sbox" name="pwd" id="spwd"/>
        <span style="color:#F00;font-size:14px;font-family: Calibri;  margin-left:20px;margin-top:5px" id="lpwd"></span> <span class="text-name" id="error" style="color:#F00; margin-top:5px "></span> </div>
      <div class="boss">
        <input type="submit" class="ssubmit"  name="login" id="login_form" value="Login"/>
      </div>
      <div class="boss">
        <div class="text-name">forgot password ?</div>
      </div>
    </form>
  </div>
</section>
<section id="container">
<header>
<div class="con" >
<div class="col-sm-3">
<a href="index.php" style=" text-decoration:none" ><div class="icon"><img src="images/logo.png" alt="edx"  width="105"></div></a>
</div><div id="menu1" data-icon="&#xe070;"></div>

<div id="drop">
<div class="cons1">
<div class="col-md-2" style="padding-top:15px !important;" >
<div class="search-bos">
<a href="allcourses.php" style=" text-decoration:none" ><div class="all-cou-img"><img src="images/icons/Activity-100.png" height="100%" width="100%"></div></a>
<input type="text" class="txt" placeholder="I want to learn about"  style="border:none !important"/>
<div class="search-icon" data-icon="&#xe073;"></div></div> 
</div></div>

<div class="col-sm-2">
<div class="sign-btn" id="regid">Sign In / Register </div>
</div>
 </div>


<div class="col-md-1 mm" style="margin-left:55px; margin-right:45px;" >
<div class="search-bos">
<a href="allcourses.php" style=" text-decoration:none" >
<div class="all-cou-img"><img src="images/icons/Activity-100.png" height="100%" width="100%"></div></a>
<input type="text" class="txt" placeholder="I want to learn about"  style="border:none !important"/>
<div class="search-icon" data-icon="&#xe073;"></div></div> 
</div>


<div class="col-sm-2 mm">
<div class="sign-btn" id="regid">Sign In / Register </div>
</div>

 </div>

</header>