from MookAPI.core import Service
from .documents import Role, User, UserCredentials

class RolesService(Service):
    __model__ = Role

class UsersService(Service):
    __model__ = User

class UserCredentialsService(Service):
    __model__ = UserCredentials

    def _preprocess_params(self, kwargs):
        password = kwargs.get('password', None)
        if password:
            hashed_password = self.__model__.hash_pass(password)
            kwargs['password'] = hashed_password
        return super(UserCredentialsService, self)._preprocess_params(kwargs)

    def get(self, id=None, **kwargs):
        if id:
            return super(UserCredentialsService, self).get(id=id)

        central_id = kwargs.get('central_id', None)
        if central_id:
            return super(UserCredentialsService, self).get(central_id=central_id)

        password = kwargs.pop('password', None)
        if not kwargs.get('local_server', None):
            kwargs['local_server'] = None
        creds = super(UserCredentialsService, self).get(id=id, **kwargs)
        if not password or creds.verify_pass(password):
            return creds
        return None
