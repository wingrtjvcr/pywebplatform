var dataIssue;
var dataUser;
var uname = parent.$(".user.active").html();
uname='liqiang'
var noneid='900000001_143';
var nonename='#0：予定なし　ー　900000001_(間接)間接';

// ※※※※※※※※※※※※※※※※※※※             ※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※
// ※※※※※※※※※※※※※※※※※※※　　初期化　　※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※
// ※※※※※※※※※※※※※※※※※※※             ※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※

$(function() {

// 日付コントローラーの初期化
$("#date").datetimepicker({
//设置语言 中文(需引入语言包)
language:'ja',
//选择日期后，不会再跳转去选择时分秒 
minView:'month',
//选择日期后，文本框显示的日期格式 
format:'yyyy-mm-dd',
//选择后自动关闭
autoclose:true,
//显示周 周数据为TRIAL专有周, 周数据范围 2016-01-03 ~ 2021-03-31, 不在范围内此列为空白
weekShow:true
});
$("#date").datetimepicker("setDate", new Date());


// 初期状態はチケットありに設定
$('#ticketsel1').trigger("click");
// コントローラーの表示設定
conshow();

$('#select_pj').select2();
$('#select_wt').select2();
$('#select_issue').select2();

// ui.loading('hide');
ui.loading();
// _url='../cgi/workdata?loginid='+uname;
// $.ajax({
//       type: 'get',
//       url: _url,
//       success: function(data){ 
//         if(data.Code!=1) {
//           ui.loading('hide');
//           // toastr.error('エラー発生');
//           return 
//         }
//        $('#home').html(data);
//        ui.loading('hide');
//     }
// });
$.ajax({
  type: 'POST',
  url: '../cgi-bin/workdata',
  data: { uname : uname },
  success: function(result){ 
    $("#home").html(result); 
    ui.loading('hide');
  
  }
});

// ※※※※※※※※※※※※※※※※※※※                  ※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※
// ※※※※※※※※※※※※※※※※※※※　　Click Event　　※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※
// ※※※※※※※※※※※※※※※※※※※                  ※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※

// QCD TAGをクリック
$('a[href="#qcd"]').click(function(){
  // alert('qcd click');
ui.loading();
_url='../Apps/getIssueList?loginid='+uname;
$.ajax({
      type: 'get',
      url: _url,
      success: function(data){ 
        if(data.Code!=1) {
          ui.loading('hide');
          toastr.error('エラー発生');
          return 
        }
        data=data.Table0;
       var optionsIssue = new Array();
       var optionsProject = new Array();

        // 間接チケットを追加
       optionsIssue.push({id:noneid ,text: nonename});
       //  チケットのデータを入れる
       $(data).each(function (i, o) {
        optionsIssue.push({
               id: o.pjid+'_'+o.issid,
               text: '#'+o.issid+'：'+o.subject+' '+o.statusname +'　ー　'+o.pjname
           });
       });
       $("#select_issue").select2({
           data: optionsIssue
       })

        ui.loading('hide');
    }
});

});

// TODO TAGをクリック
$('a[href="#todo"]').click(function(){
  ui.loading();
  _url='../Apps/getTodo?loginid='+uname;
  $.ajax({
        type: 'get',
        url: _url,
        success: function(data){ 
          if(data.Code!=1) {
            ui.loading('hide');
            toastr.error('エラー発生');
            return 
          }
          data=data.Table0;
        var t='<tr><td>#</td><td>Project</td><td>Tracker</td><td>Status</td><td>Subject</td></tr>';
        var _row='<tr><td><a href="http://redmine.trechina.cn/issues/{0}" target="_blank" >{0}</a></td><td>{1}</td><td>{2}</td><td>{3}</td><td><a href="http://redmine.trechina.cn/issues/{0}" target="_blank" >{4}</a></td></tr>';
        var datarow='';
        //  チケットのデータを入れる
        $(data).each(function (i, o) {
          
          datarow=datarow+String.format(_row,o.issueid,o.pjname,o.tname,o.sname,o.subject);
        });
        $('#todo').html('<table class="table table-striped table-condensed">'+t+datarow+'</table>');

          ui.loading('hide');
      }
  });
});

// 「登録区分」クリック
$('input[name="ticketsel"]').click(function(){
// 日付を今日にリセット
$("#date").datetimepicker("setDate", new Date());
// 画面各コントローラーの表示非表示
conshow();
// チケットなしかつselect_pjに課題データなしの場合は、課題データを読み込む
if(!ischk() && $("#select_pj option").length<=1){
ui.loading();

  _url='../Apps/getProject?loginid='+uname;
  $.ajax({
          type: 'get',
          url: _url,
          success: function(data){ 
          var dataProject=data.result;
          var optionsProject = new Array();
          //  チケットのデータを入れる
          $(dataProject).each(function (i, o) {
            optionsProject.push({
                  id: o.project_id+'_'+o.work_type_id,
                  text: o.project_cd+'_'+o.budget_project_name_half
              });
          });
          $("#select_pj").select2({
              data: optionsProject
          });
          ui.loading('hide');

        }
  });
}

});
// 「登録」クリック
$("#btnAddJS").click(function(){
if($("#select_issue").val()==null && $("#select_pj").val()==null){
  toastr.warning('正しく入力してください');
  return;
}

// 重複クリックを防ぐ
$("#btnAddJS").attr("disabled","disabled");

// チケットありの場合、登録に必要な情報を取得
var memo=$("#inputmemo").val();
var wkhour=$("#inputtime").val();
var pjcode='';
var issueid='';
if($("#select_issue").val()!=null ){
   pjcode=$("#select_issue").val().split('_')[0];
   issueid=$("#select_issue").val().split('_')[1];

}
// var done=$('input[name="progress"]:checked').val();
var done=_done;
// alert(done);

// チケットなしの場合、登録に必要な情報を取得
var date=$("#date").val();
var pjid='';
if($("#select_pj").val()!=null ){
  pjid=$("#select_pj").val().split('_')[0];
}
var wt='';
if($("#select_wt").val()!=null ){
  wt=$("#select_wt").val();
}

// チケットありなしによって、必要データが異なる
if(ischk()){
  if(uname == "" || pjcode == "" || memo == "" || wkhour == ""){
      toastr.warning('正しく入力してください');
      $("#btnAddJS").removeAttr("disabled");
      return false;
  }}
else{
  if(uname == "" || date == "" || pjid =="" || wt=="" || memo == "" ||wkhour == ""){
      toastr.warning('正しく入力してください');
      $("#btnAddJS").removeAttr("disabled");
      return false;
  }
}

// チケットありなしによって、PostUrlが異なる
var _url='';
if(ischk()){
  _url='../Apps/insQCDandRM';
  if($("#select_issue").val()==noneid){
    wt=41;
    _url='../Apps/insQCD';
    pjid=$("#select_issue").val().split('_')[1];
  }

}
else
  _url='../Apps/insQCD';
  ui.loading();
      $.ajax({
      type: 'GET',
              contentType:'application/x-www-form-urlencoded; charset=UTF-8',
      url: _url,
      data: { 
        uname : uname 
      , pjcode : pjcode  
      , memo : memo 
      , wkhour : wkhour 
      , issueid : issueid 
      , done : done
      , pjid : pjid
      , wt:wt
      , date:date
      },
      success: function(resjson){ 
        if(resjson.status=="0"){
          toastr.success('登録成功しました。');
          clearConValue();
        }else{
           toastr.error('登録失敗しました。');
        } 

        $("#btnAddJS").removeAttr("disabled");
        ui.loading('hide');
      },
      error: function(jqXHR, textStatus, errorThrown) {
        toastr.error('ERROR');
        ui.loading('hide');
      }
});

});
// 「進捗」クリック
$("input[type=radio]").click(function(){
var p=$(this).next();
checkp(p.attr('for'));
})

// ※※※※※※※※※※※※※※※※※※※                  ※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※
// ※※※※※※※※※※※※※※※※※※※　　Change Event  ※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※
// ※※※※※※※※※※※※※※※※※※※                  ※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※

// 「チケット」変更
  $("#select_issue").on("change",function(e){
if($("#select_issue").val()==null)return;
    var issueid=$("#select_issue").val().split('_')[1];
    $('#eh_time').html('');
    $('#sh_time').html('');
    $('#lab_time').html('');
    //　間接課題の場合はチケットとしての情報を非表示
    if($('#select_issue').val()==noneid){
      checkp('p0');
      $('#tr_prog').hide();
      return;
    }else{
      $('#tr_prog').show();
    }
    
    _url='../Apps/getIssue?issueid='+issueid;
    $.ajax({
          type: 'get',
          url: _url,
          success: function(data){ 
            var issue=data.issue;

            // 進捗率
            done_ratio=issue['done_ratio'];
            var pid='p'+done_ratio;
            checkp(pid);

            // 消費時間
            total_spent_hours=issue['total_spent_hours'];
            // 推定時間
            total_estimated_hours=issue['total_estimated_hours'];

            var eh;

            $('#sh_time').html(total_spent_hours);
            if(total_estimated_hours==undefined){
              eh="";
              $('#lab_time').html('（消費時間）');
            }else{
              eh=total_estimated_hours;
              $('#eh_time').html('/'+eh);
              $('#lab_time').html('（消費時間/推定時間）');
            }


        }
  });
  
});
// 「課題」変更
  $("#select_pj").on("change",function(e){
　　			console.log(e);
  if($("#select_pj").val()==null)return;
  var selpj=$("#select_pj").val();
  var pjcd=selpj.split('_')[0];
  var wt=selpj.split('_')[1];
  _url='../Apps/getWorkType?wt='+wt;
  $.ajax({
        type: 'get',
        url: _url,
        success: function(data){
          $("#select_wt").empty();
          $("#select_wt").select2("val", ""); 
          var options = new Array();
          data=data.result;
          $(data).each(function (i, o) {
            options.push({
                  id: o.work_id,
                  text: o.work_cd+'_'+o.work_name
              });
          });
          $("#select_wt").select2({
              data: options
          })

        }

      });
  });

// 全角数字を半角数字に変換
$(".js-characters-change").blur(function(){
  charactersChange($(this));
});
charactersChange = function(ele){
  var val = ele.val();
  var han = val.replace(/[Ａ-Ｚａ-ｚ０-９]/g,function(s){return String.fromCharCode(s.charCodeAt(0)-0xFEE0)});

  if(val.match(/[Ａ-Ｚａ-ｚ０-９]/g)){
    $(ele).val(han);
    // $('#sh_time').html(Number($('#sh_time').text())+Number(ele.val()));
  }
  else if(val.match(/[0-9]/g)){
    // $('#sh_time').html(Number($('#sh_time').text())+Number(ele.val()));
  }
  else{
    ele.val('');
}
}
})



// ※※※※※※※※※※※※※※※※※※※                  ※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※
// ※※※※※※※※※※※※※※※※※※※　　共通関数       ※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※
// ※※※※※※※※※※※※※※※※※※※                  ※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※



// コントローラーの入力内容をクリア
function clearConValue(){
// コメント
$("#inputmemo").val('');
// 時間(Hour)
$("#inputtime").val('');
// チケット
$("#select_issue").select2("val", " ");
// 課題
$("#select_pj").select2("val", " "); 
// 作業
$("#select_wt").select2("val", " "); 
// 進捗
checkp('p0');
// 消耗時間
$('#eh_time').html('');
$('#sh_time').html('');
}  
// チケットありなし
function ischk(){
// チケットありなし
return $("#ticketsel1").is(":checked");
}
var _done;
// チェックにより進捗率を変更
function checkp(pid){
// $('#'+pid).attr("checked", true);
$('#prog-bar').attr('class','');
$('#prog-bar').addClass('progress-bar');
$('#prog-bar').addClass(pid);
_done=pid.split('p')[1];
// alert($('input[name="progress"]:checked').val());
}

// 画面各コントローラーの表示非表示
function conshow(){
$('#inputmemo').val('');
$('#inputtime').val('');
$('#sh_time').html('');
$('#eh_time').html('');
$('#lab_time').html('');
// チケットありの場合
if(ischk()){
  $('#tr_pj').hide();
  $('#tr_date').hide();
  $('#tr_wt').hide();

  $('#tr_issue').show();
  $('#tr_prog').show();
}else{
  $('#tr_issue').hide();
  $('#tr_prog').hide();

  $('#tr_pj').show();
  $('#tr_date').show();
  $('#tr_wt').show();
}
}

