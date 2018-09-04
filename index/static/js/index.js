$(function () {
  //网页加载时要运行的操作
  loadGoods();
  check_login();
});

//异步加载商品类型以及商品列表
function loadGoods(){
  $.get('/all_type_goods/',function(data){
    var show = '';
    $.each(data,function (i,obj) {
      var html = '';
      html += "<div class='item'>";
      var jsonType = JSON.parse(obj.type);
      html += "<p class='title'>";
      html += "<a href='#'>更多</a>";
      html += "<img src='/"+jsonType.picture+"'>";
      html += "</p>";
      html += '<ul>';
      var jsonGoods=JSON.parse(obj.goods);
      $.each(jsonGoods,function (j,good) {
        html += "<li ";
        if((j+1)%5==0){
          html += "class='no-margin'";
        }
        html += "><p>";
        html += '<img src="/'+ good.fields.picture +'">';
        html += "</p>";
        html += "<div class='content'>";
        html += '<a href="javascript:add_cart('+ good.pk +');" class="cart">';
        html += '<img src="/static/images/cart.png"></a>';
        html += '<p>'+ good.fields.title +'</p>';
        html += '<span>&yen;'+good.fields.price+'/'+good.fields.spec+'</span>';
        html += '</div></li>';
      });
      html += "</ul>";
      html += "</div>";
      show += html;
    });
    $('#main').html(show);
  },'json');
}
/**
 * 异步的验证登录状态
 * 如果已登录,显示:欢迎 uname  退出
 * 如果未登录,显示:[登录][注册有惊喜]
 * */
function check_login(){
  $.get('/check_login/',function(data){
    var html="";
    //判断是否有登录信息
    if(data.loginStatus == 0){
      html+="<a href='/login/'>[登录]</a>";
      html+="<a href='/register/'>[注册有惊喜]</a>";
    }else{
      html+="欢迎:"+data.uname;
      html+="&nbsp;&nbsp;&nbsp;&nbsp;";
      html+="<a href='/logout/'>[退出]</a>";
    }
    $("#login-info").html(html);
  },'json');
}
function add_cart(good_id) {
  $.get('/check_login/',function (data) {
    if(data.loginStatus == 0){
      alert('请先登录...');
    }else{
      $.post('/add_cart/',{'good_id':good_id,'csrfmiddlewaretoken':$.cookie('csrftoken')},function (data) {
        if(data.status == 1){
          alert('添加购物车成功');
        }else{
          alert('添加购物车失败');
        }
      },'json');
    }
  },'json');
}
