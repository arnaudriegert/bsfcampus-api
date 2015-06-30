from flask.ext.admin import Admin
from flask.ext.admin.contrib.mongoengine import ModelView

from MookAPI.services import \
    users, \
    tracks, \
    skills, \
    lessons, \
    exercise_resources, \
    track_validation_resources, \
    rich_text_resources, \
    audio_resources, \
    video_resources, \
    downloadable_file_resources, \
    roles, \
    local_servers


class UserView(ModelView):
    column_list = ('full_name', 'username', 'email', 'password', 'accept_cgu', 'roles')
    form_columns = ('full_name', 'username', 'email', 'password', 'accept_cgu', 'roles')

    def on_model_change(self, form, model, is_created):
        model.password = users.__model__.hash_pass(model.password)
        return


class ResourceView(ModelView):
    column_list = ('title', 'slug', 'description', 'order', 'keywords', 'parent')
    form_columns = ('title', 'slug', 'description', 'order', 'keywords', 'parent', 'resource_content')

    def on_model_change(self, form, model, is_created):
        # TODO: create slug automatically
        return


class HierarchyTrackView(ModelView):
    column_list = ('title', 'slug', 'description', 'order', 'icon')
    form_columns = ('title', 'slug', 'description', 'order', 'icon')

    def on_model_change(self, form, model, is_created):
        # TODO: create slug automatically
        return


class HierarchySkillView(ModelView):
    column_list = ('title', 'slug', 'description', 'short_description', 'track', 'order', 'icon')
    form_columns = ('title', 'slug', 'description', 'short_description', 'track', 'order', 'icon', 'validation_exercise')

    def on_model_change(self, form, model, is_created):
        # TODO: create slug automatically
        return


class HierarchyLessonView(ModelView):
    column_list = ('title', 'slug', 'description', 'order', 'skill')
    form_columns = ('title', 'slug', 'description', 'order', 'skill')

    def on_model_change(self, form, model, is_created):
        # TODO: create slug automatically
        return


admin_ui = Admin()


admin_ui.add_view(ResourceView(
    exercise_resources.__model__,
    name='Exercise',
    category='Resources'))

admin_ui.add_view(ResourceView(
    track_validation_resources.__model__,
    name='Track Validation Test',
    category='Resources'))

admin_ui.add_view(ResourceView(
    rich_text_resources.__model__,
    name='Rich Text',
    category='Resources'))

# admin.add_view(ResourceView(
#     external_video_resources.__model__,
#     name='External Video',
#     category='Resources'))

admin_ui.add_view(ResourceView(
    audio_resources.__model__,
    name='Audio',
    category='Resources'))

admin_ui.add_view(ResourceView(
    video_resources.__model__,
    name='Video',
    category='Resources'))

admin_ui.add_view(ResourceView(
    downloadable_file_resources.__model__,
    name='Downloadable File',
    category='Resources'))


admin_ui.add_view(HierarchyTrackView(
    tracks.__model__,
    name='Track',
    category='Hierarchy'))

admin_ui.add_view(HierarchySkillView(
    skills.__model__,
    name='Skill',
    category='Hierarchy'))

admin_ui.add_view(HierarchyLessonView(
    lessons.__model__,
    name='Lesson',
    category='Hierarchy'))


admin_ui.add_view(UserView(
    users.__model__,
    name='User',
    category='Authentication'))

admin_ui.add_view(ModelView(
    roles.__model__,
    name='Role',
    category='Authentication'))

admin_ui.add_view(ModelView(
    local_servers.__model__,
    name='Local server',
    category='Authentication'))