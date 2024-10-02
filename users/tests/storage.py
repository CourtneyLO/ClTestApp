from django.core.files.storage import Storage

class MockStorage(Storage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _save(self, name, content):
        # Mock the save operation
        return name  # Return the file name as if it's saved

    def delete(self, name):
        # Mock the delete operation
        pass  # Do nothing since it's just a mock

    def url(self, name):
        # Mock the URL retrieval
        return name  # Return the file name as the URL

    def exists(self, name):
        # Mock the existence check
        return False  # Always return False since files don't actually exist
