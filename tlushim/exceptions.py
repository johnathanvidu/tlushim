class LoginAttemptFailed(BaseException):
    def __init__(self, *args, **kwargs):
        super(LoginAttemptFailed, self).__init__(args, kwargs)
        self.message = 'Login failed. Please rerun tlushim with -c and reconfigure your login information'
