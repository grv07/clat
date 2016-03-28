// Get current browser info 
function get_browser_info(){
    var ua=navigator.userAgent,tem,M=ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || []; 
    if(/trident/i.test(M[1])){
        tem=/\brv[ :]+(\d+)/g.exec(ua) || []; 
        return {name:'IE',version:(tem[1]||'')};
        }   
    if(M[1]==='Chrome'){
        tem=ua.match(/\bOPR\/(\d+)/)
        if(tem!=null)   {return {name:'Opera', version:tem[1]};}
        }   
    M=M[2]? [M[1], M[2]]: [navigator.appName, navigator.appVersion, '-?'];
    if((tem=ua.match(/version\/(\d+)/i))!=null) {M.splice(1,1,tem[1]);}
    return {
      name: M[0],
      version: M[1]
    };
 }

// 
var _browser_info = get_browser_info();
 console.log(_browser_info);
 if(_browser_info.name == 'Firefox' && parseInt(_browser_info.version) < 38){
    //Show Warn.
    document.getElementById('_b_notification').style.display = 'block';
 }
 else if(_browser_info.name == 'IE' && parseInt(_browser_info.version) < 11) {
   //Show Warn.
   // ToDO on IE
   // if (navigator.userAgent.indexOf('MSIE') !== -1 || navigator.appVersion.indexOf('Trident/') > 0) {
   // MSIE
    // }
    document.getElementById('_b_notification').style.display = 'block'; 
 }
 else if(_browser_info.name == 'Chrome' && parseInt(_browser_info.version) < 38){
  // Show Warn.
    document.getElementById('_b_notification').style.display = 'block';
 }


