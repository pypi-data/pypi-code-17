from .base import Adapter


class DjangoModelAdapter(Adapter):
    model = None
    pk_field = 'pk'
    fk_fields = {}
    m2m_fields = {}
    related_fields = []

    def __init__(self, *args, **kwargs):
        assert self.model is not None, 'model attribute cannot be null'
        self.m2m_data = {}
        self.related_data = {}

    def insert(self, data):
        obj = self.model.objects.create(**data)
        return obj

    def update(self, instance, data):
        for k, v in data.items():
            setattr(instance, k, v)
            instance.save()

        return instance

    def process_fk_data(self, data):
        for key, fk_adater_class in self.fk_fields.items():
            if key in data:
                field_data = data[key]
                if field_data:
                    data[key] = fk_adater_class().upsert(data[key])

    def pick_m2m_data(self, data):
        for key, m2m_adater_class in self.m2m_fields.items():
            adapter = m2m_adater_class()
            if key in data:
                field_data = data.pop(key)
                self.m2m_data[key] = (adapter.upsert(item) for item in field_data)

    def save_m2m_data(self, instance):
        for field, value in self.m2m_data.items():
            m2m_field = getattr(instance, field)
            m2m_field.clear()
            m2m_field.add(*value)

    def get_instance(self, data):
        return self.model.objects.filter(pk=data[self.pk_field]).first()

    def upsert(self, data):
        instance = self.get_instance(data)

        self.pick_m2m_data(data)
        self.process_fk_data(data)
        self.before_upsert(data)
        try:
            instance = instance and self.update(instance, data) or self.insert(data)

            self.save_m2m_data(instance)
        except UnicodeEncodeError as e:
            print e
            pass

        return instance

    def finalize(self):
        pass

    def before_upsert(self, data):
        pass
