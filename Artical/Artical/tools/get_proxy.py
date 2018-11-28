import requests
from lxml import etree
import MySQLdb
import time

conn = MySQLdb.connect(host='127.0.0.1',user='root', passwd="0", db="artical_spider", charset="utf8")
cur = conn.cursor()


def get_pro():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
    }

    # proxy = {
    #     'http':'180.183.8.223:8080'
    # }

    for i in range(100):
        time.sleep(0.5)
        response = requests.get('http://www.xicidaili.com/nn/{0}'.format(i),headers=headers)

        content = etree.HTML(response.text)

        #国内高匿
        tr_list = content.xpath('//table[@id="ip_list"]//tr[position()>=2]')

        proxy_list = []
        for tr in tr_list:
            ip = tr.xpath('./td[2]/text()')[0]
            port = tr.xpath('./td[3]/text()')[0]
            type = tr.xpath('./td[6]/text()')[0]
            speed_str = tr.xpath('./td[7]/div/@title')
            if speed_str:
                speed = float(speed_str[0].split('秒')[0])

            print(ip,port,type,speed)
            if port == '80' and type == 'HTTP':
                proxy_list.append((ip,port,type,speed))

        for p in proxy_list:
            try:
                cur.execute(
                    "insert proxy(ip,port,type,speed) VALUES('{0}','{1}','{2}',{3})"
                    .format(p[0],p[1],p[2],p[3])
                )
            except:
                pass
        conn.commit()


class Get_Random_Ip():
    def del_ip(self,ip):
        del_sql = """
            delete from proxy where ip='{0}'
        """.format(ip)
        cur.execute(del_sql)
        conn.commit()
        return True

    def judge_ip(self,ip,port,type):
        pro = {
            type : ip + ':' + port
        }
        try:
            response = requests.get('https://www.baidu.com/',proxies=pro)
        except Exception as e:
            print("invalid ip and port")
            self.del_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print('effective ip')
                return True
            else:
                self.del_ip(ip)
                print("invalid ip and port")
                return False


    def get_ip(self):
        random_sql = """
            SELECT ip, port, `type` FROM proxy ORDER BY RAND() LIMIT 1
        """

        result = cur.execute(random_sql)

        for i in cur.fetchall():
            ip = i[0]
            port = i[1]
            type = i[2]

            judge_re = self.judge_ip(ip,port,type)
            if judge_re:
                return '{0}://{1}:{2}'.format(type,ip,port)
            else:
                return self.get_ip()



if __name__ == '__main__':
    # count_sql = """
    #     select count(*) from proxy group by ip
    # """
    # count = cur.execute(count_sql)
    # if count < 100:
    #     proxy_spider()


    gp = Get_Random_Ip()
    gp.get_ip()































