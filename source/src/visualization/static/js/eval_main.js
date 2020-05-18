$(function(){

  // TVSum50
  showEval("TVSum","Uniform2s_Random_Knapsack","result_tvsum");
  showEval("TVSum","SuperFrame_Knapsack","result_tvsum");
  showEval("TVSum","Uniform2s_DSF_Kmedoids","result_tvsum");
  showEval("TVSum","Uniform2s_DSF-Resnet50_Kmedoids","result_tvsum");
  showEval("TVSum","Uniform2s_DSF-VGG16_Kmedoids","result_tvsum");
  showEval("TVSum","KTS_DSF_Kmedoids","result_tvsum");
  showEval("TVSum","KTS_DSF-VGG16_Kmedoids","result_tvsum");
  showEval("TVSum","KTS_DSF-RESNET50_Kmedoids","result_tvsum");
  showEval("TVSum","KTS_DSF-RESNET152_Kmedoids","result_tvsum");
  showEval("TVSum","KTS_DSF-INCEPTIONV3_Kmedoids","result_tvsum");
  showEval("TVSum","KTS_GoogLeNet_Random_Knapsack","result_tvsum");
  showEval("TVSum","KTS_GoogLeNet_DR-DSN_Knapsack","result_tvsum");
  showEval("TVSum","KTS_GoogLeNet_VASNet_Knapsack","result_tvsum");
  showEval("TVSum","One-peak_Random_Knapsack","result_tvsum");
  showEval("TVSum","One-peak_DR-DSN_Knapsack","result_tvsum");
  showEval("TVSum","One-peak_VASNet_Knapsack","result_tvsum");
  showEval("TVSum","Two-peak_Random_Knapsack","result_tvsum");
  showEval("TVSum","Two-peak_DR-DSN_Knapsack","result_tvsum");
  showEval("TVSum","Two-peak_VASNet_Knapsack","result_tvsum");
  showEval("TVSum","Randomized-KTS_GoogLeNet_Random_Knapsack","result_tvsum");
  showEval("TVSum","Randomized-KTS_GoogLeNet_DR-DSN_Knapsack","result_tvsum");
  showEval("TVSum","Randomized-KTS_GoogLeNet_VASNet_Knapsack","result_tvsum");
  showEval("TVSum","Rethinking_Uniform_Random_Knapsack","result_tvsum");
  showEval("TVSum","Rethinking_Uniform_DR-DSN_Knapsack","result_tvsum");
  showEval("TVSum","Rethinking_Uniform_VASNet_Knapsack","result_tvsum");






  // SumMe
  showEval("SumMe","Uniform2s_Random_Knapsack","result_summe");
  showEval("SumMe","DSF_Kmedoids","result_summe");
  showEval("SumMe","DSF-VGG16_Kmedoids","result_summe");
  showEval("SumMe","KTS_DSF_Kmedoids","result_summe");
  showEval("SumMe","KTS_DSF-VGG16_Kmedoids","result_summe");
  showEval("SumMe","Rethinking_Uniform_Random_Knapsack","result_summe");
  showEval("SumMe","Rehinking_Uniform_DR-DSN_Knapsack","result_summe");
  showEval("SumMe","Rethinking_Uniform_VASNet_Knapsack","result_summe");
  showEval("SumMe","Randomized-KTS_GoogLeNet_Random_Knapsack","result_summe");
  showEval("SumMe","Randomized-KTS_GoogLeNet_DR-DSN_Knapsack","result_summe");
  showEval("SumMe","Randomized-KTS_GoogLeNet_VASNet_Knapsack","result_summe");
  showEval("SumMe","KTS_GoogLeNet_Random_Knapsack","result_summe");
  showEval("SumMe","KTS_GoogLeNet_DR-DSN_Knapsack","result_summe");
  showEval("SumMe","KTS_GoogLeNet_VASNet_Knapsack","result_summe");
  showEval("SumMe","One-peak_Random_Knapsack","result_summe");
  showEval("SumMe","One-peak_DR-DSN_Knapsack","result_summe");
  showEval("SumMe","One-peak_VASNet_Knapsack","result_summe");
  showEval("SumMe","Two-peak_Random_Knapsack","result_summe");
  showEval("SumMe","Two-peak_DR-DSN_Knapsack","result_summe");
  showEval("SumMe","Two-peak_VASNet_Knapsack","result_summe");

});

function showEval(ds_name,mt,id)
{
  json_path = "evaluation/"+ds_name+"/"+mt+"/"+mt+".json"
  $.getJSON(json_path, function( data ) {
        var val = data['result']['mean'];
        $('#'+id+' tr:last').after('<tr><td>'+mt+'</td><td>'+val['pre']+'</td><td>'+val['rc']+'</td><td>'+val['f1']+'</td><td></tr>');
     });
}
