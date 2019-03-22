from bank import app

# FOR PRODUCTION: DISABLE DEBUGGING
if __name__ == '__main__':
    app.run("0.0.0.0", threaded=True, debug=True)

# Threaded automatically handles requests on different threads on the system
# This improves the performance when many users are trying to log in or make transactions in the system at once
