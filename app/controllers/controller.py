from flask import redirect, url_for
from app.config import app
from app.controllers.api import v1

# ================= BLUEPRINTS ==================
app.register_blueprint(v1)
# ==================== PAGES ====================

@app.route('/')
def start_page():
    pass
