from .users import \
    RolesService, \
    UsersService

roles = RolesService()
users = UsersService()

from .hierarchy import \
    TracksService, \
    SkillsService, \
    LessonsService

tracks = TracksService()
skills = SkillsService()
lessons = LessonsService()

from .resources import \
    ResourcesService, \
    AudioResourcesService, \
    DownloadableFileResourcesService, \
    ExerciseResourcesService, \
    ExternalVideoResourcesService, \
    RichTextResourcesService, \
    TrackValidationResourcesService, \
    VideoResourcesService

resources = ResourcesService()
audio_resources = AudioResourcesService()
downloadable_file_resources = DownloadableFileResourcesService()
exercise_resources = ExerciseResourcesService()
external_video_resources = ExternalVideoResourcesService()
rich_text_resources = RichTextResourcesService()
track_validation_resources = TrackValidationResourcesService()
video_resources = VideoResourcesService()

from .activity import \
    ActivitiesService, \
    ExerciseAttemptsService, \
    SkillValidationAttemptsService, \
    TrackValidationAttemptsService

activities = ActivitiesService()
exercise_attempts = ExerciseAttemptsService()
skill_validation_attempts = SkillValidationAttemptsService()
track_validation_attempts = TrackValidationAttemptsService()

from .local_servers import LocalServersService

local_servers = LocalServersService()

from .synchronizer import ItemsToSyncService

items_to_sync = ItemsToSyncService()