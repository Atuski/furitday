from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from .forms import *
import json

# Create your views here.
def login_views(request):
  if request.method == 'POST':
    uphone = request.POST['uphone']
    upwd = request.POST['upwd']
    uList = User.objects.filter(uphone=uphone,upwd=upwd)
    if uList:
      url = request.COOKIES['url']
      resp = HttpResponseRedirect(url)
      if 'url' in request.COOKIES:
        resp.delete_cookie('url')
      request.session['uphone'] = uphone
      request.session['id'] = uList[0].id
      if 'isSaved' in request.POST:
        expires = 60*60*24*365
        resp.set_cookie('id',uList[0].id,expires)
        resp.set_cookie('uphone',uphone,expires)
      return resp
    else:
      form = LoginForm()
      return render(request,'login.html',locals())
  else:
    url = request.META.get('HTTP_REFERER','/')
    if 'uphone' in request.session and 'id' in request.session:
      resp = HttpResponseRedirect(url)
      return resp
    elif 'uphone' in request.COOKIES and 'id' in request.COOKIES:
      if User.objects.filter(uphone = request.COOKIES['uphone'],id = request.COOKIES['id']):
        resp = HttpResponseRedirect(url)
        request.session['uphone'] = request.COOKIES['uphone']
        request.session['id'] = request.COOKIES['id']
        return resp
    else:
      form = LoginForm()
      resp = render(request,'login.html',locals())
      resp.set_cookie('url',url)
      return resp
  # if request.method == 'GET':
  #   if 'uphone' in request.session:
  #     return HttpResponse('欢迎:'+request.session['uphone'])
  #   if 'uphone' in request.COOKIES and 'id' in request.COOKIES:
  #     if User.objects.filter(uphone = request.COOKIES['uphone'],id = request.COOKIES['id']):
  #       request.session['uphone'] = request.COOKIES['uphone']
  #       request.session['id'] = request.COOKIES['id']
  #       return HttpResponse('欢迎:'+request.COOKIES['uphone'])
  #   form = LoginForm()
  #   return render(request,'login.html',locals())
  # else:
  #   uList = User.objects.filter(uphone = request.POST['uphone'],upwd = request.POST['upwd'])
  #   if uList:
  #     request.session['uphone'] = request.POST['uphone']
  #     request.session['id'] = uList[0].id
  #     resp = HttpResponse('欢迎:'+request.POST['uphone'])
  #     if 'isSaved' in request.POST:
  #       expires = 60*60*24*365
  #       resp.set_cookie('id',uList[0].id,expires)
  #       resp.set_cookie('uphone',request.POST['uphone'],expires)
  #     return resp
  #   else:
  #     form = LoginForm()
  #     return render(request,'login.html',locals())

def register_views(request):
  if request.method == 'GET':
    return render(request,'register.html')
  elif User.objects.filter(uphone = request.POST['uphone']):
    uname = request.POST['uname']
    uemail = request.POST['uemail']
    return render(request,'register.html',{'errMsg':'手机号码已经存在','uname':uname,'uemail':uemail})
  else:
    uphone = request.POST['uphone']
    upwd = request.POST['upwd']
    uname = request.POST['uname']
    uemail = request.POST['uemail']
    User.objects.create(uphone=uphone,upwd=upwd,uname=uname,uemail=uemail)
    return HttpResponse('注册成功!!')

def checkphone_views(request):
  uphone = request.GET['uphone']
  if User.objects.filter(uphone=uphone):
    data = json.dumps({'status':1})
  else:
    data = json.dumps({'status': 0})
  return HttpResponse(data)

def index_views(request):
  return render(request,'index.html')

def all_type_goods_views(request):
  #大列表:承装所有的类型和商品
  all_list=[]
  #查询所有的类型
  types = GoodsType.objects.all()
  #循环遍历types,得到每一个type以及对应的商品们
  for type in types:
    #将type序列化成json字符串
    type_json = json.dumps(type.to_dict())
    #获取type下的前5个产品
    goods_list = type.goods_set.order_by('-id')[0:5]
    # 将goods_list序列化成json字符串
    goods_list_json = serializers.serialize('json',goods_list)
    dic = {
      'type':type_json,
      'goods':goods_list_json
    }
    all_list.append(dic)
  all_list_json = json.dumps(all_list)
  return HttpResponse(all_list_json)

def logout_views(request):
  url = request.META.get('HTTP_REFERER','/')
  resp = HttpResponseRedirect(url)
  if 'uphone' in request.session and 'id' in request.session:
    del request.session['uphone']
    del request.session['id']
  if 'uphone' in request.COOKIES and 'id' in request.COOKIES:
    resp.delete_cookie('uphone')
    resp.delete_cookie('id')
  return resp

# 验证用户是否处于登录状态
def check_login_views(request):
    #验证session中是否包含登录信息
    if 'id' in request.session and 'uphone' in request.session:
        #已经处于登录状态
        loginStatus = 1
        #通过session中的id获取uname
        id=request.session.get('id')
        uname=User.objects.get(id=id).uname
        dic = {
            "loginStatus":loginStatus,
            "uname":uname
        }
        return HttpResponse(json.dumps(dic))
    else:
        # session 中没有登录信息
        # 查询COOKIES中是否包含登录信息
        if 'id' in request.COOKIES and 'uphone' in request.COOKIES:
            user_id=request.COOKIES['id']
            uphone = request.COOKIES['uphone']
            # 将user_id和uphone 保存进 session
            request.session['id']=user_id
            request.session['uphone']=uphone
            # 查询uname的值响应给客户端
            uname=User.objects.get(id=user_id).uname
            loginStatus = 1
            dic={
                "loginStatus":loginStatus,
                "uname":uname
            }
            return HttpResponse(json.dumps(dic))
        else:
            # session 和 cookies中均没有登录信息
            dic = {
                "loginStatus":0
            }
            return HttpResponse(json.dumps(dic))

def add_cart_views(request):
  user_id = request.session['id']
  good_id = request.GET['good_id']
  uList = CartInfo.objects.filter(user_id = user_id,good_id=good_id)
  if uList:
    cartinfo = uList[0]
    cartinfo.ccount = cartinfo.ccount + 1
    cartinfo.save()
    dic = {
      'status':1,
      'statusText':'更新数量成功'
    }
    return HttpResponse(json.dumps(dic))
  else:
    CartInfo.objects.create(good_id=good_id,user_id=user_id,ccount=1)
    dic = {
      'status': 1,
      'statusText': '添加购物车量成功'
    }
    return HttpResponse(json.dumps(dic))
