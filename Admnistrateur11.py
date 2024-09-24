from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modèles de données
class Equipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)

class Joueur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipe.id'), nullable=False)
    equipe = db.relationship('Equipe', backref=db.backref('joueurs', lazy=True))

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    equipe_dom_id = db.Column(db.Integer, db.ForeignKey('equipe.id'), nullable=False)
    equipe_dom = db.relationship('Equipe', foreign_keys=[equipe_dom_id])
    equipe_ext_id = db.Column(db.Integer, db.ForeignKey('equipe.id'), nullable=False)
    equipe_ext = db.relationship('Equipe', foreign_keys=[equipe_ext_id])
    cote_equipe_dom = db.Column(db.Float, nullable=False)
    cote_equipe_ext = db.Column(db.Float, nullable=False)

# Routes pour l'API d'administration
@app.route('/equipes', methods=['POST'])
def creer_equipe():
    nom = request.json.get('nom')
    if not nom:
        return jsonify({'message': 'Nom de l\'équipe requis'}), 400
    equipe = Equipe(nom=nom)
    db.session.add(equipe)
    db.session.commit()
    return jsonify({'message': 'Équipe créée avec succès'}), 201

@app.route('/joueurs', methods=['POST'])
def creer_joueur():
    nom = request.json.get('nom')
    equipe_id = request.json.get('equipe_id')
    if not nom or not equipe_id:
        return jsonify({'message': 'Nom du joueur et ID de l\'équipe requis'}), 400
    joueur = Joueur(nom=nom, equipe_id=equipe_id)
    db.session.add(joueur)
    db.session.commit()
    return jsonify({'message': 'Joueur créé avec succès'}), 201

@app.route('/matchs', methods=['POST'])
def creer_match():
    data = request.json
    date = data.get('date')
    equipe_dom_id = data.get('equipe_dom_id')
    equipe_ext_id = data.get('equipe_ext_id')
    cote_equipe_dom = data.get('cote_equipe_dom')
    cote_equipe_ext = data.get('cote_equipe_ext')
    
    if not date or not equipe_dom_id or not equipe_ext_id:
        return jsonify({'message': 'Date, ID de l\'équipe domicile et ID de l\'équipe extérieure requis'}), 400
    
    match = Match(
        date=datetime.fromisoformat(date),  # Assurez-vous que la date est au bon format
        equipe_dom_id=equipe_dom_id,
        equipe_ext_id=equipe_ext_id,
        cote_equipe_dom=cote_equipe_dom,
        cote_equipe_ext=cote_equipe_ext
    )
    db.session.add(match)
    db.session.commit()
    return jsonify({'message': 'Match créé avec succès'}), 201

@app.route('/equipes', methods=['GET'])
def lister_equipes():
    equipes = Equipe.query.all()
    return jsonify([{'id': equipe.id, 'nom': equipe.nom} for equipe in equipes]), 200

@app.route('/joueurs', methods=['GET'])
def lister_joueurs():
    joueurs = Joueur.query.all()
    return jsonify([{'id': joueur.id, 'nom': joueur.nom, 'equipe_id': joueur.equipe_id} for joueur in joueurs]), 200

@app.route('/matchs', methods=['GET'])
def lister_matchs():
    matchs = Match.query.all()
    return jsonify([{
        'id': match.id,
        'date': match.date.isoformat(),
        'equipe_dom': match.equipe_dom.nom,
        'equipe_ext': match.equipe_ext.nom,
        'cote_equipe_dom': match.cote_equipe_dom,
        'cote_equipe_ext': match.cote_equipe_ext
    } for match in matchs]), 200

if __name__ == '__main__':
    app.run(debug=True)
