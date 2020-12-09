"""Application entry point."""
from app import app


def main():
    app.run_server(host='0.0.0.0', port='5000', debug=False)


if __name__ == "__main__":
    main()
