from channels import route
from .consumers import ws_conn, ws_dis

user_page_routing = [
    route("websocket.connect", ws_conn),
    route("websocket.disconnect", ws_dis),
]