from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Item, Order
from .forms import OrderForm


class ItemListView(ListView):
    model = Item

    def get_queryset(self):
        qs = super().get_queryset()
        self.q = self.request.GET.get('q', '')
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.q
        return context

index = ItemListView.as_view()


@login_required
def order_new(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    order = Order.objects.create(user=request.user, item=item, name=item.name, amount=item.amount)
    return redirect('shop:order_pay', item_id, str(order.merchant_uid))


@login_required
def order_pay(request, item_id, merchant_uid):
    order = get_object_or_404(Order, user=request.user, merchant_uid=merchant_uid, status='ready')

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = OrderForm(instance=order)

    return render(request, 'shop/pay_form.html', {
        'form': form,
    })

