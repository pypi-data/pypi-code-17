#!/usr/bin/env python3
# coding: utf-8

from wxpy import *
import re

#    variables   #
when = 'no time'
what = 'nothing'
who = 'somebody?'
eventDate = '2017.3.6'
dateNow = '2017.3.5'
todayOrTommrrow = 'today'
roughData = '没活动'

#####  bots  #####
bot = Bot()
tulingBot = Tuling(api_key='dd9c07a83af145c3aa72fe3261959e23')

#   setup for person and @ingroups #
allFriends = bot.friends()

@bot.register(allFriends, except_self=False)  # except_self default is True
def auto_reply(msg):
    global roughData
    global when
    global what
    global who
    if not (isinstance(msg.sender, Group) and not msg.is_at):  # don't reply group unless @
        print('{}'.format(msg.receiver))
        message = msg.text
        senderName = msg.sender.remark_name
        print('testit 1')
        if len(senderName) < 1:
            receiverFull = '{}'.format(msg.receiver)
            print(receiverFull)
            if not len(receiverFull) < 1:
                self = receiverFull.partition(' ')[2]
                self = self[:-1]
                senderName = self
            else:
                senderName = 'botOwner'
        if senderName == '约吧':
            senderName = 'botOwner'
        print('{}:'.format(senderName))
        print(message)
        if message == '约':  # 查看
            print('testit 2')
            if when == 'no time':
                return '［还没人创建活动!  输入“约 时间 活动”譬如：“约 7am Overwatch”来创建活动］'
            else:
                return '［{}点,有{}一起干{}  //输入"约 {}"来参加活动］'.format(when, who, what, when)  # //输入 “约 时间” e.g. "约 7a"来参加活动
        elif (message.partition(' ')[0] == '约') and (len(msg.text) > 2):
            print('testit 3')
            roughData = message.partition(' ')[2]
            tokens = re.findall('\s+', roughData)
            spaceNo = 0
            for i in range(0, len(tokens)):
                spaceNo = spaceNo + len(tokens[i])
            if spaceNo == 1:  # 建立
                when = message.split(' ')[1]
                what = message.split(' ')[2]
                who = senderName
                #                print('{}'.format(chat.user_name))
                #                bot.create_group(users = chat.user_name)
                return '［好的，记下了, 约在: {}点, 干{}］'.format(when, what)
            elif spaceNo == 0:  # 参加
                if message.split(' ')[1] == when:
                    who = '{}&{}'.format(who, senderName)
                    print('{}'.format(senderName))
                    chat = bot.chats().search(senderName)[0]
                    yue_group.add_members(users=chat.user_name, use_invitation=True)
                    return '［你参加了{}点的{}，有{}］'.format(when, what, who)
                else:
                    return '［这个点儿没活动］'
            else:
                return '［格式不对呀，sb, 你这样写：邀约："约 7a Overwatch“ 参加：”约 7a“ 查看：“约”］'
        else:
            print('random message, reply with Tuling')
            return '[{}]'.format(tulingBot.reply_text(msg))
            #            return '[{}]'.format(tulingBot.reply_text(msg))
            #            return None
    else:
        print('message from group and I don\'t want to reply')
        return None


# setup for specific group   #
yue_group = bot.groups().search('约吧')[0]
@bot.register(yue_group, except_self=False)
def auto_reply(msg):
    global roughData
    global when
    global what
    global who
    print('testit 4')
    message = msg.text
    # member cut useless part
    memberFull = '{}'.format(msg.member)
    if not len(memberFull) < 1:
        member = memberFull.partition(' ')[2]
        member = member[:-1]
        senderName = member
    # self recognize
    if len(senderName) < 1:
        senderName = 'botOwner'
    print('{}:'.format(senderName))
    print(message)
    if message == '约':  # 查看
        print('testit 5')
        if when == 'no time':
            return '［还没人创建活动!  输入“约 时间 活动”譬如：“约 7am Overwatch”来创建活动］'
        else:
            return '［{}点,有{}一起干{}  //输入"约 {}"来参加活动］'.format(when, who, what, when)
    elif (message.partition(' ')[0] == '约') and (len(msg.text) > 2):
        roughData = message.partition(' ')[2]
        tokens = re.findall('\s+', roughData)
        spaceNo = 0
        for i in range(0, len(tokens)):
            spaceNo = spaceNo + len(tokens[i])
        if spaceNo == 1:  # 建立
            when = message.split(' ')[1]
            what = message.split(' ')[2]
            who = senderName
            return '［好的，记下了, 约在: {}点, 干{}］'.format(when, what)
        elif spaceNo == 0:  # 参加
            if message.split(' ')[1] == when:
                who = '{}&{}'.format(who, senderName)
                return '［你参加了{}点的{}，有{}］'.format(when, what, who)
            else:
                return '［这个点儿没活动］'
        else:
            return '［格式不对呀，sb, 你这样写：邀约："约 7a Overwatch Alex“ 参加：”约 7a Benson“ 查看：“约”］'
    else:
        print('random message in YUE ba function')
        return None


print("来约吧((((；ﾟДﾟ)))))))")


@bot.register(msg_types=CARD, except_self=False)
def reply_text(msg):
    print(msg.raw)
    msg.chat.send_raw_msg(msg.raw['MsgType'], msg.raw['Content'])

@bot.register(msg_types=FRIENDS)
# 自动接受验证信息中包含 'wxpy' 的好友请求
def auto_accept_friends(msg):
    # 判断好友请求中的验证文本
    new_friend = bot.accept_friend(msg.card)
    # new_friend.send('Hello, please check my Moments to see how does BroHelp work!')
    new_friend.send_image('pic.png')
    new_friend.send('https://goo.gl/forms/T4bv09npj5XEz9Es1')




bot.start()

