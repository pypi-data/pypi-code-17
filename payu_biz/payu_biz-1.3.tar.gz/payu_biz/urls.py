try:
    from django.conf.urls import patterns, url
    urlpatterns = patterns('', 
        url(r'^payubiz-success/$','payu_biz.views.payu_success', name='payu_success'),
        url(r'^payubiz-failure/$', 'payu_biz.home.views.payu_failure', name='payu_failure'),
        url(r'^payubiz-cancel/$', 'payu_biz.views.payu_cancel', name='payu_cancel'),
        )

except:
    from django.conf.urls import url
    from payu_biz import views as payu_view
    urlpatterns = [
        url(r'^payubiz-success/$',payu_view.payu_success, name='payu_success'),
        url(r'^payubiz-failure/$', payu_view.payu_failure, name='payu_failure'),
        url(r'^payubiz-cancel/$', payu_view.payu_cancel, name='payu_cancel'),

    ]