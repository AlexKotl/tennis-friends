from django.shortcuts import render, get_object_or_404

def index(request):
    return render(request, 'index.html', {
        # 'bases': Base.get_all(request),
    })