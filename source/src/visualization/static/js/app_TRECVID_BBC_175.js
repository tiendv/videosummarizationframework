$(function() {
     var url_string = window.location.href;
     var url = new URL(url_string);
     var file_id = url.searchParams.get("file_id");
     console.log(file_id);
     load_video(file_id);


    $('#date_bbc').text(file_id.split('/')[1])

});

function load_video(file_id){
  if(file_id != null){
    $("#myplayer-timeline").mediaPlayer({

        autoplay : false,

        src : "result/TRECVID_BBC_EastEnders/"+file_id+".mp4",
        plugins: {
            dataServices: [
                'json/TRECVID_BBC/shots/scores/' + file_id.split('/')[1] + "/" + file_id.split('/')[1] + ".json",
                'json/TRECVID_BBC/shots/events/' + file_id.split('/')[1] + "/" + file_id.split('/')[1] + ".json",

            ],
            list: [
                {
                    'className': 'fr.ina.amalia.player.plugins.TimelinePlugin',
                    'container': '#myplayer-timeline-timeline',
                    'parameters': {
                        listOfLines: [

                            {
                                title: 'Shot',
                                type: 'cuepoint',
                                metadataId: 'shot175',
                                color: '#F00'
                            },
                            {
                                title: 'Events',
                                type: 'cuepoint',
                                metadataId: 'event_bbc',
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
