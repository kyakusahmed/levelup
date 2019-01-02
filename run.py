from app import app
from app.models.migration import Migration


if __name__ == "__main__":  
    app.run(debug=True, port=8080)


#     db = Migration()
#     db.create_tables()
#     db.drop_tables() 
    # db.create_tables()    