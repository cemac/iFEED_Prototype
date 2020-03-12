"""Application entry point."""
from Applications.DashApp.dashindex import app


def main():
    app.run_server(host='0.0.0.0', debug=True)


if __name__ == "__main__":
    main()
