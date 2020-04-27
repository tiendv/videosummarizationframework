$(function(){

  // TVSum50
  showEval("evaluation/TVSum/Uniform_Random_Knapsack/Uniform_Random_Knapsack.json","Uniform_Random_Knapsack","result_tvsum");
  showEval("evaluation/TVSum/SuperFrame_Knapsack/SuperFrame_Knapsack.json","SuperFrame_Knapsack","result_tvsum");
  showEval("evaluation/TVSum/DSF_Kmedoids/DSF_Kmedoids.json","DSF_Kmedoids","result_tvsum");
  showEval("evaluation/TVSum/DSF_Resnet50_Kmedoids/DSF_Resnet50_Kmedoids.json","DSF_Resnet50_Kmedoids","result_tvsum");
  showEval("evaluation/TVSum/DSF_VGG16_Kmedoids/DSF_VGG16_Kmedoids.json","DSF_VGG16_Kmedoids","result_tvsum");
  // SumMe
  showEval("evaluation/SumMe/Uniform_Random_Knapsack/Uniform_Random_Knapsack.json","Uniform_Random_Knapsack","result_summe");
  showEval("evaluation/SumMe/DSF_Kmedoids/DSF_Kmedoids.json","DSF_Kmedoids","result_summe");
  showEval("evaluation/SumMe/DSF_VGG16_Kmedoids/DSF_VGG16_Kmedoids.json","DSF_VGG16_Kmedoids","result_summe");
  showEval("evaluation/SumMe/Rethinking_Uniform_Random_Knapsack/Rethinking_Uniform_Random_Knapsack.json","Rethinking_Uniform_Random_Knapsack","result_summe");
  showEval("evaluation/SumMe/Randomized-KTS_Random_Knapsack/Randomized-KTS_Random_Knapsack.json","Randomized-KTS_Random_Knapsack","result_summe");
  showEval("evaluation/SumMe/KTS_GoogLeNet_Random_Knapsack/KTS_GoogLeNet_Random_Knapsack.json","KTS_GoogLeNet_Random_Knapsack","result_summe");
  showEval("evaluation/SumMe/One-peak_Random_Knapsack/One-peak_Random_Knapsack.json","One-peak_Random_Knapsack","result_summe");
  showEval("evaluation/SumMe/Two-peak_Random_Knapsack/Two-peak_Random_Knapsack.json","Two-peak_Random_Knapsack","result_summe");

});

function showEval(json_path,mt,id)
{
  $.getJSON(json_path, function( data ) {
        var val = data['result']['mean'];
        $('#'+id+' tr:last').after('<tr><td>'+mt+'</td><td>'+val['pre']+'</td><td>'+val['rc']+'</td><td>'+val['f1']+'</td><td></tr>');
     });
}
