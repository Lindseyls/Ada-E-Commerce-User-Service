from ..db import db
from ..models.user import User
from flask import Blueprint, request, Response
from .route_utilities import create_model, get_models_with_filters, validate_model, update_model, get_user_by_email

bp = Blueprint("users_blueprint", __name__, url_prefix="/users")

@bp.post("/")
def create_user():
  request_body = request.get_json()

  return create_model(User, request_body)

@bp.get("/")
def get_all_users():
  return get_models_with_filters(User, request.args)

@bp.get("/<id>")
def get_single_user(id):
  user = validate_model(User, id)

  return user.to_dict()

@bp.get("/email")
def get_single_user_by_email():
  email = request.args.get("email")

  return get_user_by_email(email)

@bp.put("/<id>")
def update_user(id):
  user = validate_model(User, id)
  request_body = request.get_json()

  return update_model(user, request_body)

@bp.delete("/<id>")
def delete_user(id):
  user = validate_model(User, id)

  db.session.delete(user)
  db.session.commit()

  return Response(status=204, mimetype="application/json")