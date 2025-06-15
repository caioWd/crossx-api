from datetime import datetime, timezone
from database import db
from werkzeug.exceptions import InternalServerError

class User(db.Model):
    __tablename__="users"
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(40), nullable=False)
    middle_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(70), nullable=False)
    phone = db.Column(db.String(13), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __init__(self, first_name, last_name, phone, middle_name = None):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.phone = phone

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "created_at": self.created_at.strftime("%d/%m/%Y") if self.created_at else None,
            "updated_at": self.updated_at.strftime("%d/%m/%Y") if self.updated_at else None
        }

    

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()
            raise InternalServerError("Error saving user")

    @classmethod
    def get_all(cls):
        try:
            users = cls.query.all()
            return [user.to_dict() for user in users]
        except Exception as e:
            print(f"Error: {e}")
            raise InternalServerError("Error getting users")

    @classmethod
    def get_by_id(cls, user_id):
        try:
            user = db.session.get(cls, user_id)
            return user
        except Exception as e:
            print(f"Error: {e}")
            raise InternalServerError("Error getting user")

    def update_to_db(self):
        try:
            db.session.add(self)   
            db.session.commit() 
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()
            raise InternalServerError("Error updating user")

    def delete_to_db(self):
        try:
            db.session.delete(self)   
            db.session.commit() 
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()
            raise InternalServerError("Error deleting user")




