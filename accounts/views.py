from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shop.models import Order


@login_required
def profile(request):
    order_list = Order.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {
        'order_list': order_list,
    })

