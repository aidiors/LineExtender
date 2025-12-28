from app_config import parse_arguments
from application import Application

if __name__ == "__main__":
    config = parse_arguments()
    app = Application(config)
    app.run()
