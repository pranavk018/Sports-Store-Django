"""
URL configuration for projct project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from productapp import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('demo',views.demo),
    path('home',views.homePage),
    path('register', views.register),
    path('about', views.about),
    path('login', views.user_login),
    path('logout',views.user_logout),
    path('catfilter/<catval>',views.catfilter),
    # path('register', views.register),
    path('sort/<sv>', views.sort),
    path('range',views.range),
    path('contact',views.contact),
    path('details/<pid>',views.showDetails),
    path('addtocart/<pid>',views.addToCart),
    path('mycart',views.showMyCart),
    path('updateqty/<incr>/<cid>', views.updateQuantity),
    path('deletecart/<cid>',views.deleteCart),
    path('placeorder',views.placeOrder),
    path('makepayment',views.makepayment),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
