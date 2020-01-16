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
//             //判断是点赞还是踩灭,注意不能是diggnum
//         var is_up=$(this).hasClass("diggnum");
//         // console.log(is_up);
//          //获取到文章id 在js中需要加引号
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
//                 //如果为真，说明是第一次操作
//                 //console.log(data.state); 都可以使用
//                 // console.log(data["state"]);
//                 if(data.state) {
//                     var val = $("#diggnum").text();  //点赞加1
//                     val = parseInt(val) + 1;
//                     console.log(val);
//                     $("#diggnum").text(val);
//                     // }else{
//                     //      var val=$("#bury_count").text();
//                     //     val=parseInt(val)+1;
//                     //     $("#bury_count").text(val); //踩加1
//                 }
//                 else{
//                     $("#diggnum").html("您赞过了");
//                     // var val=66;
//                     // console.log(val);
//                     // if(data.first_action){
//                     //       $("#diggnum").html("您赞过了");
//                     // }else {
//                     //      $("#diggnum").html("您赞过了");
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