from channels import include

channel_routing = [
    include("chat.routing.chat_routing", path=r"^/chat/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    include("chat.routing.chat_room_routing", path=r"^/user_rooms/(?P<some_user>[a-zA-Z0-9_]+)/$"),
    include("user_page.routing.user_page_routing", path=r"^/user_page/(?P<some_user>[a-zA-Z0-9_]+)/$"),
]



