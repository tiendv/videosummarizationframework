window.onload = function() {
  var vid_name = $("#Vname").text()
  console.log(vid_name);
  addResult(vid_name,"dsf_seg_vsum_rgb");
  addResult(vid_name,"dsf_seg_vsum_rgb_vgg16");
  addResult(vid_name,"emotion_seg_vsum_dsf_fix");
  addResult(vid_name,"event_seg_vsum_dsf_fix");


}

function addResult(vidname,method) {
  addVideo(method,"/result/TRECVID_BBC_EastEnders/"+method+"/"+ vidname+"_"+method+".mp4","video/mp4")
}

function addVideo(_title,_src,_type) {
  var video = $('<video />', {
      width: 320,
      height:240,
      src: _src,
      type: _type,
      controls: true
  });
  video.appendTo($('#listvideo'));
  var title = $('<p />', {
      text: _title
  });
  title.appendTo($('#listvideo'));
}
