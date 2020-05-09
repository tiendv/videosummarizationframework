$(function(){

  // TVSum50
  showEval("TVSum","Uniform_Random_Knapsack","result_tvsum");
  showEval("TVSum","SuperFrame_Knapsack","result_tvsum");
  showEval("TVSum","DSF_Kmedoids","result_tvsum");
  showEval("TVSum","DSF_Resnet50_Kmedoids","result_tvsum");
  showEval("TVSum","DSF_VGG16_Kmedoids","result_tvsum");
  showEval("TVSum","KTS_GoogLeNet_Random_Knapsack","result_tvsum");
  showEval("TVSum","One-peak_Random_Knapsack","result_tvsum");
  showEval("TVSum","Randomized-KTS_GoogLeNet_Random_Knapsack","result_tvsum");
  showEval("TVSum","Rethinking_Uniform_Random_Knapsack","result_tvsum");
  showEval("TVSum","Two-peak_Random_Knapsack","result_tvsum");






  // SumMe
  showEval("SumMe","Uniform_Random_Knapsack","result_summe");
  showEval("SumMe","DSF_Kmedoids","result_summe");
  showEval("SumMe","DSF_VGG16_Kmedoids","result_summe");
  showEval("SumMe","KTS_DSF_Kmedoids","result_summe");
  showEval("SumMe","KTS_DSF_VGG16_Kmedoids","result_summe");
  showEval("SumMe","Rethinking_Uniform_Random_Knapsack","result_summe");
  showEval("SumMe","Randomized-KTS_GoogLeNet_Random_Knapsack","result_summe");
  showEval("SumMe","KTS_GoogLeNet_Random_Knapsack","result_summe");
  showEval("SumMe","One-peak_Random_Knapsack","result_summe");
  showEval("SumMe","Two-peak_Random_Knapsack","result_summe");

});

function showEval(ds_name,mt,id)
{
  json_path = "evaluation/"+ds_name+"/"+mt+"/"+mt+".json"
  $.getJSON(json_path, function( data ) {
        var val = data['result']['mean'];
        $('#'+id+' tr:last').after('<tr><td>'+mt+'</td><td>'+val['pre']+'</td><td>'+val['rc']+'</td><td>'+val['f1']+'</td><td></tr>');
     });
}
