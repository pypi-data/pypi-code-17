from celery import task


@task
def save_product_page_visit(customer_id, product_id, variant_id=None):
    from pcart_customers.models import ProductPageVisit
    try:
        visit = ProductPageVisit.objects.get(customer_id=customer_id, product_id=product_id, variant_id=variant_id)
        visit.increase_visits()
    except ProductPageVisit.DoesNotExist:
        visit = ProductPageVisit(
            customer_id=customer_id,
            product_id=product_id,
            variant_id=variant_id,
        )
    visit.save()


# Run this task automatically every 1 hour
@task.periodic_task(run_every=60*60)
def clean_visits_history():
    from .utils import clean_visits_history
    clean_visits_history()
