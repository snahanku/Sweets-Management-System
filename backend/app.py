
from flask import Flask, jsonify , request 
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager , create_access_token , jwt_required , get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import os


db = SQLAlchemy()  # Intial components for initializing database

jwt = JWTManager()




BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'sweet_shop.db')

# Models are defined  such as User Details , Sweet #
class User_Details(db.Model):
    __tablename__ = "userdetails"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash =db.Column(db.String(100) , nullable= False)
    role = db.Column(db.String(10), nullable=False, default='user')

    def set_password(self , password):
        self.password_hash = generate_password_hash(password)

    def check_password(self , password):
        
        return check_password_hash(self.password_hash , password)
    


    def to_dict(self):
        return {
            "id" : self.id,
             "user-name" :self.username
        }

  

class Sweet(db.Model):
    __tablename__ = "sweets"
    id = db.Column(db.Integer , primary_key =True)
    name= db.Column(db.String(100) , unique = True , nullable = False)
    category =db.Column(db.String(100)  , nullable = False)
    price = db.Column(db.Float , nullable=False)
    quantity = db.Column(db.Integer , nullable = False , default=0)

    def convert_to_dict(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'category' : self.category,
            'price' : round(self.price , 2),
            'quantity' : self.quantity
        }


# 3. Define the Application Factory
def create_app(test_config=None):
    app = Flask(__name__)
    
    # ... (Your existing app.config.from_mapping setup) ...
    app.config.from_mapping(
        SECRET_KEY='dev', 
        JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY", "3e4f7b2c5d1a9e8f0a7b4c6d3e2f1a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f"),
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{DB_PATH}', 
        SQLALCHEMY_TRACK_MODIFICATIONS=False, 
    )

    if test_config:
        app.config.from_mapping(test_config)

    db.init_app(app)
    jwt.init_app(app)
    

    @app.route("/")
    def home():
        return "Hello, World!"




##### Auth ####

    @app.route("/auth/register" , methods=['POST'])  #route to register

    def register_user():
        data = request.json 
        username = data.get("username") # retrieving user's username
        password= data.get("password")  # retrieving user's password

        if not username or not password: # check if both the fields(username , password) are blank
            return jsonify(
                {"message" : "Username and password are required"}
            )
        

        if User_Details.query.filter_by(username= username).first() :   ### check for already existing user in the database
            return jsonify(
                {
                    "message" : "user already exisit"
                }
            )
        
        new_user = User_Details(username=username) # if no above  cases , then assigning username value .
        new_user.set_password(password)            # and set password using set password method.
        db.session.add(new_user)                   # adding new user to the db.
        db.session.commit()                        # commit the changes .


        return jsonify(
            {
                "message": "user registered successfully",
                "user-details":new_user.to_dict()  # returning  user credentials in a jsonifed way .
            }
        )


    @app.route("/auth/login" , methods=['POST'])
    def login_user():
        data = request.json  
        username = data.get("username") # retrieving user's username
        password= data.get("password")  # retrieving user's password

        if not username or not password:
            return jsonify({
                "message" : "username and password required"  # check if both the fields(username , password) are blank.
            })
        

        user =  User_Details.query.filter_by(username= username).first()  #If data exist  retrieve  user data from the database.
            
        
        if user and user.check_password(password):   #  validity check for user and  user password
                                                     #if valid , it generate an access token
            access_token = create_access_token(identity= str(user.id))

            return jsonify({               # return user login status , accesstoken and user id
            "message": "Login successful",
            "access_token": access_token,
            "user_id": user.id
        }), 200

        else:                                       #if not valid , returns  Invalid Credentials as response.
            return jsonify(
                {
                    "message" :"Invalid credentials"
                }
            ) , 401




    

##### sweet-Management  ######



    @app.route("/api/add-sweets" , methods =['POST'])   ####  Route to  add sweets in Database
    @jwt_required() # jwt authenication , jwt authenticated users can access this route by default it is protected
    def add_sweets():

        data = request.json

        req_attributes = ['name' , 'category' , 'price' , 'quantity']
        if not all([ field in data for field in req_attributes]): #check  for all the fields that exist or not
           return jsonify({"message":"missing required fields"})   #if feilds dont exisit then missing   required fields response
        
        #### Adding a fix for price validation ####
        try:
        # Validate Price
          price = float(data['price']) 
          if price <= 0:
            return jsonify(message="Price must be a positive number"), 400
        except (ValueError, TypeError):
        # This block catches non-numeric input (like "not_a_number")
          return jsonify(message="Price must be a valid number"), 400

        try:
        # Validate Quantity
           quantity = int(data['quantity'])
           if quantity < 0:
             return jsonify(message="Quantity cannot be negative"), 400
        except (ValueError, TypeError):
        # This block catches non-integer input
          return jsonify(message="Quantity must be a whole number"), 400
        #####



        try:
            ####### after checking , assigning all the field valuse to the database
            new_sweet = Sweet(              
                name=data['name'],
                category=data['category'],
                # Ensure price and quantity are correctly typed before insertion
                price=float(data['price']),
                quantity=int(data['quantity'])
            )
        except ValueError: # catch Price and Quantity errors
            return jsonify({
                "messaage" : "Price must be Number(float) and Quantity must be Integer"
            })
        db.session.add(new_sweet)
        db.session.commit()

        return jsonify( { "mesaage" : "Product added successfully" ,
          "Sweet-details" : new_sweet.convert_to_dict()}) , 201
    
    
    @app.route("/api/get_all_sweets" , methods=['GET']) # Route  to list all sweet details from database
    @jwt_required()
    def get_all_sweets():

        sweets= Sweet.query.all() # Querying all sweet objects

        if not sweets: # check for if database is empty

            return jsonify({
             "message" : "No sweets currently in inventory.",
             "sweets": []
         }) , 200
        

        sweet_list =[]
        for sweet in sweets:
            sweet_list.append(sweet.convert_to_dict()) ## Appending all dictionary converted sweets in to empty list
        
        


        return jsonify(sweet_list) , 200 # returning  sweet it as json reponse.



    @app.route("/api/sweets/<int:sweet_id>", methods=['PUT'])
    @jwt_required()
    def update_sweet_details(sweet_id):# Update  specific sweet details retrieved by  sweet id

        sweet = db.session.get(Sweet, sweet_id)  # assigning  sweet instance with specidfic sweet details
        data = request.json

      # check for fields present in  request header  from the client

        if 'name' in data :
            sweet.name = data['name']  # assinging the updated  name value from client header

        if 'category' in data:
            sweet.category = data['category']  # assinging the updated  category value from client header


        if 'price' in data:
           try:
                
                new_price = float(data['price']) # converting  price into float
                if new_price <= 0: # check for price value must be positive
                     return jsonify({"message": "Price must be a positive number"}), 400
                sweet.price = new_price  # assigning the updated new price value
           except ValueError:       # catches   price value errors and return suitable response.
                return jsonify({"message": "Price must be a valid number"}), 400
            
        db.session.commit()

       
        return jsonify({
        "message": f"Sweet ID {sweet_id} updated successfully.",
        "details": sweet.convert_to_dict()
    }), 200





    

    @app.route('/api/sweets/search', methods=['GET'])
    @jwt_required()
    def search_sweets():
        #   base query for all sweets present in data dabase.
        query = Sweet.query
        
        #  Extract query parameters from the URL
        name = request.args.get('name')
        category = request.args.get('category')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')

        ## Building filters based on provided parameters

        # Filter by Name                                    ### help by ai
        if name:
            query = query.filter(Sweet.name.ilike(f'%{name}%'))

        # Filter by Category 
        if category:
            query = query.filter(Sweet.category == category)

        # Filter by Minimum Price
        if min_price:
            try:
                min_price_float = float(min_price)
                query = query.filter(Sweet.price >= min_price_float)
            except ValueError:
                return jsonify({"message": "Invalid value for min_price. Must be a number."}), 400

        # Filter by Maximum Price
        if max_price:
            try:
                max_price_float = float(max_price)
                query = query.filter(Sweet.price <= max_price_float)
            except ValueError:
                return jsonify({"message": "Invalid value for max_price. Must be a number."}), 400
                
        #  Executed  the final filtered query
        sweets = query.all()
        
        #  Handle empty result set (Standard RESTful practice)
        if not sweets:
            return jsonify({
                "message": "No sweets found matching your search criteria.",
                "sweets": []
            }) , 200
            
        # Convert to list of dictionaries and return a 200 ok status
        sweets_list = [sweet.convert_to_dict() for sweet in sweets]
        return jsonify({
    
    "message": f"Found {len(sweets_list)} sweets.",
    "sweets": sweets_list
}), 200

    
    @app.route('/api/sweets/<int:sweet_id>/delete', methods=['DELETE']) # Route to delete sweet data from data base (Admin only route).
    @jwt_required() #only logged in user can access it .
    def delete_sweet(sweet_id):
         
        current_user_id = get_jwt_identity() # assigning looged in user id
        current_user = db.session.get(User_Details, current_user_id) # fetching logged in user details.


        if not current_user or current_user.role != 'admin':  #  check for  admin user role
          return jsonify({"message": "Access Forbidden: Admin privileges required"}), 403
        
        sweet = db.session.get(Sweet, sweet_id) #current user role is  admin  and fetching the required sweet details

        if not sweet:
            return jsonify(
                {"message" : "Sweet ID {sweet_id} does not exsist"}
            )
        db.session.delete(sweet)
        db.session.commit()

        return jsonify(
            {"message": "Data deleted"}
        )




###### INVENTORY ######

   

    @app.route('/api/sweets/<int:sweet_id>/purchase', methods=['POST'])  #### Route to purchase sweet.
    @jwt_required() # check for logged in user  accessing this route.
    def purchase_sweet(sweet_id):
        
        #Check if the sweet exists (404 Not Found)
        current_id= get_jwt_identity() #accesing for logged in user id.
        sweet = db.session.get(Sweet, sweet_id) # retrieving  sweet details from sweet id 
        if sweet is None:
            return jsonify({"message": f"Sweet with ID {sweet_id} not found"}), 404

        # Get data from the request body
        data = request.json
        
        # Check for the required field
        if not data or 'quantity_purchased' not in data:
            return jsonify({"message": "Missing 'quantity_purchased' field in request body"}), 400
        
        #  Validate quantity input (type and value)
        try:
            quantity_purchased = int(data['quantity_purchased'])
            if quantity_purchased <= 0:
                return jsonify({"message": "Quantity purchased must be a positive integer"}), 400
        except ValueError:
            return jsonify({"message": "Quantity purchased must be an integer"}), 400

        #  Check for sufficient stock 
        if sweet.quantity < quantity_purchased:
            return jsonify({
                "message": f"Insufficient stock for {sweet.name}.",
                "available_stock": sweet.quantity
            }), 409 

        # Process the sale that is Decrease quantity
        sweet.quantity -= quantity_purchased
        db.session.commit() # Save the new quantity to the database
        
        # Calculate transaction total
        total_price = quantity_purchased * sweet.price
        
        # Return success  purchase transaction and response (200 OK)
        return jsonify({
            "message": f"Successfully purchased {quantity_purchased} units of {sweet.name}.",
            "transaction_total": round(total_price, 2),
            "current_stock": sweet.quantity,
            "details": sweet.convert_to_dict()
        }), 200
    



    @app.route('/api/sweets/<int:sweet_id>/restock', methods=['POST']) # Route to restock sweets ----it is admin based action
    @jwt_required() #check for logged in user can access this end point.
    def restock_sweet(sweet_id):
        # first check for user role----- logged in user & its an admin
        current_user_id = get_jwt_identity() 
        current_user = db.session.get(User_Details, current_user_id)
        current_user_role = current_user.role


        # check for current user role whether  it  is admin or not.
        if not current_user or current_user_role.lower() != 'admin':
         return jsonify({"message": "Access Forbidden: Admin privileges required"}), 403 # 403 Forbidden
        #Check if the sweet exists (404 Not Found)
        sweet = db.session.get(Sweet, sweet_id)
        if sweet is None:
            return jsonify({"message": f"Sweet with ID {sweet_id} not found"}), 404

        #Get data from the request body
        data = request.json
        
        # Check for the required field
        if not data or 'quantity_added' not in data:
            return jsonify({"message": "Missing 'quantity_added' field in request body"}), 400
        
        # Validate quantity input (type and value)
        try:
            quantity_added = int(data['quantity_added'])
            # Restock quantity must be positive
            if quantity_added <= 0:
                return jsonify({"message": "Quantity added must be a positive integer"}), 400
        except ValueError:
            return jsonify({"message": "Quantity added must be an integer"}), 400

        #  Process the restock: Increase quantity
        sweet.quantity += quantity_added
        db.session.commit() # Save the new quantity to the database
        
        #  Return success response (200 OK)
        return jsonify({
            "message": f"Successfully added {quantity_added} units of {sweet.name} to stock.",
            "current_stock": sweet.quantity,
            "details": sweet.convert_to_dict()
        }), 200
    


    return app

    
    #with app.app_context():
        # Now db.create_all() can see the User model defined above
        
      #  db.create_all()
        
        
    #return app

# Simple Entry Point
app = create_app()

if __name__ == '__main__':
    # To run, use command flask run
    app.run(debug=True)



