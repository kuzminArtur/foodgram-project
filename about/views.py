from django.shortcuts import render


def author(request):
    """Show info about author."""
    return render(request, "about/author.html", status=200)


def tech(request):
    """Show info about using technologies."""
    return render(request, "about/tech.html", status=200)
