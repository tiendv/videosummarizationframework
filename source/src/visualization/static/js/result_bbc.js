window.onload = function() {
  var vid_name = $("#Vname").text()
  console.log(vid_name);
  addResult("#listvideo",vid_name,"bbc_random_knapsack","150s");
  addResult("#listvideo",vid_name,"bbc_random_knapsack","300s");
  addResult("#listvideo",vid_name,"bbc_random_knapsack","450s");
  addResult("#listvideo",vid_name,"bbc_random_knapsack","600s");
  addResult("#listvideo1",vid_name,"bbc_vasnet_knapsack","150s");
  addResult("#listvideo1",vid_name,"bbc_vasnet_knapsack","300s");
  addResult("#listvideo1",vid_name,"bbc_vasnet_knapsack","450s");
  addResult("#listvideo1",vid_name,"bbc_vasnet_knapsack","600s");




}

function addResult(_id,vidname,method,len) {
  addVideo(_id,method+"_"+len,"/result/TRECVID_BBC_EastEnders/"+method+"/"+ method+"_"+len+".mp4","video/mp4")
}

function addVideo(_id,_title,_src,_type) {
  var video = $('<video/>', {
      width: 320,
      height:240,
      src: _src,
      type: _type,
      controls: true
  });
  video.appendTo($(_id));
  var title = $('<p />', {
      text: _title
  });
  title.appendTo($(_id));
}
