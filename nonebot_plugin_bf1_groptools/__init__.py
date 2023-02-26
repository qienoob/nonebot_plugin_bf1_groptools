from nonebot import on_request, on_notice
from nonebot.adapters.onebot.v11 import MessageSegment, Event, Bot, GroupRequestEvent, GroupIncreaseNoticeEvent
import requests, re

dict1 = {}

def _check0(event: Event):
    return isinstance(event, GroupRequestEvent)


requ = on_request(rule=_check0)

@requ.handle()
async def _(event: GroupRequestEvent, bot: Bot):
    usrname = event.comment
    usrname = re.findall(re.compile('答案：(.*)'), usrname)
    url_uid = f"https://api.gametools.network/bf1/player?name={usrname[0]}&platform=pc&skip_battlelog=false"
    uid_json = requests.get(url_uid, verify=False)
    if uid_json.status_code == 200:
        global dict1
        dict1['qid'] = event.user_id
        dict1['usrname'] = usrname[0]
        await bot.call_api("set_group_add_request", flag=event.flag, sub_type=event.sub_type, approve=True)
        await requ.finish()
    else:
        await bot.call_api("set_group_add_request", flag=event.flag, sub_type=event.sub_type,
                           approve=False, reason='id认证错误，请检查您输入的是否为游戏内id')
        await requ.finish()
        

        
def _check1(event: Event):
    return isinstance(event, GroupIncreaseNoticeEvent)

incr = on_notice(rule=_check1)
@incr.handle()
async def _(event: GroupIncreaseNoticeEvent, bot: Bot, ):
    if event.user_id == dict1['qid']:
        usrname = dict1['usrname']
        await bot.set_group_card(group_id=event.group_id, user_id=event.user_id, card=usrname)
        await bot.send_group_msg(group_id=event.group_id, message=
        MessageSegment.at(event.user_id)+MessageSegment.text(f'\n\n欢迎加入，已将您的群名片改为您的游戏名称:{usrname}'))
        await incr.finish()
    else:
        await incr.finish()


















