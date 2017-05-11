from django.conf import settings
from django.core.mail import send_mail
from django.template import Template, loader


def send_simple_email(recip, subject, context, template, from_email=None,
                      is_template_file=True, fail_silently=False):
    if is_template_file:
        # Load template from actual file in templates dir
        msg_template = loader.get_template(template)
    else:
        # Template is a string, passed directly
        msg_template = Template(template)

    msg_dict = {
        'from_email': from_email or settings.DEFAULT_FROM_EMAIL,
        'message': msg_template.render(context),
        'recipient_list': isinstance(recip, list) and recip or [recip],
        'subject': subject,
    }
    send_mail(fail_silently=fail_silently, **msg_dict)
