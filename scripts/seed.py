import os
import sys
import django
from pathlib import Path

# Add project root to system path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from core.models import Product

def run_seed():
    print("Seeding data...")
    if not Product.objects.exists():
        Product.objects.create(name="Sample Product 1", description="Description for product 1", price=10.99, stock=100)
        Product.objects.create(name="Sample Product 2", description="Description for product 2", price=25.50, stock=50)
        print("Created sample products.")
    else:
        print("Products already exist.")

if __name__ == '__main__':
    run_seed()
