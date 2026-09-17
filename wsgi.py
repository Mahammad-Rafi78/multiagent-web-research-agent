from a2wsgi import ASGIMiddleware

from ui_server import app as asgi_app

application = ASGIMiddleware(asgi_app)
