import io

from flask import Blueprint, jsonify, send_file
from flask_jwt import jwt_required

from MookAPI.services import tracks, skills, lessons

from . import route

bp = Blueprint("hierarchy", __name__, url_prefix="/hierarchy")


### TRACKS

@route(bp, "/tracks")
@jwt_required()
def get_tracks():
    """Get the list of all Track_ objects, ordered by ``order`` and ``title``, enveloped in a single-key JSON dictionary."""

    list = tracks.all().order_by('order', 'title')
    return jsonify(data=list)

@route(bp, "/tracks/<track_id>")
@jwt_required()
def get_track(track_id):
    """Get the Track_ with id ``track_id`` enveloped in a single-key JSON dictionary."""

    track = tracks.get_or_404(track_id)
    return jsonify(data=track)

@route(bp, "/tracks/<track_id>/icon")
# @jwt_required()
def get_track_icon(track_id):
    """Download the icon of the Track_ with id ``track_id``."""

    track = tracks.get_or_404(track_id)
    return send_file(
            io.BytesIO(track.icon.read()),
            attachment_filename=track.icon.filename,
            mimetype=track.icon.contentType
        )


### SKILLS

@route(bp, "/skills")
@jwt_required()
def get_skills():
    """Returns a list of all Skill_ objects, ordered by ``order`` and ``title``, enveloped in a single-key JSON dictionary."""

    list = skills.all().order_by('order', 'title')
    return jsonify(data=list)

@route(bp, "/skills/track/<track_id>")
@jwt_required()
def get_track_skills(track_id):
    """Returns a list of all Skill_ objects in a Track_, ordered by ``order`` and ``title``, enveloped in a single-key JSON dictionary."""

    list = skills.find(track=track_id).order_by('order', 'title')
    return jsonify(data=list)

@route(bp, "/skills/<skill_id>")
@jwt_required()
def get_skill(skill_id):
    """Get the Skill_ with id ``skill_id`` enveloped in a single-key JSON dictionary."""

    skill = skills.get_or_404(skill_id)
    return jsonify(data=skill)

@route(bp, "/skills/<skill_id>/icon")
# @jwt_required()
def get_skill_icon(skill_id):
    """Download the icon of the Skill_ with id ``skill_id``."""

    skill = skills.get_or_404(skill_id)
    return send_file(
            io.BytesIO(skill.icon.read()),
            attachment_filename=skill.icon.filename,
            mimetype=skill.icon.contentType
        )


### LESSONS

@route(bp, "/lessons")
@jwt_required()
def get_lessons():
    """Returns a list of all Lesson_ objects, ordered by ``order`` and ``title``, enveloped in a single-key JSON dictionary."""

    list = lessons.all().order_by('order', 'title')
    return jsonify(data=list)

@route(bp, "/lessons/skill/<skill_id>")
@jwt_required()
def get_skill_lessons(skill_id):
    """Returns a list of all Lesson_ objects in a Skill_, ordered by ``order`` and ``title``, enveloped in a single-key JSON dictionary."""

    list = lessons.find(skill=skill_id).order_by('order', 'title')
    return jsonify(data=list)

@route(bp, "/lessons/<lesson_id>")
@jwt_required()
def get_lesson(lesson_id):
    """Get the Lesson_ with id ``lesson_id`` enveloped in a single-key JSON dictionary."""

    lesson = lessons.get_or_404(lesson_id)
    return jsonify(data=lesson)