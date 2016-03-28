var commentarea=$('#commentarea');
var commentbox=$('#commentbox');
var totalcomments=parseInt(document.getElementById('total_comments_present').innerText);
count=5;
var limit = Math.ceil(totalcomments/5)*5;
var difference_of_count_totalcomments=limit-totalcomments;
post_count=0;
isDisable=false;
window.onload = loadcomments;


            //For loading of group of 5 comments (count is the end point in the range)
                function loadcomments() {
                $.ajax({
                      url : 'loadcomments/',
                      data : { 'count':count},
                      type : "GET",
                      success : function(json_from_view) {
                        if(typeof json_from_view != 'undefined' && json_from_view.length > 0)
                        {
              if(count>5){
                if(commentarea.css('overflow-y')!='scroll') {
                      commentarea.css('overflow-y','scroll');
                    }
                  }   
                   
                  for( var i=0;i<json_from_view.length;i++){
              $('#commentarea ul').prepend('<li style="list-style-type:none;" class="comment"><article><p id="comment_para" style="font-size:80%;color:black;">'+json_from_view[i][1]+'</p><p style="font-size:80%;color:black;"><span class="label label-default" id="user_id_para" style="float:right;">'+json_from_view[i][0]+'</span></p></small></article></li><hr style="height:0.2px;border:none;background-color:#E6E6E6">');

                  }
              $('#viewing_comments').html(count+post_count);
              if(totalcomments<5)
                $('#viewing_comments').html(totalcomments);

                       
                      if(count<totalcomments){
                            count=count+5;
                          }
                          else{
                            count=count+1;
                          $('#more_comments_row').toggle();
                          $('#done_loading_comments').toggle();
                          }
              }
                else{
              $('#welcome_comment').append('<span style="font-size:90%;">Be the first to comment!!!</span>');
              $('#more_comments_row').html('No comment present.');
              $('#viewing_comments').html('0');

                }

                  },

                  error : function(xhr,errmsg,err) {
                      $('#results').html("Unable to load comments"); 
              }
            
          });        
          }


            //For typed comment characters count
            commentbox.on('keyup keypress keydown paste', function(event) {
              maxLength=150;
              var submitButton = $('#comment_post_button');
                var length = $(this).val().length;
                length = maxLength-length;
                $('#characters').text(length);
                if (length<0 || length>130){
                  isDisable=true;
                        submitButton.prop('disabled',true);
                        $('#characters').css('color','red');

                }
                else{
                  if(isDisable){
                  submitButton.prop('disabled',false);
                  isDisable=false;
                }
                        $('#characters').css('color','blue');
                }
              });


          //For AJAX posting of comments
          $('#comment_form').on('submit', function(event){
            event.preventDefault();
            // For checking existance of only white spaces other than characters
            if(commentbox.val().replace(/ /g,'')===''){
                alert('Comment is consist of only spaces. Type characters!');
                return false;
              }
            post_comment();
          });



          // Move ScrollBar down each time a comment is posted
          function moveScrollDown(){
                  if( commentarea.css('overflow-y')!='scroll') {


            commentarea.css('overflow-y','scroll');
          }
                // Scroll to last comment made
                commentarea.animate({scrollTop:$('#commentarea ul').height()}, 'slow');

          }


          // AJAX POST request to post the comment
          function post_comment() {

            if(count<=5){
              $('#more_comments_row').html('All comments viewed.')

            }
          $.ajax({
              url : "postcomment/",
              type : "GET",
              data : { comment : commentbox.val() },

              success : function(json_from_view) {
                  commentbox.val(''); 
                  commentarea.find('#welcome_comment').remove();


      if($(".comment").length>5)
        commentarea.css('overflow-y','scroll');
      $('#commentarea ul').append('<li style="list-style-type:none; class="comment"><article><p id="comment_para" style="font-size:100%;color:black;">'+json_from_view.comment+'</p><p style="font-size:100%;color:black;"><span class="label label-default" id="user_id_para" style="float:right;">'+json_from_view.user_id+'</span></p></small></article></li><hr style="height:1px;border:none;background-color:#E6E6E6">');

      $('#viewing_comments').html(parseInt($('#viewing_comments').text())+1);
      post_count+=1
      $('#total_comments_present').html(totalcomments+post_count);

      moveScrollDown();
              },

              error : function(xhr,errmsg,err) {
                  $('#results').html("Your comment was not posted!!! Try again."); 
          }
      });
      }


      //For loading more comments
      $('#more_comments').on('click',function(event){
        event.preventDefault();
        if( commentarea.css('overflow-y')!='scroll') {
                  commentarea.css('overflow-y','scroll');
            }
            if(count==limit)
              count=count-difference_of_count_totalcomments;
              if(count<=totalcomments){
        loadcomments();
      }
          
      });

