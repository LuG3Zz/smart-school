from user import *

usersRouter = APIRouter()


@usersRouter.post(path='/addmessage')
async def addmessage(messageconent: MessageConent,
                     user: UsernameRole = Depends(get_cure_user_by_token),
                     db: Session = Depends(get_db)):
    if len(messageconent.connect) > 500 or len(messageconent.connect) < 5:
        return reponse(code=100502, message='留言长度在5-500个字符长度', data='')
    user_name = get_user_username(db, user.username)
    rev_user = get_user(db, messageconent.id)
    if not rev_user:
        return reponse(code=100503, message='留言用户不存在', data='')
    if rev_user.id == user_name.id:
        return reponse(code=100501, message='自己不能给自己留言', data='')
    times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    message = Message(senduser=user_name.id,
                      acceptusers=rev_user.id,
                      context=messageconent.connect,
                      sendtime=times,addtime=times,read=False)
    db.add(message)
    db.commit()
    db.refresh(message)
    return reponse(code=200, message="成功", data='')


@usersRouter.get(path="/viewmessage")
async def viewmessage(id: int,
                      user: UsernameRole = Depends(get_cure_user_by_token),
                      db: Session = Depends(get_db)):
    useris=get_user_username(db,user.username)
    message = get_message(db, id)
    if not message:
        return reponse(code=100601, message='留言不存在', data='')
    if message.acceptusers != useris.id and message.senduser != useris.id:
        return reponse(code=100602, message='权限不足', data='')
    message.read = True
    db.commit()
    db.refresh(message)
    all_pid = get_pid_message(db, message.id)
    messageone = MessageOne(id=message.id,
                            senduser=get_user(db,message.senduser).username,
                            acceptusers=get_user(db, message.acceptusers).username,
                            read=message.read,
                            sendtime=message.sendtime,
                            addtime=str(message.addtime),
                            context=message.context)
    if len(all_pid) > 0:
        allpidlist = []
        for item in all_pid:
            message = MessagePid(id=message.id,
                                 senduser=get_user(db,item.senduser).username,
                                 acceptusers=get_user(db,item.acceptusers).username,
                                 read=item.read,
                                 sendtime=item.sendtime,
                                 addtime=str(item.addtime),
                                 context=item.context, pid=item.pid)
            allpidlist.append(message)
        messageone.pid = allpidlist
    return reponse(code=200, message='成功', data=jsonable_encoder(messageone))


@usersRouter.get(path="/messagelist")
async def messagelist(user: UsernameRole = Depends(get_cure_user_by_token),
                      db: Session = Depends(get_db)):
    users = get_user_username(db, user.username)
    messagelist = get_message_list(db=db, userid=users.id)
    message_list = []
    mainmessage = []
    if len(messagelist) > 0:
        for item in messagelist:
            if item.pid == "":
                messageone = MessageOne(id=item.id,
                                        senduser=get_user(db,item.senduser).username,
                                        acceptusers=get_user(db,item.acceptusers).username,
                                        read=item.read,
                                        sendtime=item.sendtime,
                                        addtime=str(item.addtime),
                                        context=item.context)
                mainmessage.append(messageone.id)
                all_pid = get_pid_message(db, item.id)
                if len(all_pid) > 0:
                    allpidlist = []
                    for items in all_pid:
                        message = MessagePid(id=item.id,
                                             senduser=get_user(db,items.senduser).username,
                                             acceptusers=get_user(db,items.acceptusers).username,
                                             read=items.read,
                                             sendtime=items.sendtime,
                                             addtime=str(items.addtime),
                                             context=items.context,
                                             pid=items.pid)
                        allpidlist.append(message)
                    messageone.pid = allpidlist
                message_list.append(messageone)
            else:
                if item.pid not in mainmessage:
                    message = get_message(db, item.pid)
                    if  message:
                        all_pid = get_pid_message(db, message.id)
                        messageone = MessageOne(id=message.id,
                                                senduser=get_user(db,message.senduser).username,
                                                acceptusers=get_user(db,message.acceptusers).username,
                                                read=message.read,
                                                sendtime=message.sendtime,
                                                addtime=str(message.addtime),
                                                context=message.context)
                        if len(all_pid) > 0:
                            allpidlist = []
                            for item in all_pid:
                                messagepid = MessagePid(id=message.id,
                                                        senduser=get_user(db,item.senduser).username,
                                                        acceptusers=get_user(db,item.acceptusers).username,
                                                        read=item.read,
                                                        sendtime=item.sendtime,
                                                        addtime=str(item.addtime),
                                                        context=item.context, pid=item.pid)
                                allpidlist.append(messagepid)
                            messageone.pid = allpidlist
                        message_list.append(messageone)
    return reponse(code=200, message='成功', data=jsonable_encoder(message_list))


@usersRouter.post(path='/rebackmessage')
async def rebackmessage(rebackmessage: RebackMessConnet, user: UsernameRole = Depends(get_cure_user_by_token),
                        db: Session = Depends(get_db)):
    if rebackmessage.connect == "":
        return reponse(code=100802, message='回复留言内容不能为空', data='回复留言内容不能为空')
    if len(rebackmessage.connect) > 500 or len(rebackmessage.connect) < 5:
        return reponse(code=100803, message='回复内容应该在5-500字', data='回复内容应该在5-500字')
    users = get_user_username(db, user.username)
    message = get_message(db, rebackmessage.rebackid)
    if not message:
        return reponse(code=100804, message='回复留言id不存在', data='回复留言id不存在')
    db_creat_rebackmessage(db, rebackmessage, users.id)
    return reponse(code=200, message='成功', data='成功')


@usersRouter.get(path='/deletemessage')
async def deletemessage(id: int, db: Session = Depends(get_db),
                        user: UsernameRole = Depends(get_cure_user_by_token)):
    messagse = get_message(db, id)
    useris=get_user_username(db,user.username)
    if not messagse:
        return reponse(code=100901, message='删除留言不存在', data='')
    if useris.id != messagse.acceptusers and useris.id != messagse.senduser:
        return reponse(code=100902, message='权限不足', data='')
    messagse.status = 1
    db.commit()
    db.refresh(messagse)
    return reponse(code=200, message='成功', data='成功')