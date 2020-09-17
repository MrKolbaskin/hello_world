from flask_restful import Resource

class ModelResource(Resource):
    @staticmethod
    def get():
        return {"message": "GangBank welcomes you!"}, 200