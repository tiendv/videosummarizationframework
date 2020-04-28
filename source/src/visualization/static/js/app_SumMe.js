$(function() {
     var url_string = window.location.href;
     var url = new URL(url_string);
     var file_id = ((url.searchParams.get("file_id")).replace(/@/g," ")).replace("mp4","webm");
     console.log(file_id);

     load_video(file_id);


});

function load_video(file_id){
  if(file_id != null){
    $("#myplayer-timeline").mediaPlayer({

        autoplay : false,

        src : "SumMe/videos/"+file_id,
        plugins: {
            dataServices: [
                'json/SumMe/shots/GT/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/SumMe/shots/KTS_VGG/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/SumMe/shots/Rethinking/score_random_sample/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/SumMe/shots/Rethinking/segment_boundaries/KTS/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/SumMe/shots/Rethinking/segment_boundaries/one-peak/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/SumMe/shots/Rethinking/segment_boundaries/two-peak/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/SumMe/shots/Rethinking/segment_boundaries/randomized-KTS/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/SumMe/shots/Rethinking/segment_boundaries/uniform/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/SumMe/selected/GT/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/SumMe/selected/Rethinking/KTS/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/SumMe/selected/Rethinking/one-peak/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/SumMe/selected/Rethinking/two-peak/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/SumMe/selected/Rethinking/randomized-KTS/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/SumMe/selected/Rethinking/uniform/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/SumMe/selected/Random/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/SumMe/selected/vsum_dsf/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/SumMe/selected/dsf_vgg16/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),

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
                                metadataId: 'shot_gt_summe',
                                color: "#3CF",
                                pointNav: true
                            } ,
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
                                title: 'Sum[DSF]',
                                type: 'segment',
                                metadataId: 'seg_vsum_dsf',
                                color: '#F00'
                            },
                            {
                                title: 'Sum[DSF_VGG16]',
                                type: 'segment',
                                metadataId: 'seg_vsum_dsf_rgb_only_vgg16',
                                color: '#F00'
                            },
                            {
                                title: 'Random score',
                                type: 'cuepoint',
                                metadataId: 'rethinking_score_random',
                                color: "#3CF",
                                pointNav: true
                            } ,
                            {
                                title: 'Shot seg[Uniform]',
                                type: 'cuepoint',
                                metadataId: 'rethinking_uniform_seg_boundaries',
                                color: "#3CF",
                                pointNav: true
                            },
                            {
                                title: 'Sum[Uniform]',
                                type: 'segment',
                                metadataId: 'rethinking_uniform_seg',
                                color: '#F00'
                            },
                            {
                                title: 'Shot seg[One-peak]',
                                type: 'cuepoint',
                                metadataId: 'rethinking_one-peak_seg_boundaries',
                                color: "#3CF",
                                pointNav: true
                            },
                            {
                                title: 'Sum[One-peak]',
                                type: 'segment',
                                metadataId: 'rethinking_one-peak_seg',
                                color: '#F00'
                            },
                            {
                                title: 'Shot seg[Two-peak]',
                                type: 'cuepoint',
                                metadataId: 'rethinking_two-peak_seg_boundaries',
                                color: "#3CF",
                                pointNav: true
                            },
                            {
                                title: 'Sum[Two-peak]',
                                type: 'segment',
                                metadataId: 'rethinking_two-peak_seg',
                                color: '#F00'
                            },
                            {
                                title: 'Shot seg[KTS_GoogLeNet]',
                                type: 'cuepoint',
                                metadataId: 'rethinking_KTS_seg_boundaries',
                                color: "#3CF",
                                pointNav: true
                            },
                            {
                                title: 'Sum[KTS_GoogLeNet]',
                                type: 'segment',
                                metadataId: 'rethinking_KTS_seg',
                                color: '#F00'
                            },
                            {
                                title: 'Shot seg[Randomized-KTS_GoogLeNet]',
                                type: 'cuepoint',
                                metadataId: 'rethinking_randomized-KTS_seg_boundaries',
                                color: "#3CF",
                                pointNav: true
                            },
                            {
                                title: 'Sum[Randomized-KTS_GoogLeNet]',
                                type: 'segment',
                                metadataId: 'rethinking_randomized-KTS_seg',
                                color: '#F00'
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
