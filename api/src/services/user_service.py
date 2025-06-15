from src.models.user import User
from werkzeug.exceptions import Conflict, NotFound

class UserService:
    def add_user(data):
        
        first_name = data["first_name"]
        middle_name = data.get("middle_name")
        last_name = data["last_name"]
        phone = data["phone"]

        existing_user = User.query.filter_by(first_name = first_name, middle_name = middle_name, last_name = last_name).first()
        if existing_user:
            raise Conflict("User with this name alredy exists")
        
        existing_user = User.query.filter_by(phone=phone).first()
        if existing_user:
            raise Conflict("User with this phone alredy exists")
        

        user = User(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            phone=phone
        )


        user.save_to_db()

        return user.to_dict()
    
    def get_users():
        return User.get_all()
    

    def get_user_by_id(user_id):
        user = User.get_by_id(user_id)
        if not user:
            raise NotFound("User not found")
        
        return user.to_dict()
    
    def update_user(user_id, user_data):
        user = User.get_by_id(user_id)

        if not user:
            raise NotFound("User not found")

        for key, value in user_data.items():
            setattr(user, key, value)

        user.update_to_db()

        return user.to_dict()
    

    def delete_user(user_id):

        user = User.get_by_id(user_id)

        if not user:
            raise NotFound("User not found")
        
        user.delete_to_db()

