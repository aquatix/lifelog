class NotImplemented(Exception):
    """Exception raised when integration/plugin/functionality is not implemented yet.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        """Constructor.

        :param str message: The description of the exception
        """
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
