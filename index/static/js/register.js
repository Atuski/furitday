$(function(){
  //为#formReg绑定submit事件
  $('#formReg').submit(function(){
    if($('#upwd').val() != $('#upwd2').val()){
      alert('两次密码不一致,请重新输入');
      return false;
    }
    return true;
  });
  $('#uphone').blur(function () {
    $.ajax({
      'url':'/checkphone/',
      'type':'get',
      'data':'uphone='+$(this).val(),
      'dataType':'json',
      'success':function(data){
        if(data.status == 0){
          $('#uphone-show').html('通过');
        }else{
          $('#uphone-show').html('该手机号已注册');
          $('#formReg').submit(function(){
              return false;
          });
        }
      }
    });
  });
});