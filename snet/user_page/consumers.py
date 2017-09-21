from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from django.contrib.auth import get_user_model
from .models import OnlineUser

User = get_user_model()

@channel_session_user_from_http
def ws_conn(message, some_user):
    message.reply_channel.send({"accept": True})
    Group("user-%s" % some_user).add(message.reply_channel)
    try:
        usr = User.objects.get(id = some_user)
        if usr.logged_in_user.online == True:
            pass
        else:
            ol = OnlineUser(user = usr, online = True)
            ol.save()
    except:
        pass

@channel_session_user
def ws_dis(message, some_user):
    usr = User.objects.get(id = some_user)
    ol = OnlineUser(user = usr, online = False)
    ol.save()
    Group("user-%s" % some_user).discard(message.reply_channel)
