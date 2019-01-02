from app import app
from app.models.migration import Migration


if __name__ == "__main__":
    db = Migration()
    db.create_tables()
    db.drop_tables() 
    db.create_tables()  
    app.run(debug=True, port=8080)