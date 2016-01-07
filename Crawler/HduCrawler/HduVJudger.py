import requests


class HduVJudger:

    login_url = 'http://acm.hdu.edu.cn/userloginex.php?action=login'
    submit_url = 'http://acm.hdu.edu.cn/submit.php?action=submit'
    s = None
    snt = 0

    userinfo = dict(
        username = 'xxx111',
        userpass = 'heihei',
        login = 'Sign in',
    )

    submit_data = dict(
        check=0,
        problemid=1000,
        language=0,
        usercode='',
    )

    def getlange(self,lang):
        if lang == 'G++':
            return 0

    def login(self):
        snt = 30
        self.s = requests.session()
        self.s.post(url=self.login_url,data=self.userinfo)

    def submit(self,pid,lang,code):

        self.submit_data['problemid']=pid
        self.submit_data['language']=self.getlange(lang)
        self.submit_data['usercode']=code

        if self.s==None or self.snt <= 0 :
            self.login()
        else:
            self.snt = self.snt -1

        r = self.s.post(url=self.submit_url,data=self.submit_data)



if __name__=='__main__':

    code = '''
    #include <iostream>

    using namespace std;

    int main()
    {
    int a,b;
    while(cin>>a>>b)
    {
    cout<<a+b<<endl;
    }
    return 0;
    }
    '''

    HV = HduVJudger()
    HV.submit(1000,'G++',code)
    HV.submit(1000,'G++',code)