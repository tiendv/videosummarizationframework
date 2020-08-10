var video = getStoredValue('myPageMode')

function show() {
  video = getStoredValue('myPageMode')
  console.log(video);
  video_path = "Demo/video/"+((((video.replace(' ','_')).replace(' ','_')).replace("&","and")).replace("+","")).replace("#","")+".webm"
  console.log(video_path);
  var video = $("#video_player");
  video[0].src = video_path;
  video[0].load();
  video[0].play();
}
function show_sum() {
  video = getStoredValue('myPageMode')
  var segment = $("#selectsegment option:selected").text()
  var score = $("#selectscore option:selected").text()
  var selection = $("#selectselection option:selected").text()
  video_path = "Demo/result/"+segment+"_"+score+"_"+selection+"_"+((((video.replace(' ','_')).replace(' ','_')).replace("&","and")).replace("+","")).replace("#","")+".webm"
  console.log(segment);
  console.log(score);
  console.log(selection);
  console.log(video);
  console.log(video_path);
  var video = $("#sum_video_player");
  video[0].src = video_path;
  video[0].load();
  video[0].play();
}
function loader()
{
        video = (document.getElementById('myFile').value).split(/(\\|\/)/g).pop().split(".")[0]   
        storeValue('myPageMode', video);
        $('#loady').show();
}

function storeValue(key, value) {
    if (localStorage) {
        localStorage.setItem(key, value);
    } else {
        $.cookies.set(key, value);
    }
}
function getStoredValue(key) {
    if (localStorage) {
        return localStorage.getItem(key);
    } else {
        return $.cookies.get(key);
    }
}