from django.contrib.auth import get_user_model

User=get_user_model()

#todo: How to log in with username? its not working, also in authentication backend below class is imported
class UsernameAuthBackend(object):
    def authenticate(self, request, username=None, password=None):
        try:
            user=User.objects.get(username=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

