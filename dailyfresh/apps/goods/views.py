from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from goods.models import GoodsType, IndexGoodsBanner, GoodsSKU, IndexPromotionBanner, IndexTypeGoodsBanner
from order.models import OrderGoods
from django_redis import get_redis_connection

# Create your views here.
class IndexView(View):
    '''首页'''
    def get(self, request):

        '''显示首页'''
        # 获取商品的种类信息
        types = GoodsType.objects.all()

        # 获取首页轮播商品信息
        goods_banners = IndexGoodsBanner.objects.all().order_by('index')

        # 获取首页促销活动信息
        promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

        # 获取首页分类商品展示信息
        for type1 in types: # GoodsType
            # 获取type种类首页分类商品的图片展示信息
            image_banners = IndexTypeGoodsBanner.objects.filter(type=type1, display_type=1).order_by('index')
            # 获取type种类首页分类商品的文字展示信息
            title_banners = IndexTypeGoodsBanner.objects.filter(type=type1, display_type=0).order_by('index')

            # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
            type1.image_banners = image_banners
            type1.title_banners = title_banners
            


        # 获取用户购物车中商品的数目
        user = request.user
        cart_count = 0
        if user.is_authenticated():
            # 用户已经登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%d'%user.id
            cart_count = conn.hlen(cart_key)

        # 组织模板上下文
        context = {'types':types,
                   'goods_banners':goods_banners,
                   'promotion_banners':promotion_banners,
                   'cart_count':cart_count}

        return render(request, 'index.html', context)

# /goods/商品id
class DetailView(View):
    '''详情页'''
    def get(self, request, goods_id):
        '''显示详情页'''
        try:
            sku = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在
            return redirect(reverse('goods:index'))

        # 获取商品的分类信息
        types = GoodsType.objects.all()

        # 获取商品的评论信息
        sku_orders = OrderGoods.objects.filter(sku=sku).exclude(comment='')

        # 获取新品信息
        new_skus = GoodsSKU.objects.filter(type=sku.type).order_by('-create_time')

        # 获取用户购物车中商品的数目
        user = request.user
        cart_count = 0
        if user.is_authenticated():
            # 用户已经登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%d'%user.id
            cart_count = conn.hlen(cart_key)
            
        # 组织模板上下文
        context = {'sku':sku,
                   'types':types,
                   'sku_orders':sku_orders,
                   'new_skus':new_skus,
                   'cart_count':cart_count}

        # 使用模板
        return render(request, 'detail.html', context)
