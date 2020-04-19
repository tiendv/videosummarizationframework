window.onload = function() {
  var vid_name = $("#Vname").text()
  console.log(vid_name);
  addVideo("this is title","/result/TRECVID_BBC_EastEnders/dsf_seg_vsum_rgb/5136783892766027774_dsf_seg_vsum_rgb.mp4","video/mp4")
  addVideo("this is title","/result/TRECVID_BBC_EastEnders/dsf_seg_vsum_rgb/5136783892766027774_dsf_seg_vsum_rgb.mp4","video/mp4")

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
