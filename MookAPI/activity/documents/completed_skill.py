from MookAPI.core import db

from . import ActivityJsonSerializer, Activity


class CompletedSkillJsonSerializer(ActivityJsonSerializer):
    pass


class CompletedSkill(CompletedSkillJsonSerializer, Activity):
    """
    Records when a resource is completed by a user
    """

    skill = db.ReferenceField('Skill')

    @property
    def object(self):
        return self.skill

    is_validated_through_test = db.BooleanField(default=False)

    def clean(self):
        super(CompletedSkill, self).clean()
        self.type = "completed_skill"

    def get_field_names_for_csv(self):
        """ this method gives the fields to export as csv row, in a chosen order """
        rv = super(CompletedSkill, self).get_field_names_for_csv()
        rv.extend(['is_validated_through_test'])
        return rv
