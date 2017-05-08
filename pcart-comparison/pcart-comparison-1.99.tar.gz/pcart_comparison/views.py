from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from pcart_customers.utils import get_customer
from .models import ComparisonProduct


def _add_item_to_comparison(customer, site, item_id, item_type='product'):
    from pcart_catalog.models import Product, ProductVariant
    variant = product = None
    if item_type == 'variant':
        variant = ProductVariant.objects.get(pk=item_id)
        product = variant.product
    elif item_type == 'product':
        product = Product.objects.get(pk=item_id)

    if not ComparisonProduct.objects.filter(
            customer=customer, product=product, variant=variant, site=site).exists():
        ComparisonProduct.objects.create(
            customer=customer,
            product=product,
            variant=variant,
            site=site,
        )


def compare_products(request, template_name='customers/comparison.html'):
    from pcart_catalog.models import ProductType
    site = get_current_site(request)
    user = request.user
    customer = get_customer(request)

    if 'view' in request.GET:
        template_name = settings.PCART_COMPARISON_TEMPLATES[request.GET['view']]

    if request.method == 'POST':
        if 'add-item' in request.POST:
            item_id = request.POST.get('item-id')
            item_type = request.POST.get('item-type')
            if item_id and item_type:
                _add_item_to_comparison(customer, site, item_id, item_type)
                if not request.is_ajax():
                    return redirect(
                        reverse(
                            'pcart_customers:customer-profile-section',
                            args=('comparison',)
                        ))
        else:
            for k in request.POST:
                if k.startswith('item-remove-'):
                    _id = k[len('item-remove-'):]
                    ComparisonProduct.objects.filter(pk=_id, customer=customer, site=site).delete()
            if not request.is_ajax():
                return redirect(
                    reverse(
                        'pcart_customers:customer-profile-section',
                        args=('comparison',)
                    ))

    comparisons = ComparisonProduct.objects.filter(customer=customer, site=site).order_by('added')
    product_types = ProductType.objects.filter(id__in=[item.product.product_type_id for item in comparisons])

    context = {
        'user': user,
        'customer': customer,
        'customer_menu': settings.PCART_CUSTOMER_PROFILE_SECTIONS,
        'comparisons': comparisons,
        'product_types': product_types,
    }
    return render(request, template_name, context)


@csrf_exempt
@require_http_methods(['POST'])
def add_product(request):
    site = get_current_site(request)
    if request.user.is_anonymous():
        return HttpResponseForbidden('Anonymous user')
    customer = get_customer(request)

    item_id = request.POST.get('item-id')
    item_type = request.POST.get('item-type')

    if item_id and item_type:
        _add_item_to_comparison(customer, site, item_id, item_type)

    if not request.is_ajax() and 'next' in request.POST:
        return redirect(request.POST['next'])
    return HttpResponse('OK')
