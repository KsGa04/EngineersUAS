import base64

from flask import Blueprint, jsonify, request

from Client_Api.extensions import db
from Models import Education, Resume, User, Group

get_user_api = Blueprint('get_user_api', __name__)


@get_user_api.route('/user/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Проверяем наличие резюме у пользователя
    resume = Resume.query.filter_by(id_user=user_id).first()
    user_data = {
        "id_user": user.id_user,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "birth_date": user.birth_date.strftime('%Y-%m-%d') if user.birth_date else None,
        "resume": {
            "about_me": resume.about_me if resume else None,
            "educations": []
        }
    }

    # Если у пользователя есть резюме, получаем связанные образования
    if resume:
        educations = Education.query.filter_by(id_resume=resume.id_resume).all()

        for edu in educations:
            # Получаем данные университета, степени и группы, если они существуют
            university_name = edu.university.full_name if edu.university else None
            degree_name = edu.degree.degree_name if edu.degree else None
            group_name = Group.query.filter_by(
                id_group=edu.group_number).first().group_name if edu.group_number else None

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


