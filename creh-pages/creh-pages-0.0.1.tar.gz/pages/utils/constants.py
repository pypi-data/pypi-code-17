from django.conf import settings

SLIDER_SIZES = [
    (100, 100),
    (300, 300),
]

PAGE_SLIDER_SIZES = getattr(settings, 'SLIDE_SIZES', SLIDER_SIZES)
PAGE_SLIDER_FORMAT = 'PNG'
PAGE_SLIDER_OPTIONS = {
    'quality': 70
}

SLIDER_TYPE_CONTENT = [
    'TEXT',
    'BUTTON',
]