"""Application entry point."""
from Applications.DashApp.dashindex import app


def main():
    app.run_server(host='0.0.0.0', port='5000', debug=True)


if __name__ == "__main__":
    main()
