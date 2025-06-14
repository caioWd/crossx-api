from flask_restx import Namespace, Resource, fields
from src.models.user import User

user_ns = Namespace("users")

user_model = user_ns.model("User",{
    "first_name":fields.String(required=True),
    "middle_name":fields.String(required=False),
    "last_name":fields.String(required=True),
    "phone":fields.String(required=True)
})

@user_ns.route("")
class Users(Resource):
    @user_ns.expect(user_model) 
    def post(self):
        try:
            data = user_ns.payload

            user = User(
                data["first_name"],
                data["middle_name"],
                data["last_name"],
                data["phone"]
            )

            user.save()

            return {"message":"user created successfuly"}, 201
        except Exception as e:
            return {"error": str(e)}, 500
  

    def get(self):
        try:
            users = User.get_all()
            return users, 200
        except Exception as e:
            return {"error": str(e)}, 500
        

@user_ns.route("/<int:user_id>")
class UserDetail(Resource):
    @user_ns.expect(user_model)
    def put(self, user_id):
        try:
            data = user_ns.payload
            user = User.get_by_id(user_id)

            if not user:
                return {"message":"user not found"},204

            for key, value in data.items():
                setattr(user, key, value)

            user.update_to_db()
            return {"message":"user updated successfuly"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        

    def get(self, user_id):
        try: 
            user = User.get_by_id(user_id)
            return user, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
    def delete(self, user_id):
        try:
            user = User.get_by_id(user)
            user.delete_to_db()
            return {"message":"user deleted successfuly"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
