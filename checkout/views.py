import json
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    TemplateView, View, ListView
)

from catalogo.models import Product
from .models import CartItem, Order

logger = logging.getLogger('checkout.views')


class CreateCartItemView(View):

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        logger.debug('Produto %s adicionado ao carrinho' % product)
        if self.request.session.session_key is None:
            self.request.session.save()
        cart_item, created = CartItem.objects.add_item(
            self.request.session.session_key, product
        )
        if created:
            message = 'Produto adicionado com sucesso'
        else:
            message = 'Produto atualizado com sucesso'
        if request.is_ajax():
            return HttpResponse(
                json.dumps({'message': message}), content_type='application/javascript'
            )
        messages.success(request, message)
        return redirect('checkout:cart_item')


class CartItemView(TemplateView):

    template_name = 'checkout/cart.html'

    def get_formset(self, clear=False):
        CartItemFormSet = modelformset_factory(
            CartItem, fields=('quantity',), can_delete=True, extra=0
        )
        session_key = self.request.session.session_key
        if session_key:
            if clear:
                formset = CartItemFormSet(
                    queryset=CartItem.objects.filter(cart_key=session_key)
                )
            else:
                formset = CartItemFormSet(
                    queryset=CartItem.objects.filter(cart_key=session_key),
                    data=self.request.POST or None
                )
        else:
            formset = CartItemFormSet(queryset=CartItem.objects.none())
        return formset

    def get_context_data(self, **kwargs):
        context = super(CartItemView, self).get_context_data(**kwargs)
        context['formset'] = self.get_formset()
        return context

    def post(self, request, *args, **kwargs):
        formset = self.get_formset()
        context = self.get_context_data(**kwargs)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Carrinho atualizado com sucesso')
            context['formset'] = self.get_formset(clear=True)
        return self.render_to_response(context)


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'checkout/checkout.html'

    def get(self, request, *args, **kwargs):
        session_key = request.session.session_key
        if session_key and CartItem.objects.filter(cart_key=session_key).exists():
            cart_items = CartItem.objects.filter(cart_key=session_key)
            order = Order.objects.create_order(
                user=request.user, cart_items=cart_items
            )
            cart_items.delete()
        else:
            messages.info(request, 'Não há itens no carrinho de compras')
            return redirect('checkout:cart_item')
        response = super(CheckoutView, self).get(request, *args, **kwargs)
        response.context_data['order'] = order
        return response


class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'checkout/order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


order_list = OrderListView.as_view()
checkout = CheckoutView.as_view()
create_cartitem = CreateCartItemView.as_view()
cart_item = CartItemView.as_view()
