from django.contrib import messages
from django.shortcuts import redirect


def check_authentication(view_func, *args, **kwargs):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, "Você precisa estar logado para acessar essa página."
            )
            return redirect("index")
        else:
            return view_func(request, *args, **kwargs)

    return wrapped
