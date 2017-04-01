import json

from django.core.serializers.json import DjangoJSONEncoder
from django.dispatch import receiver

from ..exporter import BaseExporter
from ..signals import register_data_exporters


class JSONExporter(BaseExporter):
    identifier = 'json'
    verbose_name = 'JSON'

    def render(self, form_data):
        jo = {
            'event': {
                'name': str(self.event.name),
                'slug': self.event.slug,
                'organizer': {
                    'name': str(self.event.organizer.name),
                    'slug': self.event.organizer.slug
                },
                'categories': [
                    {
                        'id': category.id,
                        'name': str(category.name)
                    } for category in self.event.categories.all()
                ],
                'items': [
                    {
                        'id': item.id,
                        'name': str(item.name),
                        'category': item.category_id,
                        'price': item.default_price,
                        'tax_rate': item.tax_rate,
                        'admission': item.admission,
                        'active': item.active,
                        'variations': [
                            {
                                'id': variation.id,
                                'active': variation.active,
                                'price': variation.default_price if variation.default_price is not None else
                                item.default_price,
                                'name': str(variation)
                            } for variation in item.variations.all()
                        ]
                    } for item in self.event.items.all().prefetch_related('variations')
                ],
                'questions': [
                    {
                        'id': question.id,
                        'question': str(question.question),
                        'type': question.type
                    } for question in self.event.questions.all()
                ],
                'orders': [
                    {
                        'code': order.code,
                        'status': order.status,
                        'user': order.email,
                        'datetime': order.datetime,
                        'payment_fee': order.payment_fee,
                        'total': order.total,
                        'positions': [
                            {
                                'id': position.id,
                                'item': position.item_id,
                                'variation': position.variation_id,
                                'price': position.price,
                                'attendee_name': position.attendee_name,
                                'secret': position.secret,
                                'answers': [
                                    {
                                        'question': answer.question_id,
                                        'answer': answer.answer
                                    } for answer in position.answers.all()
                                ]
                            } for position in order.positions.all()
                        ]
                    } for order in
                    self.event.orders.all().prefetch_related('positions', 'positions__answers')
                ],
                'quotas': [
                    {
                        'id': quota.id,
                        'size': quota.size,
                        'items': [item.id for item in quota.items.all()],
                        'variations': [variation.id for variation in quota.variations.all()],
                    } for quota in self.event.quotas.all().prefetch_related('items', 'variations')
                ]
            }
        }

        return 'pretixdata.json', 'application/json', json.dumps(jo, cls=DjangoJSONEncoder)


@receiver(register_data_exporters, dispatch_uid="exporter_json")
def register_json_export(sender, **kwargs):
    return JSONExporter
