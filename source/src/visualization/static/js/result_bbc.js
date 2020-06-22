window.onload = function() {
  var vid_name = $("#Vname").text()
  console.log(vid_name);
  addResult("#listvideo",vid_name,"bbc_vasnet_knapsack");
  addResult("#listvideo1",vid_name,"bbc_vasnetjanine_knapsack");
  addResult("#listvideo2",vid_name,"bbc_janine_knapsack");
  addResult("#listvideo3",vid_name,"twopeak_vasnet_knapsack");

}

function addResult(_id,vidname,method) {
  for (len of ['150s','300s','450s','600s'])
  {
    addVideo(_id,method+"_"+len,"/result/TRECVID_BBC_EastEnders/"+method+"/"+ method+"_"+len+".mp4","video/mp4")
  }
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
