#encoding: u8
from easyEmail import easyEmail


def sendtextmail(mail_host, mail_user, mail_pass, FromDesc, mailto_list):
    mail_title = "发送纯文件邮件,不支持内置图片"
    mobj = easyEmail(mail_host, mail_user, mail_pass)
    res = mobj.sendTextmail(FromDesc,
                             mailto_list, 
                             mail_title,
                             ["hello\nhaha"], #文本
                             ["d:\\1.txt"] #附件
                             )

def sendhtmlmail(mail_host, mail_user, mail_pass, FromDesc, mailto_list):
    mail_title = "发送html邮件,支持内置图片"
    mobj = easyEmail(mail_host, mail_user, mail_pass)
    res = mobj.sendHtmlmail(FromDesc,
                             mailto_list, 
                             mail_title, 
                             ["<b>详见下图:</b>","d:\\1.jpg", "d:\\2.jpg"], #html+内置图片
                             ["d:\\1.txt","d:\\2.txt"] #附件
                             )  

def main():
    mail_host = "smtp.exmail.qq.com"
    mail_user = "xxx@xxx.xxx"
    mail_pass = "xxx"
    mailto_list=["xxx@xxx.xxx"]
    FromDesc = "一个测试平台"
    # sendtextmail(mail_host, mail_user, mail_pass, FromDesc, mailto_list)
    sendhtmlmail(mail_host, mail_user, mail_pass, FromDesc, mailto_list)



if __name__ == '__main__':
    main()

