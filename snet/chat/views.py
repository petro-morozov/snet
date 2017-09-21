from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Room, Message
from django.core import serializers

User = get_user_model()

@login_required(login_url='/reg/login/')
def create_room(request, user_id):
    u_id = User.objects.get(id = user_id)
    try:
        q = Room.objects.get(Q(f_usr = request.user, s_usr = u_id) |Q(f_usr = u_id, s_usr = request.user))
        return redirect('chat:chat_room', room_id=q.id)
    except ObjectDoesNotExist:
        if request.user == u_id:
            messages.success(request, 'Вы не можете писать себе.')
            return redirect('user_page:show_all_users')
        else:
            r = Room(f_usr = request.user, s_usr = u_id)
            r.save()
            return redirect('chat:chat_room', room_id=r.id)

@login_required(login_url='/reg/login/')
def chat_room(request, room_id):
    try:
        user_check = Room.objects.get(Q(id = room_id, f_usr=request.user) | Q(id = room_id, s_usr=request.user))
    except ObjectDoesNotExist:
        messages.success(request, 'Нет доступа.')
        return redirect('user_page:show_all_users')
    try:
        q_mess = Message.objects.filter(room=room_id, saw=False).exclude(fk=request.user).all()
        for q in q_mess:
            q.saw = True
            q.save()
    except ObjectDoesNotExist:
        pass
    try:
        first_msgs = Message.objects.filter(room=room_id).order_by('-id')[0:100]
        if not first_msgs:
            first_msgs = False
    except ObjectDoesNotExist:
        first_msgs = False
    rr = Room.objects.get(id = room_id)
    context = {"rr": rr, 'first_msgs':first_msgs}
    return render(request, "chat/chat.html",context)

@login_required(login_url='/reg/login/')
def messages_list(request, room_id, plscount):
    print(plscount)
    n1 = 0
    n2 = 100
    n1 = n1 + int(plscount)
    n2 = n2 + int(plscount)
    msgs2 = Message.objects.filter(room=room_id).order_by('-id')[n1:n2]
    if request.is_ajax:
        msgs_list = serializers.serialize('json', msgs2)
        return JsonResponse(msgs_list, safe=False)
    context = {'msgs2':msgs2}
    return render(request, "chat/chat.html",context)


@login_required(login_url='/reg/login/')
def user_rooms(request):
    try:
        q = Room.objects.filter(Q(f_usr = request.user) |Q(s_usr = request.user))
    except ObjectDoesNotExist:
        q = "У вас нет переписок."
    return render(request, "chat/rooms.html", {"q": q,})
