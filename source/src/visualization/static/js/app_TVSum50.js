$(function() {
     var url_string = window.location.href;
     var url = new URL(url_string);
     var para_title = (url.searchParams.get("para_title")).replace(/_/g," ")
     var file_id = url.searchParams.get("file_id");
     console.log(file_id);
     // console.log(para_title)
     load_video(file_id);
     document.getElementById("title").innerHTML =  para_title;
     getResult("evaluation/TVSum/","Random",file_id);
     getResult("evaluation/TVSum/","SuperF",file_id);
     getResult("evaluation/TVSum/","vsum_dsf",file_id);

});


function getResult(path,method_name,file_id)
{
     name_file = file_id.split(".")[0]
     $.getJSON(path + method_name +"/"+method_name+".json", function( data ) {

        var result_data = data['result'][name_file];
        $('#result tr:last').after('<tr><th>'+method_name+'</th><td>'+result_data['pre']+'</td><td>'+result_data['rc']+'</td><td>'+result_data['f1']+'</td></tr>');
      });
}

function load_video(file_id){
  if(file_id != null){
    $("#myplayer-timeline").mediaPlayer({

        autoplay : false,

        src : "TVSum50/ydata-tvsum50-v1_1/video/"+file_id,
        plugins: {
            dataServices: [
                'json/TVSum/shots/GT/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/TVSum/shots/KTS_VGG/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/TVSum/shots/Random/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/TVSum/shots/SuperF/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/TVSum/kf/'+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/TVSum/selected/GT/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/TVSum/selected/Random/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/TVSum/selected/SuperF/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/TVSum/selected/vsum_dsf/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/TVSum/selected/dsf_vgg16/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/TVSum/selected/dsf_resnet50/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),

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
                                title: 'Shot seg[superframe]',
                                type: 'cuepoint',
                                metadataId: 'shot_bl',
                                color: "#3CF",
                                pointNav: true
                            },
                            {
                                title: 'Shot seg[KTS_VGG]',
                                type: 'cuepoint',
                                metadataId: 'KTS_VGG_seg_boundaries',
                                color: "#3CF",
                                pointNav: true
                            },
                            {
                                title: 'Sum[GT]',
                                type: 'segment',
                                metadataId: 'seg_gt',
                                color: '#F00'
                            },
                            {
                                title: 'Sum[Random]',
                                type: 'segment',
                                metadataId: 'seg_rd',
                                color: '#F00'
                            },
                            {
                                title: 'Sum[superframe]',
                                type: 'segment',
                                metadataId: 'seg_sf',
                                color: '#F00'
                            },
                            {
                                title: 'Sum[Dsf]',
                                type: 'segment',
                                metadataId: 'seg_vsum_dsf',
                                color: '#F00'
                            },
                            {
                                title: 'Sum[Dsf_vgg16]',
                                type: 'segment',
                                metadataId: 'seg_vsum_dsf_rgb_only_vgg16',
                                color: '#F00'
                            },
                            {
                                title: 'Sum[Dsf_resnet50]',
                                type: 'segment',
                                metadataId: 'seg_vsum_dsf_rgb_resnet50',
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
        },
        controlBar:{
                     sticky: true,
                     autohide: false,
                     enableProgressBar: false,
                     height: 100,
                     widgets:
                             {
                                 left: {
                                     'timelabelWidget': 'fr.ina.amalia.player.plugins.controlBar.widgets.TimeLabel',
                                     'playWidget': 'fr.ina.amalia.player.plugins.controlBar.widgets.PlayButton',
                                     'pauseWidget': 'fr.ina.amalia.player.plugins.controlBar.widgets.PauseButton'
                                 },
                                 mid: {
                                     'JogShuttle': 'fr.ina.amalia.player.plugins.controlBar.widgets.JogShuttleButton'
                                 },
                                 right: {
                                     'volume': 'fr.ina.amalia.player.plugins.controlBar.widgets.ChannelVolumeControlBar',
                                     'full': 'fr.ina.amalia.player.plugins.controlBar.widgets.FullscreenButton'
                                 },
                                 settings: {
                                     timelabelWidget: {
                                         timeFormat: 's',
                                         framerate: 30
                                     },
                                     sample: {
                                         style: 'fa fa-eye fa-2x',
                                         callback: 'myCallback'
                                     },
                                     secNext: {
                                         style: 'ajs-icon ajs-icon-control-forward',
                                         callback: 'myCallbackControl',
                                         action: 'next'
                                     },
                                     volume: {
                                         channelMerger: false
                                     }
                                 }
                             }
                 }
      });
  }
}
