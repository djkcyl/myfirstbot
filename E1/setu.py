import httpx
import random
import asyncio

from datetime import datetime
from graia.saya import Saya, Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group, Member
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.parser.twilight import Sparkle, Twilight
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.pattern import FullMatch, WildcardMatch
from graia.ariadne.message.element import Forward, ForwardNode, Image, Plain


saya = Saya.current()
channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[
            Twilight(
                Sparkle(
                    matches={
                        "tag1": WildcardMatch(optional=True),
                        "header": FullMatch("涩图"),
                        "tag2": WildcardMatch(optional=True),
                    },
                )
            )
        ],
    )
)
async def setu(app: Ariadne, group: Group, tag1: WildcardMatch, tag2: WildcardMatch):

    if tag1.matched or tag2.matched:
        tag = tag1.result.asDisplay() if tag1.matched else tag2.result.asDisplay()
        url = f"http://a60.one:404/get/tags/{tag}"
    else:
        url = "http://a60.one:404/"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params={"num": 5})

    data = resp.json()

    member_list = await app.getMemberList(group)
    fwd_nodeList = []
    for imgs in data["data"]["imgs"]:
        random_member: Member = random.choice(member_list)
        fwd_nodeList.append(
            ForwardNode(
                senderId=random_member.id,
                time=datetime.now(),
                senderName=random_member.name,
                messageChain=MessageChain.create(
                    Plain(f"\n标题：{imgs['name']}\n"), Image(url=imgs["url"])
                ),
            )
        )
    message = MessageChain.create(Forward(nodeList=fwd_nodeList))
    send_message = await app.sendGroupMessage(group, message)
    await asyncio.sleep(10)
    await app.recallMessage(send_message)
