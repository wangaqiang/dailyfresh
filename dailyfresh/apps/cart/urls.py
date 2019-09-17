from django.conf.urls import url
from cart.views import CartAddView

urlpatterns = [
    utl(r'^add', CartAddView.as_view(), name='add'), # 购物车记录添加
]
