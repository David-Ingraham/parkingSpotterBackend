from .five_nearest import bp as five_nearest_bp

def register_routes(app):
    app.register_blueprint(five_nearest_bp)
