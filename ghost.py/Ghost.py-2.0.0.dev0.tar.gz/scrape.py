import time
from ghost import Ghost
ghost = Ghost()

with ghost.start(viewport_size=(1300, 800)) as session:
    page, extra_resources = session.open(
        "https://app.omixy-staging.com/auth/login"
    )
    session.set_field_value('[name=email]', 'active@domain.tld')
    session.set_field_value('[name=password]', 'secret')
    session.click('[type=submit]', expect_loading=True)
    session.open("http://app.omixy-staging.com/patient/health-summary/system/digestive-system")
    time.sleep(1)
    session.print_to_pdf('test.pdf', zoom_factor=1)
