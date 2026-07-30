from app import app

if __name__ == "__main__":
    host = '0.0.0.0'  # Bind to all available network interfaces
    port = 5500  # Choose a port number
    app.run(host=host, port=port)