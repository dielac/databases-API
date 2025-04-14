from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow




# --------------------------Initialize Flask app----------------------------------------
app = Flask(__name__)




# -------------------------------MySQL Database -----------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:rootroot@localhost/ecommerce_api_2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




# -------------------------------Initialize extensions-----------------------------------------
db = SQLAlchemy(app)
ma = Marshmallow(app)




#---------------------------- Import routes AFTER app and db are created---------------------------
import routes



#--------------------------Create tables in the database--------------------------------------------
with app.app_context():
    db.create_all()



# ------------------------Start the Flask app--------------------------------
if __name__ == '__main__':
    app.run(debug=True)
