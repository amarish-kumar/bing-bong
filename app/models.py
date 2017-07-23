from app import db

# Describes entities that we've discovered. For example, it could
# be Zlatan Ibrahimovic with classification of football player
# or "How to build a chatbot?" post on medium.com
class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), index=True)
    url = db.Column(db.String(1024), unique=True)
    image_url = db.Column(db.String(1024))
    # Text can be used for wildcard topic match
    text = db.Column(db.String(1048576))
    classification = db.Column(db.String(1024), index=True)

# Attributes that an entity has. E.g. "nationality": "Sweeden"
class Attributes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, index=True)
    attribute_name = db.Column(db.String(1024))
    attribute_value = db.Column(db.String(1024))
