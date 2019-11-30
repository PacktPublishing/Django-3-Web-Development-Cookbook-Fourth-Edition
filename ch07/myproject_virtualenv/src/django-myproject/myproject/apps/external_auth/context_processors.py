
def auth0(request):
    data = {}
    if request.user.is_authenticated:
        auth0_user = request.user.social_auth.filter(provider="auth0").first()
        data = {
            "auth0_user": auth0_user,
        }
    return data