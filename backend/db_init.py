from app import create_app, db # Import the necessary components

# 1. Create the application instance
app = create_app()

# 2. Use the application context
with app.app_context():
    # Drop existing tables (optional, but ensures a clean start)
    db.drop_all() 
    print("Dropped existing tables.")

    # Create all tables defined in your models (Sweet, User_Details)
    db.create_all()
    print("Database schema created successfully!")