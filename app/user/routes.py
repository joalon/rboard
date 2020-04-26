from app.user import user_bp


@user_bp.route('/register')
def register():
    return "register"
