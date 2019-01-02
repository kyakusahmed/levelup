from app.models.migration import Migration




db = Migration()
db.create_tables()
db.drop_tables() 
db.create_tables()  