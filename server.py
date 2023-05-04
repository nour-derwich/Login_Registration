from flask_app import app

#! Don't forget to import the controllers
from flask_app.controllers import user


if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True)    # Run the app in debug mode.