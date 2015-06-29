from flask import url_for

from MookAPI.core import db
from . import ResourceContentJsonSerializer, \
    ResourceContent, \
    ResourceJsonSerializer, \
    Resource

class DownloadableFileResourceContentJsonSerializer(ResourceContentJsonSerializer):
    pass

class DownloadableFileResourceContent(DownloadableFileResourceContentJsonSerializer, ResourceContent):
    
    content_file = db.FileField(required=True)
    """A file to download."""

    @property
    def content_file_url(self):
        """The URL at which the file can be downloaded."""
        if not self.content_file:
            return None

        if not hasattr(self, '_instance'):
            return None

        return url_for(
            "resources.get_resource_content_file",
            resource_id=self._instance.id,
            filename=self.content_file.filename,
            _external=True
        )

class DownloadableFileResourceJsonSerializer(ResourceJsonSerializer):
    pass

class DownloadableFileResource(Resource):
    """Stores a file in the database."""

    resource_content = db.EmbeddedDocumentField(DownloadableFileResourceContent)
