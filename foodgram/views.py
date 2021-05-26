from django.shortcuts import render


def page_not_found(request, exception):
    """Show 404 error page."""
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    """Show 505 error page."""
    return render(request, "misc/500.html", status=500)
