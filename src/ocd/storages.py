from django.conf import settings
from django.core.files.storage import FileSystemStorage


uploads_storage = FileSystemStorage(settings.UPLOAD_PATH)
