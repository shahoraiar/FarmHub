import sys
import os
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../core")))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

