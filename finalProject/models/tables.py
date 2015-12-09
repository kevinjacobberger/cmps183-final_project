#########################################################################
## Define your tables below; for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

from datetime import datetime

db.define_table('cats',
             Field('author', db.auth_user, default=auth.user_id),
             Field('cat_name', 'text'),
             Field('cat_id'), # To uniquely identify categories.
             Field('is_editing', 'boolean', default=False),
             Field('cat_time', 'datetime', default=datetime.utcnow()),
             Field('front_runner', 'text'),
            )

db.define_table('discs',
             Field('author', db.auth_user, default=auth.user_id),
             Field('disc_name', 'text'),
             Field('disc_id'), # To uniquely identify categories.
             Field('is_editing', 'boolean', default=False),
             Field('disc_time', 'datetime', default=datetime.utcnow()),
             Field('front_runner', 'text'),
             Field('cat_loc'), # Reference to the category
             Field('likes', 'integer', default=0),
             Field('dislikes', 'integer', default=0),
            )

db.define_table('games',
             Field('author', db.auth_user, default=auth.user_id),
             Field('game_name', 'text'),
             Field('game_id'), # To uniquely identify categories.
             Field('is_editing', 'boolean', default=False),
             Field('game_time', 'datetime', default=datetime.utcnow()),
             Field('game_votes', 'integer', default=0),
             Field('cat_loc'), # Reference to the category
            )