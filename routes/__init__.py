from .five_nearest import bp as five_nearest_bp
from .watch_add import bp as watch_add_bp  

def register_routes(app):
    app.register_blueprint(five_nearest_bp)
    app.register_blueprint(watch_add_bp)   
