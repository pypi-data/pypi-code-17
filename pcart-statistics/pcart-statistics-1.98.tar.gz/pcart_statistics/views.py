from django.shortcuts import render, redirect
# from django.conf import settings
# from django.urls import reverse
from pcart_customers.utils import get_customer
from .models import ProductPageVisit


def visited_products(request, template_name='customers/includes/visited_products.html'):
    user = request.user
    customer = get_customer(request)

    history = ProductPageVisit.objects.filter(customer=customer).order_by('-changed')
    context = {
        'user': user,
        'customer': customer,
        'history': history,
    }
    return render(request, template_name, context)
