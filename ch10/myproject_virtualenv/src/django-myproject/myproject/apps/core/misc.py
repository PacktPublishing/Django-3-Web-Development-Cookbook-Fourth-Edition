def custom_show_toolbar(request):
    return "1" == request.COOKIES.get("DebugToolbar", False)
