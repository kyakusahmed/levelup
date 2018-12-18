from db import Migration

db_conn = Migration()
db_conn.create_tables() 
db_conn.drop_tables()
db_conn.create_tables()
db_conn.add_human('name', 'address', 'age', 'single')
db_conn.get_human(1)
db_conn.delete_human(1)





