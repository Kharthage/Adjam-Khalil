from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Modèles de données
class Pays(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)

class Equipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)
    pays_id = db.Column(db.Integer, db.ForeignKey('pays.id'), nullable=False)
    pays = db.relationship('Pays', backref=db.backref('equipes', lazy=True))

class Joueur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipe.id'), nullable=False)
    equipe = db.relationship('Equipe', backref=db.backref('joueurs', lazy=True))

# Routes pour l'API d'administration
@app.route('/pays', methods=['POST'])
def creer_pays():
    nom = request.json.get('nom')
    if not nom:
        return jsonify({'message': 'Nom du pays requis'}), 400
    
    pays = Pays(nom=nom)
    db.session.add(pays)
    db.session.commit()
    return jsonify({'message': 'Pays créé avec succès'}), 201

@app.route('/equipes', methods=['POST'])
def creer_equipe():
    nom = request.json.get('nom')
    pays_id = request.json.get('pays_id')
    
    if not nom or not pays_id:
        return jsonify({'message': 'Nom de l\'équipe et ID du pays requis'}), 400
    
    equipe = Equipe(nom=nom, pays_id=pays_id)
    db.session.add(equipe)
    db.session.commit()
    return jsonify({'message': 'Équipe créée avec succès'}), 201

@app.route('/joueurs', methods=['POST'])
def creer_joueur():
    nom = request.json.get('nom')
    prenom = request.json.get('prenom')
    numero = request.json.get('numero')
    equipe_id = request.json.get('equipe_id')
    
    if not nom or not prenom or not numero or not equipe_id:
        return jsonify({'message': 'Nom, prénom, numéro et ID de l\'équipe requis'}), 400
    
    joueur = Joueur(nom=nom, prenom=prenom, numero=numero, equipe_id=equipe_id)
    db.session.add(joueur)
    db.session.commit()
    return jsonify({'message': 'Joueur créé avec succès'}), 201

@app.route('/pays', methods=['GET'])
def lister_pays():
    pays = Pays.query.all()
    return jsonify([{'id': p.id, 'nom': p.nom} for p in pays]), 200

@app.route('/equipes', methods=['GET'])
def lister_equipes():
    equipes = Equipe.query.all()
    return jsonify([{'id': e.id, 'nom': e.nom, 'pays_id': e.pays_id} for e in equipes]), 200

@app.route('/joueurs', methods=['GET'])
def lister_joueurs():
    joueurs = Joueur.query.all()
    return jsonify([{
        'id': j.id,
        'nom': j.nom,
        'prenom': j.prenom,
        'numero': j.numero,
        'equipe_id': j.equipe_id
    } for j in joueurs]), 200

if __name__ == '__main__':
    app.run(debug=True)
