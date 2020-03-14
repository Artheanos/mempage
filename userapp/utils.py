import bcrypt

from userapp.models import User


def encrypt(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def match(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def get_user(request):
    return User.objects.get(id=request.session.get('id'))


def session_login(request, user):
    request.session['id'] = user.id
    request.session['username'] = user.username


def session_logout(request):
    for field in ['id', 'username']:
        if request.session.get(field):
            request.session.pop(field)
