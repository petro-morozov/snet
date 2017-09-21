import json
from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user
from django.contrib.auth import get_user_model
from django.db.models import Q
from user_page.models import OnlineUser
from .models import Message, Room, IsUserInChat, IsUserInRoomsPage
from django.core.exceptions import ObjectDoesNotExist
from random import randint

User = get_user_model()

@channel_session_user_from_http
def ws_connect(message, room_name):
    rr = Room.objects.get(id=room_name)
    message.channel_session['room'] = room_name
    Group("chat-%s" % room_name).add(message.reply_channel)
    message.reply_channel.send({"accept": True})
    q_user = User.objects.get(id=message.channel_session['_auth_user_id'])
    if q_user.logged_in_user.online == True:
        pass
    else:
        ol = OnlineUser(user = q_user, online = True)
        ol.save()

    try:
        is_user_in_chat = IsUserInChat.objects.get(user=q_user)
    except ObjectDoesNotExist:
        is_user_in_chat = IsUserInChat.objects.create(user = q_user, in_chat=True, room_id=rr)
        is_user_in_chat.save()
    try:
        is_user_in_chat = IsUserInChat.objects.get(user=q_user, in_chat=True, room_id=rr)
    except ObjectDoesNotExist:
        is_user_in_chat.in_chat = True
        is_user_in_chat.room_id = rr
        is_user_in_chat.save()

    if rr.f_usr.id == q_user.id:
        rr.f_in_chat = True
        rr.save()
        if q_user.user_in_chat.in_chat == True and q_user.user_in_chat.room_id == rr:
            Group("chat-%s" % room_name).send({"text": json.dumps({'q1': 'f_usr' }) })
    elif rr.s_usr.id == q_user.id:
        rr.s_in_chat = True
        rr.save()
        if q_user.user_in_chat.in_chat == True and q_user.user_in_chat.room_id == rr:
            Group("chat-%s" % room_name).send({"text": json.dumps({'q2': 's_usr' })})



@channel_session_user
def websocket_receive(message, room_name):
    global m_count
    m_count = 0
    rr = Room.objects.get(id = room_name)
    q_user = User.objects.get(id= message.channel_session['_auth_user_id'])
    if rr.f_usr.id == q_user.id:
        if rr.s_in_chat == True:
            Group("chat-%s" % room_name).send({"text": json.dumps({'f_usr': rr.f_usr.id, 'u': rr.f_usr.username,
                'm': message.content['text'], }) })
            Message.objects.create(fk=q_user, text=message.content['text'], room=rr, saw=True)
        else:
            Group("chat-%s" % room_name).send({"text": json.dumps({'f_usr': rr.f_usr.id, 'u': rr.f_usr.username,
                'm': message.content['text'], 'unseen': " (непрочитано) ",}) })
            Message.objects.create(fk=q_user, text=message.content['text'], room=rr, saw=False)
            try:
                user_rooms = Room.objects.filter(Q(f_usr=rr.s_usr) | Q(s_usr=rr.s_usr))
                for room in user_rooms:
                    try:
                        m = room.message.last()
                        if m.fk != rr.s_usr and m.saw == False:
                            global m_count
                            m_count += 1
                    except:
                        pass

                mm = rr.message.last()
                if mm.fk != rr.s_usr and mm.saw == False:
                    count_count = randint(0, 10000)
                    try:
                        if rr.s_usr.user_in_chat.in_chat == True:
                            s_usr_in_chat = True
                        else:
                            s_usr_in_chat = False
                    except:
                        s_usr_in_chat = False
                    try:
                        if rr.s_usr.user_in_rooms_page.in_rooms_page == True:
                            s_usr_in_rooms_page = True
                        else:
                            s_usr_in_rooms_page = False
                    except:
                        s_usr_in_rooms_page = False

                    if s_usr_in_chat == True:
                        Group("chat-%s" % rr.s_usr.user_in_chat.room_id.id).send({"text": json.dumps(
                            {'u': rr.f_usr.username, 'm': message.content['text'], 'c': m_count,'cc': count_count})})
                    elif s_usr_in_rooms_page == True:
                        Group("user-room-%s" % rr.s_usr.id).send({"text": json.dumps({'u': rr.f_usr.username,
                            'id': rr.f_usr.id,'m': message.content['text'],'c': m_count,'cc': count_count})})
                    else:
                        Group("user-%s" % rr.s_usr.id).send({"text": json.dumps({'u': rr.f_usr.username,
                            'm': message.content['text'], 'c': m_count, 'cc': count_count  }) })

                else:
                    global m_count
                    m_count += 1
                    count_count = randint(0, 10000)
                    try:
                        if rr.s_usr.user_in_chat.in_chat == True:
                            s_usr_in_chat = True
                        else:
                            s_usr_in_chat = False
                    except:
                        s_usr_in_chat = False
                    try:
                        if rr.s_usr.user_in_rooms_page.in_rooms_page == True:
                            s_usr_in_rooms_page = True
                        else:
                            s_usr_in_rooms_page = False
                    except:
                        s_usr_in_rooms_page = False

                    if s_usr_in_chat == True:
                        Group("chat-%s" % rr.s_usr.user_in_chat.room_id.id).send({"text": json.dumps(
                            {'u': rr.f_usr.username, 'm': message.content['text'], 'c': m_count,'cc': count_count})})
                    elif s_usr_in_rooms_page == True:
                        Group("user-room-%s" % rr.s_usr.id).send({"text": json.dumps({'u': rr.f_usr.username,
                            'id': rr.f_usr.id, 'm': message.content['text'], 'c': m_count,'cc': count_count})})
                    else:
                        Group("user-%s" % rr.s_usr.id).send({"text": json.dumps({'u': rr.f_usr.username,
                            'm': message.content['text'], 'c': m_count, 'cc': count_count  }) })
            except:
                pass

    elif rr.s_usr.id == q_user.id:
        if rr.f_in_chat == True:
            Group("chat-%s" % room_name).send({"text": json.dumps({'s_usr': rr.s_usr.id, 'u': rr.s_usr.username,
                'm': message.content['text'], }) })
            Message.objects.create(fk=q_user, text=message.content['text'], room=rr, saw=True)
        else:
            Group("chat-%s" % room_name).send({"text": json.dumps({'s_usr': rr.s_usr.id, 'u': rr.s_usr.username,
                'm': message.content['text'], 'unseen': " (непрочитано) ", }) })
            Message.objects.create(fk=q_user, text=message.content['text'], room=rr, saw=False)
            try:
                user_rooms = Room.objects.filter(Q(f_usr=rr.f_usr) | Q(s_usr=rr.f_usr))
                for room in user_rooms:
                    try:
                        m = room.message.last()
                        if m.fk != rr.f_usr and m.saw == False:
                            global m_count
                            m_count += 1
                    except:
                        pass

                mm = rr.message.last()
                if mm.fk != rr.f_usr and mm.saw == False:
                    count_count = randint(0, 10000)
                    try:
                        if rr.f_usr.user_in_chat.in_chat == True:
                            f_usr_in_chat = True
                        else:
                            f_usr_in_chat = False
                    except:
                        f_usr_in_chat = False
                    try:
                        if rr.f_usr.user_in_rooms_page.in_rooms_page == True:
                            f_usr_in_rooms_page = True
                        else:
                            f_usr_in_rooms_page = False
                    except:
                        f_usr_in_rooms_page = False

                    if f_usr_in_chat == True:
                        Group("chat-%s" % rr.f_usr.user_in_chat.room_id.id).send({"text": json.dumps(
                            {'u': rr.s_usr.username, 'm': message.content['text'], 'c': m_count,'cc': count_count})})
                    elif f_usr_in_rooms_page == True:
                        Group("user-room-%s" % rr.f_usr.id).send({"text": json.dumps({'u': rr.s_usr.username,
                            'id': rr.s_usr.id, 'm': message.content['text'], 'c': m_count, 'cc': count_count})})
                    else:
                        Group("user-%s" % rr.f_usr.id).send({"text": json.dumps({'u': rr.s_usr.username,
                            'm': message.content['text'], 'c': m_count, 'cc': count_count})})
                else:
                    global m_count
                    m_count += 1
                    count_count = randint(0, 10000)
                    try:
                        if rr.f_usr.user_in_chat.in_chat == True:
                            f_usr_in_chat = True
                        else:
                            f_usr_in_chat = False
                    except:
                        f_usr_in_chat = False
                    try:
                        if rr.f_usr.user_in_rooms_page.in_rooms_page == True:
                            f_usr_in_rooms_page = True
                        else:
                            f_usr_in_rooms_page = False
                    except:
                        f_usr_in_rooms_page = False

                    if f_usr_in_chat == True:
                        Group("chat-%s" % rr.f_usr.user_in_chat.room_id.id).send({"text": json.dumps(
                            {'u': rr.s_usr.username, 'm': message.content['text'], 'c': m_count,'cc': count_count})})
                    elif f_usr_in_rooms_page == True:
                        Group("user-room-%s" % rr.f_usr.id).send({"text": json.dumps({'u': rr.s_usr.username,
                            'id': rr.s_usr.id, 'm': message.content['text'], 'c': m_count, 'cc': count_count})})
                    else:
                        Group("user-%s" % rr.f_usr.id).send({"text": json.dumps({'u': rr.s_usr.username,
                            'm': message.content['text'], 'c': m_count, 'cc': count_count})})
            except:
                pass


@channel_session_user
def ws_disconnect(message, room_name):
    rr = Room.objects.get(id=room_name)
    q_user = User.objects.get(id=message.channel_session['_auth_user_id'])
    if rr.f_usr.id == q_user.id:
        rr.f_in_chat = False
        rr.save()
    elif rr.s_usr.id == q_user.id:
        rr.s_in_chat = False
        rr.save()
    is_user_in_chat = IsUserInChat.objects.get(user=q_user)
    is_user_in_chat.in_chat = False
    is_user_in_chat.save()

    ol = OnlineUser(user = q_user, online = False)
    ol.save()
    Group("chat-%s" % room_name).discard(message.reply_channel)

@channel_session_user_from_http
def ws_room_conn(message, some_user):
    message.reply_channel.send({"accept": True})
    q_user = User.objects.get(id=message.channel_session['_auth_user_id'])
    Group("user-room-%s" % some_user).add(message.reply_channel)
    if q_user.logged_in_user.online == True:
        pass
    else:
        ol = OnlineUser(user = q_user, online = True)
        ol.save()
    try:
        is_user_in_room_page = IsUserInRoomsPage.objects.get(user=q_user)
    except ObjectDoesNotExist:
        is_user_in_room_page = IsUserInRoomsPage.objects.create(user = q_user, in_rooms_page=True)
        is_user_in_room_page.save()
    try:
        is_user_in_room_page = IsUserInRoomsPage.objects.get(user=q_user, in_rooms_page=True)
    except ObjectDoesNotExist:
        is_user_in_room_page.in_rooms_page = True
        is_user_in_room_page.save()


@channel_session_user
def ws_room_dis(message, some_user):
    q_user = User.objects.get(id=message.channel_session['_auth_user_id'])
    is_user_in_room_page = IsUserInRoomsPage.objects.get(user=q_user)
    is_user_in_room_page.in_rooms_page = False
    is_user_in_room_page.save()

    ol = OnlineUser(user = q_user, online = False)
    ol.save()
    Group("user-room-%s" % some_user).discard(message.reply_channel)
