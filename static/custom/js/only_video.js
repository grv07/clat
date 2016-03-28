// window.onbeforeunload = function () {
//     return "Do you really want to close?";
// };

//   function userActive(el){
//         $.ajax({
//                     url : "/check/module/",
//                     data : { 'module_name' : '{{module_name}}' ,'el_id': el.id },
//                     type : "GET",

//                     success : function(json_from_view) {
//                       if(json_from_view){
//                         // alert('success');
//                       }
//                     else{
//                         // alert('error');
//                      }
//                     }
//                 ,
//                     // handle a non-successful response
//                     error : function(xhr,errmsg,err) {
//                       alert('Server error in checking module!!!')
//                 }
//                 });
// }
//   $('#frame_id').load(function(){
//         var iframe = $('#frame_id').contents();
//         iframe.bind('mouseup', function(e) {
//         console.log('mouseup');
// });
//         iframe.find('ul#slide_list').mousedown(function(event) {
//           console.log(iframe);
//           userActive(this);
//         });
//         iframe.find('div#control-previous').mouseup(function(event) {
//           userActive(this);
//         });
//         iframe.find('div#control-next').mouseup(function(event) {
//           userActive(this);
//         });
// });

//Increases the height of iframe when loading youtube demo video
$('#youtube-video').css('height','500px');
//Load the corresponding articulate file when modules links are clicked
  function loadVideo(element){
    $(".pop").show();
    // var s='';
    $('#frame_id').attr('src',"http://{{ request.META.HTTP_HOST }}"+$(element).data("video-url"));    
    // $(element).data("video-type")+" "+$(element).data("video-url")+" "+$(element).data("video-file"));
    // $('#video_player_div').html('okie');
    // if($(element).data("video-type") == 'youtube'){
    //   $('#video_player_div').html('');
    //   $('#video_player_div').html('<iframe id="youtube-video" src="https://www.youtube.com/embed/'+$(element).data("video-url")+'?enablejsapi=1&rel=0&iv_load_policy=3" frameborder="0" enablejsapi="1" allowfullscreen width="100%" height="400"></iframe>');
    // }
  if($(element).data("video-type") == 'mp4'){
    // s ='<video id="vid1" controls style="width:100%;height: auto;"><source src="http://{{ request.META.HTTP_HOST }}'+$(element).data("video-url")+'"'+'></video>';
    // $('#course').html(s);
  }
  else{
    // s ='<iframe src="http://{{ request.META.HTTP_HOST }}'+$(element).data("video-url")+'/story.html" width="100%" height="600" class="start_art"></iframe>';
    // $('#course').html(s);
      $('#frame_id').attr('src',""+$(element).data("video-url")+"/story.html");
      }
}
// function collapseWeeks(element){
//   // alert(element.id);
// }
