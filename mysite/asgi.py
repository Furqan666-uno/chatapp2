# import os
# import django
# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
# django.setup()  # This must be called before importing routing or models

# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# import chatapp.routing

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(  # Optional: use AuthMiddlewareStack for user session handling
#         URLRouter(chatapp.routing.websocket_urlpatterns)
#     ),
# })
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

# ✅ Set this BEFORE importing models or anything Django-related
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()  

import chatapp.routing  # ← Safe to import now, after setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(URLRouter(chatapp.routing.websocket_urlpatterns)),
})

