from django.shortcuts import redirect

from chat.models import Room
from django.db.models import Q

def add_variable_to_context(request):
    msg_count = 0
    if request.user.is_authenticated:
        try:
            user_rooms = Room.objects.filter(Q(f_usr=request.user) | Q(s_usr=request.user))
            for room in user_rooms:
                try:
                    m = room.message.last()
                    if m.fk != request.user and m.saw == False:
                        msg_count += 1
                except:
                    pass
        except:
            msg_count = 0
    else:
        msg_count = 'blablabla'

    return {
        'new_messages_counter': msg_count
    }
