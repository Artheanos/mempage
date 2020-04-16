import bcrypt


def encrypt(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def match(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def session_logged_in(request):
    return bool(request.session['username']) and bool(request.session['id'])


def session_login(request, user):
    request.session['id'] = user.id
    request.session['username'] = user.username


def session_logout(request):
    for field in ['id', 'username']:
        if request.session.get(field):
            request.session.pop(field)
