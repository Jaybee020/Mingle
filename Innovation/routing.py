from django.conf.urls import url
from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from channels.security.websocket import OriginValidator,AllowedHostsOriginValidator
from chat.consumers import ChatConsumer
from chat.views import chat
application=ProtocolTypeRouter(
    {
        'websocket':AllowedHostsOriginValidator(
            AuthMiddlewareStack(    
                URLRouter(
                    [
                        path('chat/<username>/',ChatConsumer)
                    ]

                )#getting which user is sending the request
            )#making sure that whatever host is doing the request will match the one in our settings.py
        )

    }
)