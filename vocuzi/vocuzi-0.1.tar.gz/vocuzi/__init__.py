from selenium import webdriver
def help():
    print "-------------------------------------------------------"
    print "File :       vocuzi.py"
    print "Author :     Vipin Joshi (@vocuzi)"
    print "Date :       Created : April 24, 2017"
    print "Download :   http://vocuzi.in/dev/ , https://github.com/vocuzi/vocuzi"
    print "Brief :      Helping psinous with simple operations."
    print "Notes :      In memory of peace and happiness. #oso7d"
    print "Classes :"
    print """         psource : returns page source through various modes.
            Usage - psource.func(url,mode)
            Modes - 
                selenium = uses selenium to get the page source.
                proxy = uses requests with webproxy hosted on google cloud platform to get the page source. 
                urllib2-proxy = uses urllib2 with webproxy hosted on google cloud platform to get the page source.
                urllib2 =  uses urllib2 to get the page source.
                foobar = uses requests to get the page source.\n"""    
    print """         ldork : returns either a list of dorks for today or 0 for no dorks.
            Usage - ldork.func(src,date)
            Description - 
                src = Page source of the dork source page. I use google-hacking-database as the dork source.
                date = Present date in format yyyy-mm-dd."""
    print """         date : returns date according to specified choice.
            Usage - date.func(format)
            Formats - 
                dd-mm-yy
                dd-mmm-yyyy
                dd-mm-yyyy
                yyyy-mm-dd"""
    print "-------------------------------------------------------\n"
class psource:
    #psource - Page Source
    #Usage - 
    #   s = psource()
    #   s.func(url,mode) <- returns the page source
    requests = __import__('requests')
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
    def func(self,url,mode):
        if mode == "selenium":
            d = webdriver.PhantomJS()
            d.get(url)
            return d.page_source
        elif mode=="proxy":
            r = "http://test1231123456489.appspot.com/"+url.split("//")[1]
            r = self.requests.get(r, headers=self.header).text
            return r
        elif mode=="urllib2-proxy":
            r = "http://test1231123456489.appspot.com/"+url.split("//")[1]
            r = self.urllib2.Request(r, headers=self.header)
            r = self.urllib2.urlopen(r).read()
            return r
        elif mode=="urllib2":
            r = self.urllib2.Request(url, headers=self.header)
            r = self.urllib2.urlopen(r).read()
            return r
        else:
            r = self.requests.get(url, headers=self.header).text
            return r


class ldork:
    #ldork - latest dorks
    #Usage - 
    #    l = ldork()
    #    l.func(src,date) <- returns the latest dorks list
    bs4 = __import__('bs4')
    def func(self,src,date):
        src = self.bs4.BeautifulSoup(src,'html.parser')
        src = src.findAll("table", { "class" : "category-list" })
        src  = str(src)
        if src.find(date) > -1:
            src = self.bs4.BeautifulSoup(src,'html.parser')
            src = str(src.findAll('tbody'))
            src = self.bs4.BeautifulSoup(src,'html.parser')
            src = src.findAll('tr')
            rdork = []
            for dork in src:
                dork = dork.findAll('td')
                if dork[0].text == date:
                    #dork date, dork, dork category
                    drkdata = [dork[1].text,dork[2].text]
                    rdork.append(drkdata)
                else:
                    continue
            return rdork
        else:
            return 0

        

class date:
    #date - custom date formats
    #Usage - 
    #    d = date()
    #    d.func(format) <- returns the specified format date
    #    dd-mm-yy - 21-08-14
    #    dd-mmm-yyyy - 21-aug-2014
    #    dd-mm-yyyy - 21-08-2014
    #    yyyy-mm-dd - 2014-08-21
    subprocess = __import__("subprocess")
    def func(self,format):
        hour = self.subprocess.check_output("date")[:-1].split(" ")
        date = hour[2]
        if len(date) == 1:
            date = "0"+date
        months = ['jan','feb','mar','apr','may','june','july','aug','sept','oct','nov','dec']
        al_month = hour[1].lower()
        num_month = str(int(months.index(al_month))+1)
        if len(num_month) == 1:
            num_month = "0"+num_month
        year = hour[5]
        day = hour[0]
        if format=="dd-mm-yy":
            return date+"-"+num_month+"-"+year[2:]
        elif format=="dd-mmm-yyyy":
            return date+"-"+al_month+"-"+year
        elif format=="dd-mm-yyyy":
            return date+"-"+num_month+"-"+year
        elif format=="yyyy-mm-dd":
            return year+"-"+num_month+"-"+date
        else:
            return date+"-"+num_month+"-"+year[2:]