from main import app
from a2wsgi import ASGIMiddleware

# PythonAnywhere uses WSGI, but FastAPI is ASGI.
# This adapter makes them work together.
application = ASGIMiddleware(app)
