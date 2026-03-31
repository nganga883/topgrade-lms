from django.contrib.auth import get_user_model
from django.db.utils import OperationalError

def create_superuser():
    User = get_user_model()
    
    try:
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@example.com",
                password="StrongPassword123"
            )
            print("✅ Superuser created automatically")
    except OperationalError:
        # database not ready yet
        pass