
from channels import route
from .consumers import ws_connect, websocket_receive, ws_disconnect, ws_room_conn, ws_room_dis#, ws_room_mess

chat_routing = [
    route("websocket.connect", ws_connect),
    route("websocket.receive", websocket_receive),
    route("websocket.disconnect", ws_disconnect),
]

chat_room_routing = [
    route("websocket.connect", ws_room_conn),
    route("websocket.disconnect", ws_room_dis),
]