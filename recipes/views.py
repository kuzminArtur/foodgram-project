from django.shortcuts import get_object_or_404, render, redirect


def index(request):
    return render(request, 'recipes/index.html')


def page_not_found(request, exception):
    """Отображает страницу 404 ошибки"""
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    """Отображает страницу 500 ошибки"""
    return render(request, "misc/500.html", status=500)
