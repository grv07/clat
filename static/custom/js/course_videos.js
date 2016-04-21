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

//Increases the height of iframe when loading youtube demo video
$('#youtube-video').css('height','500px');
//Load the corresponding articulate file when modules links are clicked
  function loadVideo(element){
    $(".pop").show();
    $('#frame_id').attr('src',"http://{{ request.META.HTTP_HOST }}"+$(element).data("video-url"));    
  if($(element).data("video-type") == 'mp4'){
  }
  else{
      $('#frame_id').attr('src',""+$(element).data("video-url")+"/story.html");
      }
}
