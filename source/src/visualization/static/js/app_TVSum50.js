$(function() {
     var url_string = window.location.href;
     var url = new URL(url_string);
     var para_title = (url.searchParams.get("para_title")).replace(/_/g," ")
     var file_id = url.searchParams.get("file_id");
     console.log(file_id);
     console.log(para_title)
     load_video(file_id);
     document.getElementById("title").innerHTML =  para_title
});

function load_video(file_id){
  if(file_id != null){
    $("#myplayer-timeline").mediaPlayer({

        autoplay : false,

        src : "TVSum50/ydata-tvsum50-v1_1/video/"+file_id,
        plugins: {
            dataServices: [
                'json/TVSum/shots/GT/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/TVSum/shots/BL/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/TVSum/kf/'+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/TVSum/selected/GT/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/TVSum/selected/BL/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),

            ],
            list: [
                {
                    'className': 'fr.ina.amalia.player.plugins.TimelinePlugin',
                    'container': '#myplayer-timeline-timeline',
                    'parameters': {
                        listOfLines: [
                            {
                                title: 'Shot with score[GT]',
                                type: 'cuepoint',
                                metadataId: 'shot_gt',
                                color: "#3CF",
                                pointNav: true
                            },
                            {
                                title: 'Shot seg[Baseline]',
                                type: 'cuepoint',
                                metadataId: 'shot_bl',
                                color: "#3CF",
                                pointNav: true
                            },
                            {
                                title: 'Sum[GT]',
                                type: 'segment',
                                metadataId: 'seg_GT',
                                color: '#F00'
                            },
                            {
                                title: 'Sum[Base line]',
                                type: 'segment',
                                metadataId: 'seg_bl',
                                color: '#F00'
                            },
                            {
                                title: 'Keyframe',
                                type: 'image',
                                metadataId: 'kf-amalia01',
                                pointNav: true
                            },

                        ]
                    }
                }
            ]
        }
      });
  }
}
