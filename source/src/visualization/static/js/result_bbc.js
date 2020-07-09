window.onload = function() {
  var vid_name = $("#Vname").text()
  console.log(vid_name);
  addResult("#listvideo",vid_name,"bbc_vasnet_knapsack",0);
  addResult("#listvideo",vid_name,"bbc_vasnetjanine_knapsack",0);
  addResult("#listvideo",vid_name,"bbc_janine_knapsack",0);
  addResult("#listvideo",vid_name,"twopeak_vasnet_knapsack",0);
  addResult("#listvideo1",vid_name,"bbc_vasnet",1);
  addResult("#listvideo1",vid_name,"bbc_vasnetjanine",1);
  addResult("#listvideo1",vid_name,"bbc_janine",1);
  addResult("#listvideo2",vid_name,"bbc2.32_vasnet_knapsack",0);
  addResult("#listvideo2",vid_name,"bbc2.32_vasnetjanine_knapsack",0);
  addResult("#listvideo2",vid_name,"bbc2.32_janine_knapsack",0);
  addVideo("#listvideo3","bbc_feature_kmedoids_20s","/result/TRECVID_BBC_EastEnders/bbc_feature_kmedoids/bbc_feature_kmedoids_20s.mp4","video/mp4")
  addResult("#listvideo3",vid_name,"bbc175_vasnetjanine_knapsack",2);

}

function addResult(_id,vidname,method,type) {
  if (type == 0)
    for (len of ['600s'])
    {
      addVideo(_id,method+"_"+len,"/result/TRECVID_BBC_EastEnders/"+method+"/"+ method+"_"+len+".mp4","video/mp4")
    }
  else if (type == 1)
  {
    var len = 'top20'
    addVideo(_id,method+"_"+len,"/result/TRECVID_BBC_EastEnders/"+method+"/"+ method+"_"+len+".mp4","video/mp4")
  }
  else if (type == 2)
  {
    for (len of ['60s','120s','180s'])
    {
      addVideo(_id,method+"_"+len,"/result/TRECVID_BBC_EastEnders/"+method+"/"+ method+"_"+len+".mp4","video/mp4")
    }
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
