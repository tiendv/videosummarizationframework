$(function() {
    // $('#submit').click(function() {
    //     event.preventDefault();
    //     var form_data = new FormData($('#uploadform')[0]);
    //     $.ajax({
    //         type: 'POST',
    //         url: '/uploadajax',
    //         data: form_data,
    //         async: false,
    //         cache: false,
    //         contentType: false,
    //         enctype: 'multipart/form-data',
    //         processData: false,
    //         success: function (response) {
    //         //alert(response);
    //         window.location.replace("?file_id="+response);
    //         }
    //        });
    //
    //        return false;
    //  })
     var url_string = window.location.href;
     var url = new URL(url_string);
     var file_id = url.searchParams.get("file_id");
     console.log(file_id);
     load_video(file_id);

     $.getJSON( "TRECVID_BBC_EastEnders/metadata/"+file_id.split(".")[0]+".json", function( data ) {

        var items = [];
        var eval_text = ""
        console.log(data["date"]);
        // $.each( data, function( key, val ) {
        //      eval_text = eval_text + key + ": " + val + "     "
        // });
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
                'json/TRECVID_BBC_EastEnders/shots/'+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/TRECVID_BBC_EastEnders/kf/'+file_id.replace(file_id.split(".")[file_id.split(".").length-1],'json'),
                'json/TRECVID_BBC_EastEnders/selected/GT/'+file_id.split(".")[0]+"/chelsea.json",
                'json/TRECVID_BBC_EastEnders/selected/GT/'+file_id.split(".")[0]+"/darrin.json",
                'json/TRECVID_BBC_EastEnders/selected/GT/'+file_id.split(".")[0]+"/garry.json",
                'json/TRECVID_BBC_EastEnders/selected/GT/'+file_id.split(".")[0]+"/heather.json",
                'json/TRECVID_BBC_EastEnders/selected/GT/'+file_id.split(".")[0]+"/max.json",
                'json/TRECVID_BBC_EastEnders/selected/GT/'+file_id.split(".")[0]+"/minty.json",
                'json/TRECVID_BBC_EastEnders/selected/GT/'+file_id.split(".")[0]+"/mo.json",
                'json/TRECVID_BBC_EastEnders/selected/GT/'+file_id.split(".")[0]+"/zainab.json",
                'json/TRECVID_BBC_EastEnders/selected/GT/'+file_id.split(".")[0]+"/jane.json",
                'json/TRECVID_BBC_EastEnders/selected/GT/'+file_id.split(".")[0]+"/jack.json",
                'json/TRECVID_BBC_EastEnders/events/'+file_id.split(".")[0]+"/"+file_id.split(".")[0]+".json",
                'json/TRECVID_BBC_EastEnders/events_emotion/'+file_id.split(".")[0]+"/"+file_id.split(".")[0]+".json",

            ],
            list: [
                {
                    'className': 'fr.ina.amalia.player.plugins.TimelinePlugin',
                    'container': '#myplayer-timeline-timeline',
                    'parameters': {
                        listOfLines: [
				                    {
                                title: 'chelsea-INS-Score',
                                type: 'segment',
                                metadataId: 'chelsea',
                                color: '#F00'
                            },
				                    {
                                title: 'darrin-INS-Score',
                                type: 'segment',
                                metadataId: 'darrin',
                                color: '#F00'
                            },
				                    {
                                title: 'garry-INS-Score',
                                type: 'segment',
                                metadataId: 'garry',
                                color: '#F00'
                            },
				                    {
                                title: 'heather-INS-Score',
                                type: 'segment',
                                metadataId: 'heather',
                                color: '#F00'
                            },
				                    {
                                title: 'max-INS-Score',
                                type: 'segment',
                                metadataId: 'max',
                                color: '#F00'
                            },
				                    {
                                title: 'minty-INS-Score',
                                type: 'segment',
                                metadataId: 'minty',
                                color: '#F00'
                            },
				                    {
                                title: 'mo-INS-Score',
                                type: 'segment',
                                metadataId: 'mo',
                                color: '#F00'
                            },
				                    {
                                title: 'zainab-INS-Score',
                                type: 'segment',
                                metadataId: 'zainab',
                                color: '#F00'
                            },
				                    {
                                title: 'jane-INS-Score',
                                type: 'segment',
                                metadataId: 'jane',
                                color: '#F00'
                            },
				                    {
                                title: 'jack-INS-Score',
                                type: 'segment',
                                metadataId: 'jack',
                                color: '#F00'
                            },
                            {
                                title: 'Events',
                                type: 'cuepoint',
                                metadataId: 'event_bbc',
                                color: "#3CF",
                                pointNav: true
                            },
                            {
                                title: 'Emotions',
                                type: 'cuepoint',
                                metadataId: 'emotions',
                                color: "#3CF",
                                pointNav: true
                            },
                            {
                                title: 'Shot[GT]',
                                type: 'cuepoint',
                                metadataId: 'events-amalia01',
                                color: "#3CF",
                                pointNav: true
                            },
				            {
                                title: 'Sum[GT]',
                                type: 'segment',
                                metadataId: 'seg_GT',
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
