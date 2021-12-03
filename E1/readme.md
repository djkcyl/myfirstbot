> 使用场景，在群里发送“涩图”指令后 Bot 向群内返回涩图。

本例子内涉及内容
1. Poetry 虚拟容器的基础使用
2. Airadne Bot 创建及与 `MAH` 连接
3. 创建一个**群消息**监听器
4. 使用 `Twilight` 进行消息匹配
5. 基础的 `async` 用法
6. 使用 `httpx` 模块异步获取网络内容
7. 解析 `json/dict` 数据
8. 获取群内成员列表
9. 使用 `randon` 随机挑选列表内的内容
10. 消息链构建
11. 转发消息及转发节点构建
12. 图片，文字以及 At 等消息元素的使用
13. 发送群消息
14. 使用 `asyncio` 进行异步延时 (sleep)
15. 撤回群消息
16. 使用 `graia-saya` 将此功能插件化

**注：本例子默认你掌握了 Python 基础**

废话不多说，让我们开始吧 ~

> 本教程默认你已经拥有一个正确部署的 `MAH` 可供使用
#
## 首先，创建一个适合的虚拟容器
```shell
mkdir myfirstbot
cd myfirstbot
poetry init
```
此时，如果你没有特殊的需要，可直接回车至此处
```shell
root@A60-Server:/A60/myfirstbot# poetry init

This command will guide you through creating your pyproject.toml config.

Package name [myfirstbot]:  
Version [0.1.0]:  
Description []:  
Author [djkcyl <cyl@cyllive.cn>, n to skip]:  
License []:  
Compatible Python versions [^3.8]:  
```
选择你需要的 Python 版本，例如 `^3.8` 或 `^3.9` ，这里我们选择 `^3.9` 。

紧接着，Poetry 会询问你是否需要定义依赖，由于国内网络访问 PyPi 的情况较差，我们输入 no 直接跳过。
```shell
Would you like to define your main dependencies interactively? (yes/no) [yes] no
Would you like to define your development dependencies interactively? (yes/no) [yes] no
```
然后输入 yes 即可完成 Poetry 环境初始化
```shell
Generated file

[tool.poetry]
name = "myfirstbot"
version = "0.1.0"
description = ""
authors = ["djkcyl <cyl@cyllive.cn>"]

[tool.poetry.dependencies]
python = "^3.9"

[tool.poetry.dev-dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"


Do you confirm generation? (yes/no) [yes] yes
```
> 由于大陆区域的网络问题，为了防止后续的包解析及安装等待时间过长，可以预先修改项目根目录下的 `pyproject.toml` 来添加国内镜像加速站，打开该文件后在文件末尾添加如下内容
> ```toml
> [[tool.poetry.source]]
> name = "tsinghua"
> url = "https://pypi.tuna.tsinghua.edu.cn/simple"
> default = true
> ```
当然，仅有一个环境是不够的，我们还需要向环境内安装我们需要的 `Graia Airadne` 及其他依赖，不过在此之前，还需要先将容器创建出来。
```shell
poetry env use 3.9
poetry add graia-ariadne
```
将返回类似如下的内容
> 你看到的返回内容并不一定与示例中的内容完全相同
```shell
# poetry env use 3.9

Creating virtualenv myfirstbot-BexBd8Xq-py3.9 in /root/.cache/pypoetry/virtualenvs
Using virtualenv: /root/.cache/pypoetry/virtualenvs/myfirstbot-BexBd8Xq-py3.9
```
```shell
# poetry add graia-ariadne

Using version ^0.4.7 for graia-ariadne

Updating dependencies
Resolving dependencies... (38.9s)

Writing lock file

Package operations: 14 installs, 0 updates, 0 removals

  • Installing frozenlist (1.2.0)
  • Installing idna (3.3)
  • Installing multidict (5.2.0)
  • Installing typing-extensions (3.10.0.2)
  • Installing aiosignal (1.2.0)
  • Installing async-timeout (4.0.1)
  • Installing attrs (21.2.0)
  • Installing charset-normalizer (2.0.8)
  • Installing yarl (1.7.2)
  • Installing aiohttp (3.8.1)
  • Installing graia-broadcast (0.14.3)
  • Installing loguru (0.5.3)
  • Installing pydantic (1.8.2)
  • Installing graia-ariadne (0.4.7)
```

## 快速开始
接着，按照 [快速开始](https://graia.readthedocs.io/zh_CN/latest/quickstart/) 内的方法快速创建一个 Ariadne 实例


首先创建一个名为 bot.py 的文件，输入如下内容
```python
import asyncio

from graia.broadcast import Broadcast

from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.model import Friend, MiraiSession

loop = asyncio.new_event_loop()

bcc = Broadcast(loop=loop)
app = Ariadne(
    broadcast=bcc,
    connect_info=MiraiSession(
        host="http://localhost:8080",
        verify_key="A60FirstExample",
        account=123456789,
        # 此处的内容请按照你的 MAH 配置来填写
    ),
)


@bcc.receiver("FriendMessage")
async def setu(app: Ariadne, friend: Friend):
    await app.sendMessage(friend, MessageChain.create([Plain("Hello, World!")]))


loop.run_until_complete(app.lifecycle())

```
让我们启动它来看看吧！
```shell
poetry run python bot.py
```
```shell
# poetry run python bot.py
2021-12-03 10:47:47.328 | INFO     | graia.ariadne.app:launch:1264 - Launching app...
2021-12-03 10:47:47.328 | INFO     | graia.ariadne.app:launch:1268 - 
                _           _            
     /\        (_)         | |           
    /  \   _ __ _  __ _  __| |_ __   ___ 
   / /\ \ | '__| |/ _` |/ _` | '_ \ / _ \
  / ____ \| |  | | (_| | (_| | | | |  __/
 /_/    \_\_|  |_|\__,_|\__,_|_| |_|\___|

2021-12-03 10:47:47.329 | INFO     | graia.ariadne.app:launch:1277 - graia-ariadne version: 0.4.7
2021-12-03 10:47:47.330 | INFO     | graia.ariadne.app:launch:1277 - graia-broadcast version: 0.14.3
2021-12-03 10:47:47.331 | INFO     | graia.ariadne.app:launch:1277 - graia-scheduler version: Not Found / Installed
2021-12-03 10:47:47.331 | INFO     | graia.ariadne.app:launch:1277 - graia-saya version: Not Found / Installed
2021-12-03 10:47:47.331 | DEBUG    | graia.ariadne.app:daemon:1192 - Ariadne daemon started.
2021-12-03 10:47:47.385 | INFO     | graia.ariadne.adapter:fetch_cycle:367 - websocket: connected
2021-12-03 10:47:47.386 | INFO     | graia.ariadne.adapter:fetch_cycle:372 - websocket: ping task created
2021-12-03 10:47:47.386 | DEBUG    | graia.ariadne.adapter:ws_ping:295 - websocket: ping
2021-12-03 10:47:47.386 | DEBUG    | graia.ariadne.adapter:ws_ping:299 - websocket: ping success, delay 30.0s
2021-12-03 10:47:47.399 | DEBUG    | graia.ariadne.adapter:fetch_cycle:391 - websocket: received pong
2021-12-03 10:47:47.477 | INFO     | graia.ariadne.app:launch:1286 - Remote version: 2.3.3
2021-12-03 10:47:47.477 | INFO     | graia.ariadne.app:launch:1289 - Application launched with 0.15s
```

此时，我们的 Bot 已经成功启动了，向你的 Bot 发送一条消息试试看吧
```shell
2021-12-03 10:49:45.350 | INFO     | graia.ariadne.model:log_friend_message:114 - 2119799445: [A60(2948531755)] -> '你好！'
2021-12-03 10:49:45.478 | INFO     | graia.ariadne.app:sendFriendMessage:114 - [BOT 2119799445] Friend(2948531755) <- Hello, World!
```

[!P1](pic/p1.png)

现在，它已经可以在收到任意私聊消息的时候回复 Hello World 了，但当然，这并不是我们想要的，我们先将私聊消息的监听器 `"FriendMessage"` 修改为 `GroupMessage` 并删除 `friend: Friend`

```python
...
from graia.ariadne.event.message import GroupMessage
...


...
@bcc.receiver(GroupMessage)
async def friend_message_listener(app: Ariadne):
    await app.sendMessage(friend, MessageChain.create([Plain("Hello, World!")]))
...
```
重新启动 Bot ，此时 Bot 将监听任意群聊的任意消息并回复 Hello World，但我们想要的效果是收到指令 `涩图` 后才触发消息，所以我们需要添加消息匹配器 `Twilight` 来精准的匹配到群友发送的 `涩图` 指令。

首先在合适的位置导入 `Twilight` 并创建一个可以精准匹配指令 `涩图` 的匹配器
```python
...
from graia.ariadne.model import Group
from graia.ariadne.message.parser.twilight import Twilight, Sparkle
from graia.ariadne.message.parser.pattern import FullMatch
...

```

使用 Bcc 的 dispatchers 来让我们的群消息监听器来使用消息匹配器，添加并修改如下内容
```python
...
@bcc.receiver(GroupMessage, dispatchers=[Twilight(Sparkle([FullMatch("涩图")]))])
async def setu(app: Ariadne, group: Group):
    await app.sendMessage(group, MessageChain.create([Plain("Hello, World!")]))
...
```
此时再向群内发送**其他**消息 Bot 将不会继续回复 Hello World 了。

[!P2](pic/p2.png)

这样，我们的消息匹配部分以及群消息发送就大功告成了，接着实现剩下的需求

## 获取涩图并发送

既然我们是涩图功能，当然不能一直发 Hello World，下面我们来尝试从 A60 LoliconMirror 获取涩图并发送

首先安装一个新的第三方依赖 `httpx` 用于快捷的异步访问网络资源
```shell
poetry add httpx
```
在 Bot 里导入该依赖
```python
import httpx
...
```

创建一个异步的 httpx 实例并访问 A60 LoliconMirror
```python
...
@bcc.receiver(GroupMessage, dispatchers=[Twilight(Setu)])
async def setu(app: Ariadne, group: Group):
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://a60.one:404/")
...
```
但由于我们并不知道访问该 Api 后会返回什么内容，所以我们可以试着创建一个新的 test.py 来进行测试，当然，用于测试就不需要使用异步了~~（其实是我懒~~

先将返回的 text 内容打印出来看看
```python
import httpx

resp = httpx.get("http://a60.one:404/")
print(resp.text)
```
```json
# poetry run python text.py

{"code":200,"data":{"imgs":[{"id":9128,"pic":"74927386_p2","name":"アズレン落書詰め","tags":"アズールレーン,碧蓝航线,時雨(アズールレーン),Shigure (Azur Lane),狼耳,wolf ears,アズールレーン500users入り,Azur Lane 500+ bookmarks","userid":18395363,"username":"蝉丸せみ","sanity_level":4,"url":"https://pic.a60.one:8443/74927386_p2.jpg"}]},"time":"10ms"}
```
我们可以很清楚的看到，这是一个 json 结构的内容，这样我们可以利用 httpx 的 `.json()` 来快速的将获取到的响应体转换为 Python 能用的 Dict 类型，也为了后续的方便使用，将修改内容为
```python
data = resp.json()
print(data)
```
这样就可以继续下面的内容了

让我们来看看这段 Dict 里的内容
| 字段 | 类型 | 说明                                       |
| ---- | ---- | ------------------------------------------ |
| code | int  | 状态代码                                   |
| data | dict | 这是一个 Dict 里面包含了我们需要的所有内容 |
| time | str  | 查询时长                                   |

在分析 data 内的内容后得到以下数据
| 字段 | 类型 | 说明   |
| ---- | ---- | ------ |
| imgs | List | 图片们 |

进一步分析 imgs 可以得到
| 字段         | 类型 | 说明             |
| ------------ | ---- | ---------------- |
| id           | int  | 数据库 id        |
| pic          | str  | 作品 id          |
| name         | str  | 作品标题         |
| tags         | str  | 作品标签         |
| userid       | int  | 作者 uid         |
| username     | str  | 作者名           |
| sanity_level | int  | Pixiv 的涩情判定 |
| url          | str  | 图片地址         |

我们只需要其中的 name 及 urls 即可
```python
pic_name = data["data"]["imgs"][0]["name"]
pic_url = data["data"]["imgs"][0]["url"]

print(pic_name, pic_url)
```
执行后可用看到已经达到了我们的需求
```shell
# poetry run python test.py

アズレン落書詰め https://pic.a60.one:8443/74927386_p2.jpg
```

接着我们吧这些内容放到我们的 Bot 中去并且创建一个可以用于发送的消息链，当然，我们也需要导入用于发送图片以及At的对应元素和类
```python
...
from graia.ariadne.message.element import At, Plain, Image
from graia.ariadne.model import Friend, Group, MiraiSession, Member
...


...
async def setu(app: Ariadne, group: Group, member: Member):
...


...
    setu_message = MessageChain.create(
        At(member.id), Plain(f"\n标题：{pic_name}\n"), Image(url=pic_url)
    )
...
```
消息链构建好了，接着就可以调用 app 内的 `sendGroupMessage` 来发送群消息了
```python
...
    await app.sendGroupMessage(group, setu_message)
...
```

然后我们再次运行 Bot 去群里看看结果吧！

[!P3](pic/p3.png)

## 更多的玩法

可以看到我们的bot已经成功的从 Api 获取了图片发送到群里并 At 了发送的人，现在我们的基础需求已经完成了，但这还不够，接着让我们来尝试通过构建 `Forward` 和 `ForwardNode` 来使用转发消息发送这些图片

要构建 `Forward` 和 `ForwardNode` 首先需要导入它们，由于转发节点需要我们输入时间，所以我们同时将 `datetime` 也进行导入
```python
...
from datetime import datetime

from graia.ariadne.message.element import At, Plain, Image, Forward, ForwardNode
...
```
然后开始构建，首选将我们上面已经构建好的 setu_message 添加至转发节点列表内，并创建一个新的消息链，将其添加进去

```python
    fwd_nodeList = [
            ForwardNode(
                senderId=member.id,
                time=datetime.now(),
                senderName=member.name,
                messageChain=setu_message,
            )
        ]
    message = MessageChain.create(Forward(nodeList=fwd_nodeList))
```
这时候我们的转发消息已经构建完成了，但只有一条消息怎么能叫转发消息呢，让我们发挥想象力，添加一些奇奇怪怪的功能，**用转发消息来模仿群友发涩图**。

需求：同时获取多张图片，用转发消息构建出假的消息链，从群内随机挑选幸运群友来充当“发涩图”的人

既然要随机挑选，当然少不了导入 `random`
```python
import random
...
```
从上面的测试我们可以看到，Api 一次仅会返回一张图片，但我们需要不止一张，我们有很多解决办法，例如多次访问这个 Api，不必这么麻烦，让我们来看看这个Api 的参数列表，打开 Api 的[文档](http://a60.one:404/docs)，可以看到通过设置 `num` 参数即可修改每次返回的图片数量

修改 `httpx` 部分的代码添加 `num` 参数，在 `get` 方法里添加 `params` ，内容为一个 dict
```python
...
        resp = await client.get("http://a60.one:404/", params={"num": 5})
...
```
继续使用之前的测试方法，得到以下数据
```json
{"code":200,"data":{"imgs":[{"id":25408,"pic":"86528808_p0","name":"bed","tags":"腋,腋下,バニーガール,兔女郎,獣耳,兽耳,魅惑のふともも,魅惑的大腿,コンドーム,避孕套,透けへそ,隐约入目的肚脐","userid":3386241,"username":"Romana","sanity_level":4,"url":"https://pic.a60.one:8443/86528808_p0.jpg"},{"id":23116,"pic":"85366357_p0","name":"ハロウィン⭐ナイト","tags":"オリジナル,原创,ハロウィン,万圣节,オリジナル7500users入り,原创7500收藏,ガオー,Roar","userid":1250474,"username":"鈍色玄@お仕事募集中","sanity_level":4,"url":"https://pic.a60.one:8443/85366357_p0.jpg"},{"id":30918,"pic":"89936471_p0","name":"ウェディングランジェリーネロちゃま","tags":"Fate/GrandOrder,命运－冠位指定,FGO,Fate/Grand Order,ネロ・クラウディウス(Fate),尼禄·克劳狄乌斯（Fate）,Fate/GO1000users入り,Fate/GO1000users加入书籤,腋,腋下","userid":10311630,"username":"kuro太","sanity_level":4,"url":"https://pic.a60.one:8443/89936471_p0.jpg"},{"id":23863,"pic":"85800239_p0","name":"バー","tags":"バーバラ,芭芭拉,原神,Genshin Impact,バーバラ(原神),芭芭拉（原神）,芭芭拉,Barbara,白タイツ,白裤袜,ソックス足裏,着袜足底,原神50000users入り,原神50000收藏","userid":8129277,"username":"Sak","sanity_level":2,"url":"https://pic.a60.one:8443/85800239_p0.jpg"},{"id":15818,"pic":"80518296_p5","name":"ユニちゃんズ。。　よろしく","tags":"女の子,女孩子,プリコネR,公主连结,ユニ(プリコネ),尤妮（公主连结）,仲良し部,プリンセスコネクト!Re:Dive,公主连结Re:Dive,おっぱい,欧派,白タイツ,白裤袜,タイツ,裤袜,おへそ,肚脐,プリコネ1000users入り,Princess Connect! 1000+ bookmarks","userid":27350443,"username":"Leviathan","sanity_level":4,"url":"https://pic.a60.one:8443/80518296_p5.jpg"}]},"time":"10ms"}
```
根据之前的分析，我们得知这次的 `imgs` 内包含了 5 张图片，让我们将它们都添加至转发消息里吧

首先当然需要先获取群内的人员列表
```python
...
    member_list = await app.getMemberList(group)
...
```
然后让我们来向转发消息里添加这些东西

```python
...
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
    await app.sendGroupMessage(group, message)
...
```

启动 Bot 试试吧

[!P4](pic/p4.png)

可以看到，假消息链已经构建出来了，让我们再添加一些更多的内容

需求：通过 tag 来搜索相应的内容

在 Api 文档内，包含了通过 tag 来搜索相应图片的功能 `/get/tags/` ，得好好利用一下

上文我们创建的消息匹配器内，使用了 `FullMatch` ，意味着除了 `涩图` 外的指令都不进行匹配，那我们如何获取到 tag 呢，这里就要用到 `WildcardMatch` 了，先导入它
```python
...
from graia.ariadne.message.parser.pattern import FullMatch, WildcardMatch
...
```
修改之前的匹配器为下面这样，详细的使用方法可以查看 Twilight 的文档

当然，代码也需要大幅修改
```python
...
@bcc.receiver(
    GroupMessage,
    dispatchers=[
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
    await app.sendGroupMessage(group, message)
...
```
发送完消息，是不是也可以在一定时间后撤回呢，当然可以，但我们需要先获取到需要撤回的消息id，app.sendGroupMessage() 在执行完毕后会返回这条消息的id，我们可以通过创建一个变量为其赋值来获取到
```python
    send_message = await app.sendGroupMessage(group, message)
```
这个变量有且仅有一个参数 `messageId` ，让我们等待几秒后撤回该条消息。

注意：在异步程序里，请使用 `asyncio.sleep()` 来代替 `sleep()` ，否则你的程序将会被 `sleep()` 阻塞

```python
    await asyncio.sleep(10)
    await app.recallMessage(send_message)
```

再次运行你的 Bot 检验下是否可以使用了吧！

[!P5](pic/p5.png)


## 将功能模块化

在上面，我们将功能都添加在 bot.py 里，那么设想一下，如果所有的功能都写在一起，整个项目的可读性将非常差，那么有没有什么方法可以将每一个单独的功能都做成单独的模块呢，当然可以， `graia-saya` 提供了这样的模块管理功能

首先我们需要安装它
```shell
poetry add graia-saya
```

接着在 boy.py 中引用它们
```python
...
from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour
...
```

在 Broadcast 实例后创建 Saya 实例
```python
saya = Saya(bcc)
```

接着创建 BroadcastBehaviour 实例，并将其注册到现有的 Saya 实例中
```python
saya.install_behaviours(BroadcastBehaviour(bcc))
```

创建一个新的 setu.py 文件，将其制作为 Saya 需要的样子
```python
from graia.saya import Saya, Channel

saya = Saya.current()
channel = Channel.current()
```

接下来, 导入 ListenerSchema
```python
...
from graia.saya.builtins.broadcast.schema import ListenerSchema
...
```

在上文，我们通过 @bcc.receiver 来监听群消息事件，Saya 里需要使用 @channel.use 当然用法也与上文不同。
```python
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def module_listener():
    pass
```

这样，我们的模块就创建完成了，让我们在 Bot 中加载它
```python
with saya.module_context():
    saya.require("setu")
```

接着，把我们上面写的功能搬过来并进行一些小的改动
```python
import httpx
import random
import asyncio

from datetime import datetime
from graia.saya import Saya, Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group, Member
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.twilight import Sparkle, Twilight
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

```

删掉一些不需要的引用，并为程序添加对 KeyboardInterrupt 的捕捉
```python
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
        host="http://localhost:8080",
        verify_key="A60FirstExample",
        account=123456789,
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

```
再次启动 Bot 后可得到以下结果
```shell
# poetry run python E1/bot.py

2021-12-03 16:51:30.414 | DEBUG    | graia.saya:require:111 - require setu
2021-12-03 16:51:30.492 | INFO     | graia.saya:require:134 - module loading finished: setu
2021-12-03 16:51:30.492 | INFO     | graia.ariadne.app:launch:1264 - Launching app...
2021-12-03 16:51:30.492 | INFO     | graia.ariadne.app:launch:1268 - 
                _           _            
     /\        (_)         | |           
    /  \   _ __ _  __ _  __| |_ __   ___ 
   / /\ \ | '__| |/ _` |/ _` | '_ \ / _ \
  / ____ \| |  | | (_| | (_| | | | |  __/
 /_/    \_\_|  |_|\__,_|\__,_|_| |_|\___|

2021-12-03 16:51:30.493 | INFO     | graia.ariadne.app:launch:1277 - graia-ariadne version: 0.4.7
2021-12-03 16:51:30.494 | INFO     | graia.ariadne.app:launch:1277 - graia-broadcast version: 0.14.3
2021-12-03 16:51:30.494 | INFO     | graia.ariadne.app:launch:1277 - graia-scheduler version: Not Found / Installed
2021-12-03 16:51:30.495 | INFO     | graia.ariadne.app:launch:1277 - graia-saya version: 0.0.13
2021-12-03 16:51:30.495 | DEBUG    | graia.ariadne.app:daemon:1192 - Ariadne daemon started.
2021-12-03 16:51:30.498 | INFO     | graia.ariadne.adapter:fetch_cycle:367 - websocket: connected
2021-12-03 16:51:30.498 | INFO     | graia.ariadne.adapter:fetch_cycle:372 - websocket: ping task created
2021-12-03 16:51:30.499 | DEBUG    | graia.ariadne.adapter:ws_ping:295 - websocket: ping
2021-12-03 16:51:30.499 | DEBUG    | graia.ariadne.adapter:ws_ping:299 - websocket: ping success, delay 30.0s
2021-12-03 16:51:30.499 | DEBUG    | graia.ariadne.adapter:fetch_cycle:391 - websocket: received pong
2021-12-03 16:51:30.503 | INFO     | graia.ariadne.app:launch:1286 - Remote version: 2.3.3
2021-12-03 16:51:30.504 | INFO     | graia.ariadne.app:launch:1289 - Application launched with 0.011s
```

可用看到前两行
```shell
2021-12-03 16:51:30.414 | DEBUG    | graia.saya:require:111 - require setu
2021-12-03 16:51:30.492 | INFO     | graia.saya:require:134 - module loading finished: setu
```
Airadne 成功加载了我们刚才创建的 Saya 插件

到此为止，本示例就结束了。