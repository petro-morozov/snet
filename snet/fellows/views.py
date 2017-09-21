from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import Fellows

User = get_user_model()

@login_required(login_url='/reg/login/')
def add_to_fellows(request):
    if request.method == 'POST':
        page_owner_id = User.objects.get(id = request.POST['page_owner_id'])
        if request.user != page_owner_id:
            try:
                f_query = Fellows.objects.get(first_user = request.user, second_user = page_owner_id)
            except ObjectDoesNotExist:
                new_f = Fellows(first_user = request.user, second_user = page_owner_id)
                new_f.save()
    return render(request, "user_page/all_users.html", {})
