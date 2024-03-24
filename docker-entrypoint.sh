echo "Run database makemigrations"
ENV_FOR_DYNACONF=production python manage.py makemigrations

echo "Run database migrations"
ENV_FOR_DYNACONF=production python manage.py migrate


echo "Creating admin..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser('octoAdmin', 'octoAdmin@octoxlabs.com.tr', '159951', first_name='octoAdmin')" | ENV_FOR_DYNACONF=production python manage.py shell

echo "Starting application server"
ENV_FOR_DYNACONF=production python manage.py runserver 0.0.0.0:8000