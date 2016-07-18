# coding: utf-8
from django.shortcuts import render, redirect
from product.models import Category, Keyword, Product
from django.core.paginator import Paginator

# Create your views here.
# 添加产品
# request/response
def add(request):
    if request.method == 'POST':
        post = request.POST
        # 创建对象并保存到数据库
        product = Product.objects.create(name=post.get('product_name'),
                               spec=post.get('product_spec'),
                               cate_id=post.get('product_cate'),
                               stock=post.get('product_stock'),
                               price=post.get('product_price'),
                               desc=post.get('product_desc'))
        # 多对多的保存必须单独处理
        for key_id in post.getlist('product_key'):
            product.key.add(key_id)
        return redirect('list')
    categorys = Category.objects.all()
    keywords = Keyword.objects.all()
    return render(request, 'product/add.html', locals())

# 修改产品
def update(request, id):
    if request.method == 'POST':
        post = request.POST
        # 先得到要修改的对象
        product = Product.objects.get(pk=id)
        product.name=post.get('product_name')
        product.spec=post.get('product_spec')
        product.cate_id=post.get('product_cate')
        product.stock=post.get('product_stock')
        product.price=post.get('product_price')
        product.desc=post.get('product_desc')
        product.save()
        # 多对多的保存必须单独处理
        for key_id in post.getlist('product_key'):
            key = Keyword.objects.get(pk=key_id)
            if key not in product.key.all():
                product.key.add(key)
        for key in product.key.all():
            if str(key.id) not in post.getlist('product_key'):
                product.key.remove(key)
        return redirect('list')
    product = Product.objects.get(pk=id)
    categorys = Category.objects.all()
    keywords = Keyword.objects.all()
    return render(request, 'product/update.html', locals())

# 删除产品
def delete(request, id):
    # 先得到要删除的对象
    product = Product.objects.get(pk=id)
    product.delete()
    return redirect('list')

# 产品列表
def list(request):
    products = Product.objects.order_by('-id')
    paginator = Paginator(products, 1)
    try:
        page = int(request.GET.get('page'))
        products = paginator.page(page)
    except:
        products = paginator.page(1)
    return render(request, 'product/list.html', locals())