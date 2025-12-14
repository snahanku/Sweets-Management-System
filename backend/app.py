# backend/app.py (Corrected Structure)
from flask import Flask, jsonify , request # Added jsonify for proper API routes
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager , create_access_token , jwt_required , get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import os

# 1. Initialize Components
db = SQLAlchemy()

jwt = JWTManager()




BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'sweet_shop.db')

# 2. Define ALL Database Models HERE (BEFORE create_app is called)
class User_Details(db.Model):
    # Example Model
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

    # ... other model fields ...

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

s1= Sweet()
s1.id = 1
s1.name = "gulabjamun"
s1.category = "Sweet"
s1.price= 23.5
s1.quantity =200






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
    
    # 4. Define or Register Routes/Blueprints INSIDE the Factory
    # The error was caused by registering a route *before* the app existed
    @app.route("/")
    def index():
        # You can access the database here because the context is set up
        return "Hello, World!"



    @app.route("/random")
    def value():
        # You can access the database here because the context is set up
        return s1.convert_to_dict()
    



##### Auth ####

    @app.route("/auth/register" , methods=['POST'])

    def register_user():
        data = request.json
        username = data.get("username")
        password= data.get("password")

        if not username or not password:
            return jsonify(
                {"message" : "Username and password are required"}
            )
        
        ### check for already existing user 
        if User_Details.query.filter_by(username= username).first() :
            return jsonify(
                {
                    "message" : "user already exisit"
                }
            )
        
        new_user = User_Details(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()


        return jsonify(
            {
                "message": "user registered successfully",
                "user-details":new_user.to_dict()
            }
        )


    @app.route("/auth/login" , methods=['POST'])
    def login_user():
        data = request.json
        username = data.get("username")
        password= data.get("password")

        if not username or not password:
            return jsonify({
                "message" : "username and password required"
            })
        

        user =  User_Details.query.filter_by(username= username).first()
            
        
        if user and user.check_password(password):

            access_token = create_access_token(identity= str(user.id))

            return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "user_id": user.id
        }), 200

        else:
            return jsonify(
                {
                    "message" :"Invalid credentials"
                }
            ) , 401




    

##### sweet-Management  ######



    @app.route("/api/add-sweets" , methods =['POST'])
    @jwt_required()
    def add_sweets():

        data = request.json

        req_attributes = ['name' , 'category' , 'price' , 'quantity']
        if not all([ field in data for field in req_attributes]):
           return jsonify({"message":"missing required fields"}) 
        
        try:
            new_sweet = Sweet(
                name=data['name'],
                category=data['category'],
                # Ensure price and quantity are correctly typed before insertion
                price=float(data['price']),
                quantity=int(data['quantity'])
            )
        except ValueError:
            return jsonify({
                "messaage" : "Price must be Number(float) and Quantity must be Integer"
            })
        db.session.add(new_sweet)
        db.session.commit()

        return jsonify( { "mesaage" : "Product added successfully" ,
          "Sweet-details" : new_sweet.convert_to_dict()}) , 201
    
    
    @app.route("/api/get_all_sweets" , methods=['GET'])
    @jwt_required()
    def get_all_sweets():

        sweets= Sweet.query.all()

        if not sweets: 

            return jsonify({
             "message" : "No sweets currently in inventory.",
             "sweets": []
         }) , 200
        

        sweet_list =[]
        for sweet in sweets:
            sweet_list.append(sweet.convert_to_dict())
        
        


        return jsonify(sweet_list) , 200



    @app.route("/api/sweets/<int:sweet_id>", methods=['PUT'])
    @jwt_required()
    def update_sweet_details(sweet_id):

        sweet = Sweet.query.get(sweet_id)
        data = request.json
         
        if 'name' in data :
            sweet.name = data['name']

        if 'category' in data:
            sweet.category = data['category']

        if 'price' in data:
           try:
                
                new_price = float(data['price'])
                if new_price <= 0:
                     return jsonify({"message": "Price must be a positive number"}), 400
                sweet.price = new_price
           except ValueError:
                return jsonify({"message": "Price must be a valid number"}), 400
            
        db.session.commit()

       
        return jsonify({
        "message": f"Sweet ID {sweet_id} updated successfully.",
        "details": sweet.convert_to_dict()
    }), 200





    

    @app.route('/api/sweets/search', methods=['GET'])
    @jwt_required()
    def search_sweets():
        # 1. Start with the base query for all sweets
        query = Sweet.query
        
        # 2. Extract query parameters from the URL
        name = request.args.get('name')
        category = request.args.get('category')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')

        # 3. Build dynamic filters based on provided parameters

        # Filter by Name (Case-insensitive partial match)
        if name:
            query = query.filter(Sweet.name.ilike(f'%{name}%'))

        # Filter by Category (Exact match)
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
                
        # 4. Execute the final filtered query
        sweets = query.all()
        
        # 5. Handle empty result set (Standard RESTful practice)
        if not sweets:
            return jsonify({
                "message": "No sweets found matching your search criteria.",
                "sweets": []
            }) , 200
            
        # 6. Convert to list of dictionaries and return
        sweets_list = [sweet.convert_to_dict() for sweet in sweets]
        return jsonify(sweets_list), 200

    
    @app.route('/api/sweets/<int:sweet_id>', methods=['DELETE'])
    @jwt_required()
    def delete_sweet(sweet_id):
         
        current_user_id = get_jwt_identity() 
        current_user = User_Details.query.get(current_user_id)

        if not current_user or current_user.role != 'admin':
          return jsonify({"message": "Access Forbidden: Admin privileges required"}), 403
        
        sweet =Sweet.query.get(sweet_id)

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

   

    @app.route('/api/sweets/<int:sweet_id>/purchase', methods=['POST'])
    @jwt_required()
    # NOTE: In a real application, this should be protected (e.g., @jwt_required())
    def purchase_sweet(sweet_id):
        
        # 1. Check if the sweet exists (404 Not Found)
        current_id= get_jwt_identity()
        sweet = Sweet.query.get(sweet_id)
        if sweet is None:
            return jsonify({"message": f"Sweet with ID {sweet_id} not found"}), 404

        # 2. Get data from the request body
        data = request.json
        
        # 3. Check for the required field
        if not data or 'quantity_purchased' not in data:
            return jsonify({"message": "Missing 'quantity_purchased' field in request body"}), 400
        
        # 4. Validate quantity input (type and value)
        try:
            quantity_purchased = int(data['quantity_purchased'])
            if quantity_purchased <= 0:
                return jsonify({"message": "Quantity purchased must be a positive integer"}), 400
        except ValueError:
            return jsonify({"message": "Quantity purchased must be an integer"}), 400

        # 5. CRITICAL: Check for sufficient stock (409 Conflict)
        if sweet.quantity < quantity_purchased:
            return jsonify({
                "message": f"Insufficient stock for {sweet.name}.",
                "available_stock": sweet.quantity
            }), 409 

        # 6. Process the sale: Decrease quantity
        sweet.quantity -= quantity_purchased
        db.session.commit() # Save the new quantity to the database
        
        # 7. Calculate transaction total
        total_price = quantity_purchased * sweet.price
        
        # 8. Return success response (200 OK)
        return jsonify({
            "message": f"Successfully purchased {quantity_purchased} units of {sweet.name}.",
            "transaction_total": round(total_price, 2),
            "current_stock": sweet.quantity,
            "details": sweet.convert_to_dict()
        }), 200
    




     # backend/app.py (Inside create_app function)

    @app.route('/api/sweets/<int:sweet_id>/restock', methods=['POST'])
    # NOTE: In a real application, this should be protected by @admin_required()
    @jwt_required()
    def restock_sweet(sweet_id):
        


       # current_user_id = get_jwt_identity() 
       # current_user = User_Details.query.get(current_user_id)
       # current_user_role = current_user.role
       # if not current_user or current_user_role.lower() != 'admin':
        # return jsonify({"message": "Access Forbidden: Admin privileges required"}), 403 # 403 Forbidden
        # 1. Check if the sweet exists (404 Not Found)
        sweet = Sweet.query.get(sweet_id)
        if sweet is None:
            return jsonify({"message": f"Sweet with ID {sweet_id} not found"}), 404

        # 2. Get data from the request body
        data = request.json
        
        # 3. Check for the required field
        if not data or 'quantity_added' not in data:
            return jsonify({"message": "Missing 'quantity_added' field in request body"}), 400
        
        # 4. Validate quantity input (type and value)
        try:
            quantity_added = int(data['quantity_added'])
            # Restock quantity must be positive
            if quantity_added <= 0:
                return jsonify({"message": "Quantity added must be a positive integer"}), 400
        except ValueError:
            return jsonify({"message": "Quantity added must be an integer"}), 400

        # 5. Process the restock: Increase quantity
        sweet.quantity += quantity_added
        db.session.commit() # Save the new quantity to the database
        
        # 6. Return success response (200 OK)
        return jsonify({
            "message": f"Successfully added {quantity_added} units of {sweet.name} to stock.",
            "current_stock": sweet.quantity,
            "details": sweet.convert_to_dict()
        }), 200
    


    return app












    

















    # 5. Create Tables within the App Context
    with app.app_context():
        # Now db.create_all() can see the User model defined above
        
        db.create_all()
        
        
    return app

# 6. Simple Entry Point (This is the ONLY part outside the factory)
# This is fine for a simple app runner, but the actual 'flask run' command 
# doesn't need this if FLASK_APP is set correctly.
app = create_app()

if __name__ == '__main__':
    # To run, you often use FLASK_APP=backend/app.py flask run
    # or a dedicated run.py file.
    app.run(debug=True)



