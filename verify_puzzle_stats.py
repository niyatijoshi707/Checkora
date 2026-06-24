import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from game.models import PuzzleStats
from django.urls import reverse

User = get_user_model()

# Create a test user
user, created = User.objects.get_or_create(username='puzzle_tester', email='test@example.com')
if created:
    user.set_password('testpassword123')
    user.save()

# Update their PuzzleStats manually
stats, _ = PuzzleStats.objects.get_or_create(user=user)
stats.current_streak = 5
stats.best_streak = 12
stats.save()

# Use Django test client to hit the endpoint
client = Client()
client.force_login(user)

response = client.get(reverse('puzzle_stats'))

print(f"Status Code: {response.status_code}")
try:
    print(f"Response JSON: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Failed to parse JSON. Raw content: {response.content}")

if response.status_code == 200 and response.json().get('streak') == 5 and response.json().get('longest_streak') == 12:
    print("SUCCESS: Endpoint returned actual database values!")
else:
    print("ERROR: Endpoint did not return expected values.")
