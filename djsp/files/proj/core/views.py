from django.shortcuts import render


def home(request):
    template_name = "core/home.html"
    context = dict(
        project="{{ ' '.join(proj.upper().split('_')) }}",
        text="Hello World!",
    )
    return render(request, template_name, context=context)
