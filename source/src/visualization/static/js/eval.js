
$(function() {
    var dataset = $("#dataset").text()
    var method = $("#method").text()
    console.log(dataset);

    if (dataset=='TVSum50')
    {
      if (method=='Random')
        getResult("evaluation/TVSum/Random/Random.json",0);
      else if (method == "SuperFrame" )
        getResult("evaluation/TVSum/SuperF/SuperF.json",0);
      else if (method == "VSumDSF" )
        getResult("evaluation/TVSum/vsum_dsf/vsum_dsf.json",0);
      else if (method == "DSFvgg16m" )
        getResult("evaluation/TVSum/dsf_vgg16_m/dsf_vgg16_m.json",0);
      else if (method == "DSFresnet50" )
        getResult("evaluation/TVSum/dsf_resnet50/dsf_resnet50.json",0);
    }
    else if (dataset=='SumMe')
    {
      if (method=='Random')
        getResult("evaluation/SumMe/Random/Random.json",1);
      else if (method == "SuperFrame" )
        getResult("evaluation/SumMe/SuperF/SuperF.json",1);
      else if (method == "VSumDSF" )
        getResult("evaluation/SumMe/vsum_dsf/vsum_dsf.json",1);
      else if (method == "DSF_vgg16" )
        getResult("evaluation/SumMe/dsf_vgg16/dsf_vgg16.json",1);

    }

});


function getResult(json_path,k)
{
     $.getJSON(json_path, function( data ) {

        var result = data['result'];
        // var items = [];
        var result_data = [];
        var i = 0;
        // result_data.push(method_name);
        $.each( result, function( key, val ) {
             i = i + 1;
             if (key == 'mean')
                $('#result tr:last').after('<tr><th scope="row"> </th><th>'+key+'</th><th>'+val['pre']+'</th><th>'+val['rc']+'</th><th>'+val['f1']+'</th><th></tr>');
             else if (k==0)
                $('#result tr:last').after('<tr><th scope="row">'+i+'</th><td><a href="/visualTVSum50?file_id='+key+'.mp4&#38para_title=">'+key+'</a></td><td>'+val['pre']+'</td><td>'+val['rc']+'</td><td>'+val['f1']+'</td><td></tr>');
             else if (k==1)
                $('#result tr:last').after('<tr><th scope="row">'+i+'</th><td><a href="/visualSumMe?file_id='+key+'.mp4">'+key+'</a></td><td>'+val['pre']+'</td><td>'+val['rc']+'</td><td>'+val['f1']+'</td><td></tr>');

        });


      });
}
