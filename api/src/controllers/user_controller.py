from flask_restx import Namespace, Resource, fields
from src.services.user_service import UserService
from werkzeug.exceptions import Conflict, InternalServerError, NotFound

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
            user = UserService.add_user(user_ns.payload)

            return {
                "message":"user created successfuly",
                "user":user
                }, 201
        except Conflict as e:
            return {"message": str(e)}, 409
        except InternalServerError as e:
            return {"message": str(e)}, 500
  

    def get(self):
        try:
            return UserService.get_users(), 200
        except InternalServerError as e:
            return {"message": str(e)}, 500
        

@user_ns.route("/<int:user_id>")
class UserDetail(Resource):
    @user_ns.expect(user_model)
    def put(self, user_id):
        try:
            user = UserService.update_user(user_id, user_ns.payload)

            return {
                "message":"user updated successfuly",
                "user":user
                }, 200
        
        except NotFound as e:
            return {"message": str(e)}, 404
        except InternalServerError as e:
            return {"message": str(e)}, 500
        

    def get(self, user_id):
        try: 
            return UserService.get_user_by_id(user_id), 200
        except NotFound as e:
            return {"message": str(e)}, 404
        except InternalServerError as e:
            return {"message": str(e)}, 500
        
    def delete(self, user_id):
        try:
            UserService.delete_user(user_id)
            return "", 204
        except NotFound as e:
            return {"message": str(e)}, 404
        except InternalServerError as e:
            return {"message": str(e)}, 500
