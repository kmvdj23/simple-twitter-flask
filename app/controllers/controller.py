from flask import redirect, url_for
from app.config import app
from app.controllers.api import api

# ================= BLUEPRINTS ==================
app.register_blueprint(api)
# ==================== PAGES ====================

@app.route('/')
def start_page():
    pass
