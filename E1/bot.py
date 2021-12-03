import asyncio

from graia.ariadne.app import Ariadne
from graia.ariadne.model import MiraiSession
from graia.broadcast import Broadcast
from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour

loop = asyncio.new_event_loop()

bcc = Broadcast(loop=loop)
app = Ariadne(
    broadcast=bcc,
    connect_info=MiraiSession(
        host="http://localhost:8086",
        verify_key="tdtogkf123",
        account=2119799445,
    ),
)
saya = Saya(bcc)
saya.install_behaviours(BroadcastBehaviour(bcc))

with saya.module_context():
    saya.require("setu")


if __name__ == "__main__":
    try:
        loop.run_until_complete(app.lifecycle())
    except KeyboardInterrupt:
        loop.run_until_complete(app.request_stop())
