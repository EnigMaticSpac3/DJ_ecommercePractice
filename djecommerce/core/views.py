from django.http import request
from django.shortcuts import redirect, render, get_object_or_404
from .models import Item, Order, OrderItem
from django.utils import timezone
#special imports
from django.views.generic import ListView, DetailView, View
from django.contrib import messages

# Create your views here.

class CheckoutView(View):
    def get(self, *args, **kwargs):
        context = {
            'title': "Checkout"
        }
        return render(self.request, "checkout.html", context)

# class HomeView(ListView):
#     model = Item
#     paginate_by = 10
#     template_name = "home.html"
   
class HomeView(ListView):
    model = Item 
    template_name = "home.html"
    
# def home(request):
#     context = {
#         'items': Item.objects.all(),
#         'title': "Ecommerce"
#     }
#     return render(request, "home.html", context)

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

def add_to_cart(request, slug):
    item         = get_object_or_404(Item, slug=slug)
    order_item, created   = OrderItem.objects.get_or_create(
        item=item,
        user = request.user,
        ordered = False
    )
    order_qs     = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'This item quantity has been updated.')
        else:
            order.items.add(order_item)
            messages.info(request, 'This item has been added to your cart.')
    else:
        ordered_date  = timezone.now()
        order         = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'This item has been added to your cart.')
    
    return redirect("core:product", slug=slug)


def remove_from_cart(request, slug):
    item       = get_object_or_404(Item, slug=slug)
    order_qs   =   Order.objects.filter(
        user = request.user,
        ordered = False
    )

    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.get_or_create(
                item=item,
                user = request.user,
                ordered = False
            )[0]
            order.items.remove(order_item)
            messages.info(request, 'This item has been removed from your cart.')
            return redirect("core:product", slug=slug)

        else:
            # add message saying > the order doesnt contain the item
            messages.info(request, 'This item is not in your cart.')
            return redirect("core:product", slug=slug)

    else:
        # add message saying > the user doesnt have an order.
        messages.info(request, 'You do not have an active order.')
        return redirect("core:product", slug=slug)