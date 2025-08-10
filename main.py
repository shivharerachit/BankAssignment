from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

db = SQLAlchemy(app)

class Bank(db.Model):
    __tablename__ = 'banks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@app.route('/api/banks', methods=['GET'])
def get_banks():
    try:
        banks = Bank.query.all()
        return jsonify([{
            'id': bank.id,
            'name': bank.name
        } for bank in banks]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/banks/<int:bank_id>/branches', methods=['GET'])
def get_branches(bank_id):
    try:
        query = text("""
            SELECT 
                     ifsc, 
                     bank_id, 
                     branch, 
                     address, 
                     city, 
                     district, 
                     state, 
                     bank_name
            FROM bank_branches
            WHERE bank_id = :bank_id
        """)

        result = db.session.execute(query, {"bank_id": bank_id}).mappings().all()
        return jsonify([dict(row) for row in result]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/branches/<string:ifsc>', methods=['GET'])
def get_branch_details(ifsc):
    try:
        query = text("""
            SELECT 
                     ifsc, 
                     bank_id, 
                     branch, 
                     address, 
                     city, 
                     district, 
                     state, 
                     bank_name
            FROM bank_branches
            WHERE ifsc = :ifsc
        """)

        result = db.session.execute(query, {"ifsc": ifsc}).mappings().all()
        return jsonify([dict(row) for row in result]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)