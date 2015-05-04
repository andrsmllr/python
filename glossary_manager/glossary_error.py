
class GlossaryError(Exception):
    """Base error for everything that can go wrong in Glossary operations."""
    def __init__(self, message):
        super(Exception, self).__init__(message)

