
def product_page_visit_listener(sender, **kwargs):
    from .tasks import save_product_page_visit
    save_product_page_visit.delay(
        customer_id=kwargs.get('customer_id'),
        product_id=kwargs.get('product_id'),
        variant_id=kwargs.get('variant_id'),
    )
