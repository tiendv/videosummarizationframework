$(function(){
  // TVSum50
  showEval("evaluation/TVSum/Random/Random.json","Random","result_tvsum");
  showEval("evaluation/TVSum/SuperF/SuperF.json","SuperFrame","result_tvsum");
  showEval("evaluation/TVSum/vsum_dsf/vsum_dsf.json","vsum_dsf","result_tvsum");
  showEval("evaluation/TVSum/dsf_vgg16_m/dsf_vgg16_m.json","dsf_vgg16","result_tvsum");
  showEval("evaluation/TVSum/dsf_resnet50/dsf_resnet50.json","dsf_resnet50","result_tvsum");
  // SumMe
  showEval("evaluation/SumMe/Random/Random.json","Random","result_summe");
  showEval("evaluation/SumMe/vsum_dsf/vsum_dsf.json","vsum_dsf","result_summe");
  showEval("evaluation/SumMe/dsf_vgg16/dsf_vgg16.json","dsf_vgg16","result_summe");

});

function showEval(json_path,mt,id)
{
  $.getJSON(json_path, function( data ) {
        var val = data['result']['mean'];
        $('#'+id+' tr:last').after('<tr><td>'+mt+'</td><td>'+val['pre']+'</td><td>'+val['rc']+'</td><td>'+val['f1']+'</td><td></tr>');
     });
}
