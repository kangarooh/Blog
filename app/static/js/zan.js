// function dianzan(){
//     $.ajax({
//         url:"/zan",
//         type:'post',
//         data:{
//             "is_up":'True',
//         },
//         dataType:json,
//         success:function (data) {
//
//         }
//
//     })
// }
//
//
// $("#diggnum").on("click",function () {
//             //�ж��ǵ��޻��ǲ���,ע�ⲻ����diggnum
//         var is_up=$(this).hasClass("diggnum");
//         // console.log(is_up);
//          //��ȡ������id ��js����Ҫ������
//         var article_id="{{ article.pk }}";
//         $.ajax({
//             url:"/zan",
//             type:"post",
//             data:{
//                 "is_up":is_up,
//                 "article_id":article_id,
//                 // "csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val(),
//             },
//             success:function(data){
//                 // alert(data);
//                 //���Ϊ�棬˵���ǵ�һ�β���
//                 //console.log(data.state); ������ʹ��
//                 // console.log(data["state"]);
//                 if(data.state) {
//                     var val = $("#diggnum").text();  //���޼�1
//                     val = parseInt(val) + 1;
//                     console.log(val);
//                     $("#diggnum").text(val);
//                     // }else{
//                     //      var val=$("#bury_count").text();
//                     //     val=parseInt(val)+1;
//                     //     $("#bury_count").text(val); //�ȼ�1
//                 }
//                 else{
//                     $("#diggnum").html("���޹���");
//                     // var val=66;
//                     // console.log(val);
//                     // if(data.first_action){
//                     //       $("#diggnum").html("���޹���");
//                     // }else {
//                     //      $("#diggnum").html("���޹���");
//                     //
//                     // }
//                 }
//
//
//
//             }
//
//             }
//
//         )
//
//     })
$(function () {
    $('#diggit').click(function () {
        $.ajax({
            url:'/zan',
            type: get,
            data: {'status':0,'topic.zan':'{{topic.zan}}'},
            dataType:'json',
            success:function (data) {
                if(data['status']){
                    var val = $("#diggnum").text();
                    val = parseInt(val) + 1;
                    $("#diggnum").text(val);
                }
                else{
                    alert(data['message'])
                }

            }
        })

    })

})