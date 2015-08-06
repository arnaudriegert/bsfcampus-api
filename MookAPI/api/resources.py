import io

from flask import Blueprint, jsonify, send_file, abort
from flask_jwt import current_user, verify_jwt
from MookAPI.auth import jwt_required

from MookAPI.services import \
    resources, \
    lessons, \
    exercise_resources, \
    downloadable_file_resources, \
    audio_resources, \
    linked_file_resources

from . import route

bp = Blueprint('resources', __name__, url_prefix="/resources")


@route(bp, "/")
@jwt_required()
def get_resources():
    return resources.all().order_by('parent', 'order', 'title')


@route(bp, "/lesson/<lesson_id>")
@jwt_required()
def get_lesson_resources(lesson_id):
    return resources.find(parent=lesson_id).order_by('order', 'title')


@route(bp, "/skill/<skill_id>")
@jwt_required()
def get_skill_resources(skill_id):
    lessons_list = lessons.find(skill=skill_id)
    return resources.find(parent__in=lessons_list).order_by('order', 'title')


@route(bp, "/<resource_id>", jsonify_wrap=False)
# @jwt_required()
def get_resource(resource_id):
    resource = resources.get_or_404(resource_id)
    response = None

    try:
        verify_jwt()
    except:
        pass
    else:
        if not resource.is_additional:
            from MookAPI.services import visited_resources
            visited_resources.create(
                credentials=current_user._get_current_object(),
                resource=resource
            )
            current_user.add_started_track(resource.track)
            if not exercise_resources._isinstance(resource):
                current_user.add_completed_resource(resource)
                if current_user.user.is_track_test_available_and_never_attempted(resource.track):
                    alert = {"code": "prompt_track_validation", "id": resource.track._data.get("id", None)}
                    response = jsonify(data=resource, alert=alert)

    if not response:
        response = jsonify(data=resource)

    return response


@route(bp, "/<resource_id>/hierarchy", jsonify_wrap=False)
@jwt_required()
def get_resource_hierarchy(resource_id):
    resource = resources.get_or_404(resource_id)

    lesson = resource.parent
    skill = lesson.skill
    track = skill.track

    return jsonify(
        data=resource,
        lesson=lesson,
        skill=skill,
        track=track,
        siblings=resource.siblings(),
        aunts=resource.aunts(),
        cousins=resource.cousins()
    )


@route(bp, "/<resource_id>/content-file/<filename>", jsonify_wrap=False)
# @jwt_required()
def get_resource_content_file(resource_id, filename):
    resource = resources.get_or_404(resource_id)

    if linked_file_resources._isinstance(resource):
        content_file = resource.resource_content.content_file

        return send_file(
            io.BytesIO(content_file.read()),
            attachment_filename=content_file.filename,
            mimetype=content_file.contentType
        )

    abort(404)


@route(bp, "/<resource_id>/content-image/<filename>", jsonify_wrap=False)
# @jwt_required()
def get_resource_content_image(resource_id, filename):
    resource = resources.get_or_404(resource_id)

    if audio_resources._isinstance(resource):
        content_image = resource.resource_content.image

        return send_file(
            io.BytesIO(content_image.read()),
            attachment_filename=content_image.filename,
            mimetype=content_image.contentType
        )

    abort(404)


@route(bp, "/<resource_id>/question/<question_id>/image/<filename>", jsonify_wrap=False)
# @jwt_required()
def get_exercise_question_image(resource_id, question_id, filename):
    resource = exercise_resources.get_or_404(resource_id)

    try:
        question = resource.question(question_id=question_id)
        question_image = question.question_image
        return send_file(
            io.BytesIO(question_image.read()),
            attachment_filename=question_image.filename,
            mimetype=question_image.contentType
        )
    except:
        abort(404)
