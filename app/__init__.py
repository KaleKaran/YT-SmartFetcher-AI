from flask import Flask
import os
from pathlib import Path
import shutil

def create_app():
    # Get the base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create the app
    app = Flask(__name__, 
                template_folder=os.path.join(base_dir, 'templates'),
                static_folder=os.path.join(base_dir, 'static'))
    app.secret_key = os.urandom(24)
    
    # Setup directories
    temp_dir = Path(os.path.join(base_dir, "temp_images"))
    try:
        shutil.rmtree(temp_dir)
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Warning: Could not delete temp_images - {e}")
    
    temp_dir.mkdir(exist_ok=True)
    
    # Create the images directory if it doesn't exist
    images_dir = os.path.join(base_dir, 'static', 'images')
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
    # Register template filters
    from app.utils.filters import format_content
    app.jinja_env.filters['format_content'] = format_content
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.video import video_bp
    from app.routes.document import document_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(video_bp)
    app.register_blueprint(document_bp)
    
    return app 