
$(function() {
    var dataset = $("#dataset").text()
    var method = $("#method").text()
    console.log(dataset);

    if (dataset=='TVSum50')
    {
        getResult("evaluation/TVSum/"+method+"/"+method+".json",0);
    }
    else if (dataset=='SumMe')
    {
        getResult("evaluation/SumMe/"+method+"/"+method+".json",0);
    }

});


function getResult(json_path,k){
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
