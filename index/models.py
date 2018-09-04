from django.db import models

# Create your models here.

class User(models.Model):
  uphone = models.CharField(max_length=11)
  upwd = models.CharField(max_length=30)
  uname = models.CharField(max_length=20,unique='True')
  uemail = models.EmailField()
  isActive = models.BooleanField(default='True')

class GoodsType(models.Model):
  title = models.CharField(max_length=40,verbose_name='标题')
  picture = models.ImageField(upload_to='static/upload/goodstype',verbose_name='图片')
  desc = models.TextField(verbose_name='描述')

  def to_dict(self):
    dic = {
      'title':self.title,
      'picture':self.picture.__str__(),
      'desc':self.desc
    }
    return dic

  def __str__(self):
    return self.title

  class Meta:
    verbose_name = '商品类型'
    verbose_name_plural = verbose_name

class Goods(models.Model):
  title = models.CharField(max_length=40,verbose_name='标题')
  price = models.DecimalField(max_digits=7,decimal_places=2,verbose_name='价格')
  spec = models.CharField(max_length=20)
  picture = models.ImageField(upload_to='static/upload/goods',verbose_name='图片')
  isActive = models.BooleanField(default=True,verbose_name='状态')
  # 增加对商品类型的引用(1(GoodsType):M(Goods))
  goodsType = models.ForeignKey(GoodsType,null=True)

  def __str__(self):
    return self.title

  class Meta:
    verbose_name = '商品'
    verbose_name_plural = verbose_name

class CartInfo(models.Model):
  ccount = models.IntegerField(verbose_name='购买数量')
  user = models.ForeignKey(User)
  good = models.ForeignKey(Goods)

  class Meta:
    verbose_name = '购物车'
    verbose_name_plural = verbose_name