import tornado.web
import tornado.gen

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from tools.dbcore import ConnPool
from tools.encode import UTF8StrToBase64Str, Base64StrToUTF8Str
from UIModule.MsgModule import renderMSG

from Crawler.BnuVJCrawler.BnuVJCrawler import BnuVJCrawler


class ProblemHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(10)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, oj=None, pid=None):

        cid = self.get_argument('cid', -1)

        print('oj: ' + oj + ' pid: ' + pid)
        D = yield self.getProblem(oj, pid)

        if D is None :
            yield self.CrawlerOnLine(oj,pid)
            D = yield self.getProblem(oj, pid)

        if D is None :
            self.write(renderMSG('Can\'t find this problem',waittime=1000000))
            self.finish()
            return

        clearkeys = list()
        for x in D.keys():
            lenth = len(str(D[x]))
            if lenth == 0 : clearkeys.append(x)

        for x in clearkeys :    del D[x]

        current_user = self.get_secure_cookie('username')
        self.render('problem.html', D=D, current_user=current_user, cid=cid)

    @run_on_executor
    def CrawlerOnLine(self,oj,pid):
        BVC = BnuVJCrawler()
        BVC.CrawlerProblem(oj,pid)

    @run_on_executor
    def getProblem(self, oj, problemid):

        # get pid
        conn = ConnPool.connect()
        cur = conn.cursor()

        sql = 'SELECT * FROM problem WHERE ( originOJ LIKE "{}" and originProb LIKE "{}" )'.format(oj, problemid)
        cur.execute(sql)
        rt = cur.fetchone()

        # error
        if rt is None:
            return None

        d = dict()

        d['originOJ'] = oj
        d['originProb'] = problemid

        if rt[0] is not None:
            d['pid'] = rt[0]
        if rt[1] is not None:
            d['title'] = rt[1]
        if rt[2] is not None:
            d['source'] = rt[2]
        if rt[3] is not None:
            d['url'] = rt[3]

        sql = 'SELECT * FROM problemdetail WHERE pid = {}'.format(d['pid'])
        cur.execute(sql)
        rt = cur.fetchone()

        print(sql)
        print(rt)

        if rt[2] is not None:
            d['description'] = Base64StrToUTF8Str(rt[2])
        if rt[3] is not None:
            d['input'] = Base64StrToUTF8Str(rt[3])
        if rt[4] is not None:
            d['output'] = Base64StrToUTF8Str(rt[4])
        if rt[5] is not None:
            d['sampleinput'] = Base64StrToUTF8Str(rt[5])
        if rt[6] is not None:
            d['sampleoutput'] = Base64StrToUTF8Str(rt[6])
        if rt[7] is not None:
            d['hint'] = Base64StrToUTF8Str(rt[7])
        if rt[8] is not None:
            d['author'] = Base64StrToUTF8Str(rt[8])
        if rt[10] is not None:
            d['updatetime'] = str(rt[10])
        if rt[11] is not None:
            d['memorylimit'] = rt[11]
        if rt[12] is not None:
            d['timelimit'] = rt[12]
        if rt[13] is not None:
            d['specialjudge'] = rt[13]

        cur.close()
        conn.close()
        return d


def main():
    oj = 'HDU'
    problemid = '1092'

    # get pid
    conn = ConnPool.connect()
    cur = conn.cursor()

    sql = 'SELECT * FROM problem WHERE ( originOJ LIKE "{}" and originProb LIKE "{}" )'.format(oj, problemid)
    cur.execute(sql)
    rt = cur.fetchone()

    # error
    if rt is None: pass

    d = dict()

    if rt[0] is not None:
        d['pid'] = rt[0]
    if rt[1] is not None:
        d['title'] = rt[1]
    if rt[2] is not None:
        d['source'] = rt[2]
    if rt[3] is not None:
        d['url'] = rt[3]

    sql = 'SELECT * FROM problemdetail WHERE pid = {}'.format(d['pid'])
    cur.execute(sql)
    rt = cur.fetchone()

    if rt[2] is not None:
        d['description'] = Base64StrToUTF8Str(rt[2])
    if rt[3] is not None:
        d['input'] = Base64StrToUTF8Str(rt[3])
    if rt[4] is not None:
        d['output'] = Base64StrToUTF8Str(rt[4])
    if rt[5] is not None:
        d['sampleinput'] = Base64StrToUTF8Str(rt[5])
    if rt[6] is not None:
        d['sampleoutput'] = Base64StrToUTF8Str(rt[6])
    if rt[7] is not None:
        d['hint'] = Base64StrToUTF8Str(rt[7])
    if rt[8] is not None:
        d['author'] = Base64StrToUTF8Str(rt[8])
    if rt[10] is not None:
        d['updatetime'] = str(rt[10])
    if rt[11] is not None:
        d['memorylimit'] = rt[11]
    if rt[12] is not None:
        d['timelimit'] = rt[12]
    if rt[13] is not None:
        d['specialjudge'] = rt[13]

    cur.close()

    for key in d:
        print(key + ' ---> ' + str(d[key]))


if __name__ == '__main__':
    main()
