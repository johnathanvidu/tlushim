import re
import requests
import exceptions

from bs4 import BeautifulSoup

TEKEN = 9.25

class entry():
    def __init__(self, date, starttime='', endtime='', tottime='', usdata=[]):
        self.date = date
        self.usdata = usdata
        self.tottime = ''

    def calc_days(self):
        if float(self.usdata[-1]) == -9.25:
            self.usdata = self.usdata[:-1]
        if len(self.usdata) > 2:
            self.tottime = self.usdata[-1] if float(self.usdata[-1]) > 0 else self.usdata[-2]


class Tlushim(object):
    headers = {
        'Origin': 'https://www.tlushim.co.il',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8,he;q=0.6',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.0.10802 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Referer': 'https://www.tlushim.co.il/',
        'Connection': 'keep-alive',
        }

    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password

    def calculate(self, requested_month):
        """
        requested_month: should be in tlushim format - yyyy_mm
        """
        req_session = requests.Session()
        data = 'id_num={0}&password={1}&connect='.format(self.user_id, self.password)
        url = 'https://www.tlushim.co.il/login.php'
        urlt = 'https://www.tlushim.co.il/main.php?op=atnd&month={0}'.format(requested_month)
        rf = req_session.post(url, headers=self.headers, data=data)
        if rf.url in ['https://www.tlushim.co.il/index.php?error=2',
                      'https://www.tlushim.co.il/index.php?error=id_num']:
            raise exceptions.LoginAttemptFailed()
        r = req_session.get(urlt)
        sitedata = r.content
        soup = BeautifulSoup(sitedata, 'html.parser')
        agg = soup.findAll('td', attrs={'class': 'atnd'})
        nagg = []
        for ag in agg:
            if ag.text not in [' ', '']:
                nagg.append(ag.text)
        entry_data = []
        entries = []
        entry_date = ''
        for nag in nagg:
            if re.findall('\d{2}\/\d{2}\/\d{2}', nag):
                if entry_date and entry_data:
                    new_entry = entry(entry_date, usdata=entry_data)
                    entries.append(new_entry)
                    entry_date = ''
                    entry_data = []
                entry_date = nag
            else:
                entry_data.append(nag)
        tot_done = float()
        tot_need = float()
        for entri in entries:
            entri.calc_days()
            if entri.tottime:
                tot_done += float(entri.tottime)
                tot_need += TEKEN
        days = int(tot_need/TEKEN)
        differe = tot_done-tot_need
        ahead_or_behind = 'ahead'
        if differe < 0:
            ahead_or_behind = 'behind'
            differe = -differe
        return days, differe, ahead_or_behind
