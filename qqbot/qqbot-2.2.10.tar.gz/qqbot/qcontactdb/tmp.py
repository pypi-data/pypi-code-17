# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 21:38:47 2017

@author: hcj
"""

    '''
    def tname(self, tinfo):
        if tinfo in ('buddy', 'group', 'discuss'):
            return tinfo, CHSTYPE[tinfo]+'列表'
        else:
            return tinfo.ctype+'_member_'+tinfo.qq, str(tinfo)+'的成员列表'
    '''
    
    

    def _table(self, tinfo):
        ctype, owner = GetCTypeAndOwner(tinfo)
        if ctype in ('buddy', 'group', 'discuss'):
            return self.ctables[ctype]
        else:
            return self.ctables[ctype].get(owner.uin, NullTable)
    
    def table(self, tinfo):
        tb = self._table(tinfo)
        if tb.IsNull():
            tb = self.session.FetchTable(tinfo)
            tb and self.setTable(tinfo, tb)
        return tb
    
    def Update(self, tinfo, bot):
        tb = self.session.FetchTable(tinfo)
        
        if tb:
            self.updateTable(tinfo, tb, bot)
            status = '成功'
        else:
            status = '失败'
        
        ctype, owner = GetCTypeAndOwner(tinfo)
        if ctype in ('buddy', 'group', 'discuss'):
            action = '更新 %s 列表' % CTYPES[ctype]
        else:
            action = '更新 %s 的成员列表' % owner
        
        return action + status
    
    def List(self, tinfo, cinfo=None):
        table = self.table(tinfo)
        if table:
            return table.List(cinfo)
        else:
            return None

    def Find(self, tinfo, uin):
        cl = self.List(tinfo, 'uin='+uin)
        if cl is None:
            return None
        elif not cl:
            ctype, owner = GetCTypeAndOwner(tinfo)
            if ctype != 'group-member':
                return None
            qq = self.session.fetchBuddyQQ(uin)
            table = self._table(owner)
            cll = table.List('qq='+qq)
            if not cll:
                return None
            else:
                table.SetUin(cll[0], uin)
                return cll[0]
        else:
            return cl[0]
    
    def setTable(self, tinfo, table):
        ctype, owner = GetCTypeAndOwner(tinfo)
        if ctype in ('buddy', 'group', 'discuss'):
            self.ctables[ctype] = table
            # if ctype in ('group', 'discuss'):
            #     for c in table.List():
            #         self.ctables[ctype+'-member'][c.uin] = NullTable
            DEBUG('已更新 %s 列表', CTYPES[ctype])
        else:
            self.ctables[ctype][owner.uin] = table
            DEBUG('已更新 %s 的成员列表', owner)
    
    def updateTable(self, tinfo, table, bot):
        oldTable = self._table(tinfo)
        
        if oldTable.lastUpdateTime >= table.lastUpdateTime:
            return

        if table.lastUpdateTime - oldTable.lastUpdateTime > 3600:
            self.setTable(tinfo, table)
            return

        ctype, owner = GetCTypeAndOwner(tinfo)
        
        for c in table:
            if c not in oldTable:
                INFO('新增联系人： %s(owner=%s)', c, owner)
                Put(bot.onNewContact, c, owner)
                # if c.ctype in ('group', 'discuss'):
                #     self.ctables[c.ctype+'-member'][c.uin] = NullTable
        
        for c in oldTable:
            if c not in table:
                INFO('丢失联系人： %s(owner=%s)', c, owner)
                Put(bot.onLostContact, c, owner)
                if ctype in ('group', 'discuss'):
                    self.ctables[ctype+'-member'].pop(c.uin, None)
        
        self.setTable(tinfo, table)
    
    def UpdateForever(self, bot):
        tinfoQueue = collections.deque(['buddy','group','discuss','member'])
        self.autoUpdate(tinfoQueue, bot)
        
    # dancing with `fetchUpdate`, in main thread
    def autoUpdate(self, tinfoQueue, bot):
        tinfo = tinfoQueue.popleft()

        if tinfo == 'member':
            tinfoQueue.extend(self.ctables['group'].clist)
            tinfoQueue.extend(self.ctables['discuss'].clist)
            tinfoQueue.extend(['end', 'buddy','group','discuss','member'])
            needFetch = False
        elif tinfo == 'end':
            self.Dump()
            bot.onFetchComplete()
            needFetch = False
        else:
            needFetch = not self._table(tinfo).IsFresh()
            
        PutTo('auto-fetch', self.fetchUpdate,tinfo,needFetch,tinfoQueue,bot)
    
    # dancing with `autoUpdate`, in child thread 'auto-fetch'
    def fetchUpdate(self, tinfo, needFetch, tinfoQueue, bot):
        if needFetch:
            table = self.autoSession.FetchTable(tinfo)
            table and Put(self.updateTable, tinfo, table, bot)

        if tinfo == 'end':
            if bot.conf.fetchInterval < 0:
                INFO('已获取所有联系人资料，不再对联系人列表和资料进行刷新')
                sys.exit(0)
            else:
                time.sleep(bot.conf.fetchInterval)
        else:
            time.sleep(15)

        Put(self.autoUpdate, tinfoQueue, bot)
    
    # dancing with 'monitorFetch', in mainThread
    def MonitorForever(self, bot):
        if bot.conf.monitorTables:
            session = self.session.Copy()
            monitorTables = bot.conf.monitorTables[:]
            PutTo('monitor-fetch', lambda : (
                INFO('特别监视将在 30 秒后启动'),
                time.sleep(30),
                INFO('特别监视已启动'),
                Put(self.monitor, monitorTables, session, bot)
            ))
    
    # dancing with `monitor-fetch`, in main thread
    def monitor(self, monitorTables, session, bot):
        self.table('buddy')
        self.table('group')
        self.table('discuss')

        for tname in monitorTables[:]:
            if tname in ('buddy', 'group', 'discuss'):
                tl = [tname]
            elif tname.startswith('group-member-'):
                tl = self._table('group').List(tname[13:])
            elif tname.startswith('discuss-member-'):
                tl = self._table('discuss').List(tname[15:])
            else:
                tl = []

            if not tl:
                WARN(('特别监视列表中的 "%s" 不存在，'
                      '因此将其从特别监视列表中删除'), tname)
                monitorTables.remove(tname)
            else:
                PutTo('monitor-fetch', self.monitorFetch, session, tl, bot)
        
        if monitorTables:
            PutTo('monior-fetch',
                  Put, self.monitor, monitorTables, session, bot)
    
    # dancing with `monitor`, in child thread 'monitor-fetch'
    def monitorFetch(self, session, tl, bot):
        for tinfo in tl:
            table = session.FetchTable(tinfo)
            table and Put(self.updateTable, tinfo, table, bot)
            time.sleep(15)

    def StrOfList(self, ctype, info1=None, info2=None):
        if ctype in ('buddy', 'group', 'discuss'):
            return self.strOfList(ctype, cinfo=info1)
        elif ctype in ('group-member', 'discuss-member'):
            assert info1
            oinfo, cinfo = info1, info2            
            cl = self.List(ctype[:-7], oinfo)            
            if cl is None:
                return '错误：无法向 QQ 服务器获取联系人资料'
            elif not cl:
                return '错误：%s（%s）不存在' % (CTYPES[ctype[:-7]], oinfo)
            else:
                return '\n\n'.join(self.strOfList(owner,cinfo) for owner in cl)
        else:
            DEBUG(ctype)
            assert False
    
    def strOfList(self, tinfo, cinfo=None):
        ctype, owner = GetCTypeAndOwner(tinfo)
        cl = self.List(tinfo, cinfo)
        
        if cl is None:
            return ('错误：无法向 QQ 服务器获取联系人资料')
        
        if cinfo is None:
            cinfoStr = ''
        else:
            cinfoStr = '（"%s"）' % cinfo

        if ctype in ('buddy', 'group', 'discuss'):
            head = '%s列表%s：' % (CTYPES[ctype], cinfoStr)
        else:
            head = '%s 的成员列表%s：' % (owner, cinfoStr)
        
        if not cl:
            return head + '空'
        
        result = [head]
        result.append('=' * 100)
        result.append('\t'.join(('类型',) + CHSTAGS + EXCHSTAGS))
        result.append('=' * 100)
        
        for c in cl:
            l = [CTYPES[c.ctype]] + \
                [(getattr(c, tag[:-1], '') or '#') for tag in (TAGS+EXTAGS)]
            result.append('\t'.join(l))

        result.append('=' * 100)

        return '\n'.join(result)
    
    def ObjOfList(self, ctype, info1=None, info2=None):
        if ctype in ('buddy', 'group', 'discuss'):
            return self.objOfList(ctype, cinfo=info1)
        elif ctype in ('group-member', 'discuss-member'):
            assert info1
            oinfo, cinfo = info1, info2            
            cl = self.List(ctype[:-7], oinfo)
            if cl is None:
                return None, '错误：无法向 QQ 服务器获取联系人资料'
            elif not cl:
                return None, '错误：%s（%s）不存在' % (CTYPES[ctype[:-7]], oinfo)
            else:
                result = []
                for owner in cl:
                    r = self.objOfList(owner, cinfo)
                    result.append({
                        'owner': owner.__dict__,
                        'membs': {'r':r[0], 'e':r[1]}
                    })
                return result, None
        else:
            DEBUG(ctype)
            assert False
    
    def objOfList(self, tinfo, cinfo=None):
        ctype, owner = GetCTypeAndOwner(tinfo)
        cl = self.List(tinfo, cinfo)        
        if cl is None:
            return None, '错误：无法向 QQ 服务器获取联系人资料'
        else:
            return [c.__dict__ for c in cl], None

    def DeleteMember(self, group, memb, bot):
        if self._table(group).Remove(memb):
            INFO('丢失联系人： %s(owner=%s)', memb, group)
            Put(bot.onLostContact, memb, group)

    def SetMemberCard(self, group, memb, card):
        self._table(group).SetCard(memb, card)
    
    def FirstFetch(self):
        self.List('buddy')
        gl = self.List('group')
        dl = self.List('discuss')
        [self.List(g) for g in gl]
        [self.List(d) for d in dl]
        self.Dump()
