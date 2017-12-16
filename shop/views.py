from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Item
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
    initial = {'name': item.name, 'amount': item.amount}

    if request.method == 'POST':
        form = OrderForm(request.POST, initial=initial)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.item = item
            order.save()
            return redirect('profile')
    else:
        form = OrderForm(initial=initial)

    return render(request, 'shop/order_form.html', {
        'form': form,
        'iamport_shop_id': 'iamport',
    })

