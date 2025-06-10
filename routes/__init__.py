from routes.five_nearest import bp as five_nearest_bp
from routes.watch_camera import bp as watch_camera_bp
from routes.direct_camera_search import bp as direct_camera_search_bp

def register_routes(app):
    app.register_blueprint(five_nearest_bp)
    app.register_blueprint(watch_camera_bp)
    app.register_blueprint(direct_camera_search_bp)
