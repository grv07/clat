<?php include('after-header.php');?>

<script type="text/javascript">

$(document).ready(function() {  $("#filter0").click(function(){ $("#fi0").slideToggle(); $("#fi1").hide();$("#fi2").hide(); $("#fi3").hide();$("#fi4").hide();
  });});
$(document).ready(function() {  $("#filter1").click(function(){ $("#fi1").slideToggle(); $("#fi0").hide();$("#fi2").hide(); $("#fi3").hide();$("#fi4").hide();
   });});
 $(document).ready(function() {  $("#filter2").click(function(){ $("#fi2").slideToggle(); $("#fi1").hide();$("#fi0").hide(); $("#fi3").hide();$("#fi4").hide();
  });});
 $(document).ready(function() {  $("#filter3").click(function(){ $("#fi3").slideToggle(); $("#fi1").hide();$("#fi2").hide(); $("#fi0").hide();$("#fi4").hide();
   });});
 $(document).ready(function() {  $("#filter4").click(function(){ $("#fi4").slideToggle(); $("#fi1").hide();$("#fi2").hide(); $("#fi3").hide();$("#fi0").hide();
   });});
</script>

<script type="text/javascript">


var make_button_active = function()
{
  //Get item siblings
  var siblings =($(this).siblings());

  //Remove active class on all buttons
  siblings.each(function (index)
    {
      $(this).removeClass('active');
    }
  )


  //Add the clicked button class
  $(this).addClass('active');
}

//Attach events to menu
$(document).ready(
  function()
  {
    $(".filters li").click(make_button_active);
  }  
)

</script>


<section id="privacy">
<div class="con"  id="pro">


<div class="col-lg-1 right" >


<div class="col-lg-4" id="course">
<iframe width="100%" height="500" src="player/story.html" frameborder="0" allowfullscreen></iframe>


</div></div>

<!--div class="filter-con" -->
<div class="col-sm-3 right" >

<ul class="filters">
<li class="week" id="filter0">Week 0 <span class="plus-icon" data-icon="S"></span></li>
<div class="filter-week" id="fi0">
<ul>
<li>E-LECTURE  </li>
<li>Video Lecture</li>
<li>Concept</li>
</ul>
 </div>


<li class="week" id="filter1">Week 1 <span class="plus-icon" data-icon="S"></span></li>
<div class="filter-week" id="fi1">
<ul>
<li>E-LECTURE  </li>
<li>Video Lecture</li>
<li>Concept</li>
</ul> 
 </div>

<li class="week" id="filter2">Week 2 <span class="plus-icon" data-icon="S"></span></li>
<div class="filter-week" id="fi2">
<ul>
<li>E-LECTURE  </li>
<li>Video Lecture</li>
<li>Concept</li>
</ul>
 </div>

<li class="week" id="filter3">Week 3 <span class="plus-icon" data-icon="S"></span></li>
<div class="filter-week" id="fi3">
<ul>
<li>E-LECTURE  </li>
<li>Video Lecture</li>
<li>Concept</li>
</ul>
 </div>

<li class="week" id="filter4">Week 4 <span class="plus-icon" data-icon="S"></span></li>
<div class="filter-week" id="fi4">
<ul>
<li>E-LECTURE  </li>
<li>Video Lecture</li>
<li>Concept</li>
</ul>
 </div>


</div>



</div></section>
<?php include('footer.php');?>