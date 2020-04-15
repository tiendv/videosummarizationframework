$(function(){
  $.getJSON("evaluation/TVSum/Random/Random.json", function( data ) {
        var val = data['result']['mean'];
        $('#result_tvsum tr:last').after('<tr><td>Random</td><td>'+val['pre']+'</td><td>'+val['rc']+'</td><td>'+val['f1']+'</td><td></tr>');
     });
 $.getJSON("evaluation/TVSum/SuperF/SuperF.json", function( data ) {
       var val = data['result']['mean'];
       $('#result_tvsum tr:last').after('<tr><td>SuperFrame</td><td>'+val['pre']+'</td><td>'+val['rc']+'</td><td>'+val['f1']+'</td><td></tr>');
    });
  $.getJSON("evaluation/TVSum/vsum_dsf/vsum_dsf.json", function( data ) {
        var val = data['result']['mean'];
        $('#result_tvsum tr:last').after('<tr><td>vsum_dsf</td><td>'+val['pre']+'</td><td>'+val['rc']+'</td><td>'+val['f1']+'</td><td></tr>');
     });
 $.getJSON("evaluation/TVSum/dsf_vgg16_m/dsf_vgg16_m.json", function( data ) {
       var val = data['result']['mean'];
       $('#result_tvsum tr:last').after('<tr><td>dsf_vgg16</td><td>'+val['pre']+'</td><td>'+val['rc']+'</td><td>'+val['f1']+'</td><td></tr>');
    });
  $.getJSON("evaluation/TVSum/dsf_resnet50/dsf_resnet50.json", function( data ) {
        var val = data['result']['mean'];
        $('#result_tvsum tr:last').after('<tr><td>dsf_resnet50</td><td>'+val['pre']+'</td><td>'+val['rc']+'</td><td>'+val['f1']+'</td><td></tr>');
     });

   $.getJSON("evaluation/SumMe/Random/Random.json", function( data ) {
         var val = data['result']['mean'];
         $('#result_summe tr:last').after('<tr><td>Random</td><td>'+val['pre']+'</td><td>'+val['rc']+'</td><td>'+val['f1']+'</td><td></tr>');
      });
  $.getJSON("evaluation/SumMe/vsum_dsf/vsum_dsf.json", function( data ) {
        var val = data['result']['mean'];
        $('#result_summe tr:last').after('<tr><td>vsum_dsf</td><td>'+val['pre']+'</td><td>'+val['rc']+'</td><td>'+val['f1']+'</td><td></tr>');
     });
   $.getJSON("evaluation/SumMe/dsf_vgg16/dsf_vgg16.json", function( data ) {
         var val = data['result']['mean'];
         $('#result_summe tr:last').after('<tr><td>dsf_vgg16</td><td>'+val['pre']+'</td><td>'+val['rc']+'</td><td>'+val['f1']+'</td><td></tr>');
      });
});
