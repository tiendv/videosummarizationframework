$(function() {
     var url_string = window.location.href;
     var url = new URL(url_string);
     var file_id = url.searchParams.get("file_id");
     console.log(file_id);
     load_video(file_id);

     $.getJSON( "TRECVID_BBC_EastEnders/metadata/"+file_id.split(".")[0]+".json", function( data ) {

        var items = [];
        var eval_text = ""
        console.log(data["date"]);

        $('#date_bbc').text("Date: "+data["date"])

      });

});

function load_video(file_id){
  if(file_id != null){
    $("#myplayer-timeline").mediaPlayer({

        autoplay : false,

        src : "TRECVID_BBC_EastEnders/videos/"+file_id,
        plugins: {
            dataServices: [
              'json/TRECVID_BBC/selected/person_shot/'+file_id.split(".")[0]+'/janine.json',
              'json/TRECVID_BBC/selected/person_shot/'+file_id.split(".")[0]+'/ryan.json',
              'json/TRECVID_BBC/selected/person_shot/'+file_id.split(".")[0]+'/stacey.json',

              'json/TRECVID_BBC/selected/bbc_vasnet_knapsack_150s/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
              'json/TRECVID_BBC/selected/bbc_vasnetjanine_knapsack_150s/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
              'json/TRECVID_BBC/selected/bbc_janine_knapsack_150s/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
              'json/TRECVID_BBC/selected/twopeak_vasnet_knapsack_150s/'+file_id.split(".")[0]+"/"+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),

            ],
            list: [
                {
                    'className': 'fr.ina.amalia.player.plugins.TimelinePlugin',
                    'container': '#myplayer-timeline-timeline',
                    'parameters': {
                        listOfLines: [
                            {
                                title: 'JANINE',
                                type: 'segment',
                                metadataId: 'janine',
                                color: '#F00'
                            },
                            {
                                title: 'RYAN',
                                type: 'segment',
                                metadataId: 'ryan',
                                color: '#F00'
                            },
                            {
                                title: 'STACEY',
                                type: 'segment',
                                metadataId: 'stacey',
                                color: '#F00'
                            },

                            {
                                title: 'Sum[bbc_vasnet_knapsack_150s]',
                                type: 'segment',
                                metadataId: 'bbc_vasnet_knapsack_150',
                                color: '#F00'
                            },
                            {
                                title: 'Sum[bbc_vasnetjanine_knapsack_150s]',
                                type: 'segment',
                                metadataId: 'bbc_vasnetjanine_knapsack_150',
                                color: '#F00'
                            },
                            {
                                title: 'Sum[bbc_janine_knapsack_150s]',
                                type: 'segment',
                                metadataId: 'bbc_janine_knapsack_150',
                                color: '#F00'
                            },
                            {
                                title: 'Sum[twopeak_vasnet_knapsack_150s]',
                                type: 'segment',
                                metadataId: 'twopeak_vasnet_knapsack_150',
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
