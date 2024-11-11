import base64

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from Client_Api.extensions import db
from Models import Education, Resume, User, Group, UserSocialNetwork

get_user_api = Blueprint('get_user_api', __name__)


@get_user_api.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()  # Требуем наличие JWT
def get_user_info(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"msg": "Access denied"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Проверка, что фото профиля существует, и его преобразование
    profile_photo_base64 = (
        base64.b64encode(user.profile_photo).decode('utf-8') if user.profile_photo else None
    )

    # Собираем данные пользователя
    resume = Resume.query.filter_by(id_user=user_id).first()
    user_data = {
        "id_user": user.id_user,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "middle_name": user.middle_name,
        "birth_date": user.birth_date.strftime('%Y-%m-%d') if user.birth_date else None,
        "profile_photo": profile_photo_base64,  # Передаем фото как base64 строку
        "resume": {
            "about_me": resume.about_me if resume else None,
            "id_pattern": resume.id_pattern if resume else None,
            "educations": [],
            "telegram": None
        }
    }

    # Получение Telegram ссылки
    if resume:
        tg_entry = UserSocialNetwork.query.filter_by(id_resume=resume.id_resume).first()
        if tg_entry:
            user_data["resume"]["telegram"] = tg_entry.network_link

    # Получение образований
    if resume:
        educations = Education.query.filter_by(id_resume=resume.id_resume).all()
        for edu in educations:
            university_name = edu.university.full_name if edu.university else None
            degree_name = edu.degree.degree_name if edu.degree else None
            group_name = Group.query.filter_by(id_group=edu.group_number).first().group_name if edu.group_number else None

            education_data = {
                "university": university_name,
                "group": group_name,
                "degree": degree_name,
                "start_date": edu.start_date.strftime('%Y-%m-%d') if edu.start_date else None,
                "end_date": edu.end_date.strftime('%Y-%m-%d') if edu.end_date else None
            }
            user_data["resume"]["educations"].append(education_data)

    return jsonify(user_data), 200


@get_user_api.route('/api/user/<int:user_id>/update_photo', methods=['POST'])
def update_user_photo(user_id):
    """API для обновления фотографии пользователя."""
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Проверка наличия фото в запросе
    photo_data = request.json.get("profile_photo")
    if not photo_data:
        return jsonify({"msg": "No photo data provided"}), 400

    try:
        # Декодируем изображение из Base64
        decoded_photo = base64.b64decode(photo_data)
        user.profile_photo = decoded_photo
        db.session.commit()
        return jsonify({"msg": "Profile photo updated successfully"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"msg": "Failed to update photo"}), 500


