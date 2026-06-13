import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()

# Run migrations programmatically in production/serverless environment
from django.core.management import call_command  # noqa: E402
try:
    call_command('migrate', interactive=False)
except Exception as e:
    print(f"Failed to run migrations: {e}")
