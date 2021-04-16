import flask
from flask import request,jsonify
import json

class Players():
    def __init__(self,name,id,team):
        self.name=name
        self.id=id
        self.team=team

    @app.route('/all', methods=['GET'])
    def getAllPlayer(self):
        return jsonify(readPlayers())
