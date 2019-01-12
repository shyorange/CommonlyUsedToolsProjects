#coding=gbk
#__author__ : "shyorange"
#__date__ :  2018/8/22
import random;
import sqlite3;
import threading;
import requests;
from lxml import etree;
"""获取免费代理ip的工具（爬取快代理和西刺代理，以天猫网址作为检测代理ip是否可用的网站）"""
class  ProiexsPool:

    @staticmethod
    def get_html(url):
        html = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0"
        }).text
        return html

    # 爬取快代理
    @staticmethod
    def _get_proiexs_from_kuai(page=10):
        print("开始爬取快代理")
        # 首先爬取代理ip的网站（只爬取前10页）
        for i in range(1,page+1):
            url = "https://www.kuaidaili.com/free/inha/"+str(i)+"/"
            html = ProiexsPool.get_html(url)
            # 取出ip和协议类型
            html_tree = etree.HTML(html);
            tr_ips = html_tree.xpath("//tbody/tr");
            # print(tr_ips);
            for index,tr in enumerate(tr_ips):
                xieyi = tr.xpath("//td[4]/text()")[index];
                ip = tr.xpath("//td[1]/text()")[index]+":"+tr.xpath("//td[2]/text()")[index];
                # print(type(ip));
                # port = ;
                ProiexsPool.test_real_ip(xieyi,ip)

    # 爬取西刺代理
    @staticmethod
    def _get_proiexs_from_xici(page=10):
        print("开始爬取西刺代理")
        for i in range(1,page+1):
            url = f"https://www.xicidaili.com/nn/{i}"
            html = ProiexsPool.get_html(url)
            if html:
                tre = etree.HTML(html)
                trs=tre.xpath('//table[@id="ip_list"]//tr')[1:]
                for tr in trs:
                    td_ip = tr.xpath('./td[2]/text()')
                    td_port = tr.xpath('./td[3]/text()')
                    ip = td_ip + ":" + td_port
                    xieyi = tr.xpath('./td[6]/text()').lower()

                    # 检测ip是否可用
                    ProiexsPool.test_real_ip(xieyi,ip)



    # 使用多线程，进行爬取两个网站的ip
    @staticmethod
    def _get_proiexs():
        t_kuai = threading.Thread(target=ProiexsPool._get_proiexs_from_kuai)
        t_xici = threading.Thread(target=ProiexsPool._get_proiexs_from_xici)
        t_kuai.start()
        t_xici.start()
        t_kuai.join()
        t_xici.join()


    # 对爬取到的ip进行测试
    @staticmethod
    def test_real_ip(xieyi,ip):
        full_ip = {"http": xieyi.lower() + "://" + ip, "https": xieyi.lower() + "://" + ip};
        print(f"正在检测：{full_ip}")
        # 测试ip是否可用
        if ProiexsPool._check_ip(full_ip):
            # 查看数据库中是否存在该组ip
            if ProiexsPool._select_ip_from_database(ip):
                # 将所有可用的ip存入数据库
                ProiexsPool._save_ip_to_database(xieyi, ip);

    @staticmethod
    def _check_ip(ip):
        """
        检查ip是否可用的方法
        :param ip:要检查的ip
        :return: True或者False
        """
        try:
            print("正在检查ip：{}".format(ip));
            html = requests.get("https://www.tmall.com/",headers={
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0"
            },proxies=ip,timeout = 6);
        except Exception as e:
            print(e);
            return False;
        else:
            if html.status_code == 200:
                return True;
            else:
                return False;

    @staticmethod
    def _save_ip_to_database(xieyi,ip):
        """
        将ip存入数据库
        :param xieyi: 代理ip的协议（https，http，socket等）
        :param ip: 一个ip代理（字典类型）
        :return: None
        """
        lock = threading.Lock()
        lock.acquire()  # 加锁
        conn = sqlite3.connect("ProxiesPool.db");
        cursor = conn.cursor();
        cursor.execute("create table if not exists proxies(xieyi varchar,ip varchar)");
        cursor.execute("insert into proxies(xieyi ,ip) values ('{}','{}')".format(xieyi,ip));
        conn.commit();
        cursor.close();
        conn.close();
        lock.release()  #  释放锁

    @staticmethod
    def _select_ip_from_database(ip):
        """
        根据传入的ip查询，看数据库中是否有该ip，决定是否保存该ip
        :param ip: 要查询的ip
        :return: True或False
        """
        try:
            lock = threading.Lock()
            lock.acquire()  # 加锁
            conn = sqlite3.connect("ProxiesPool.db");
            cursor = conn.cursor();
            cursor.execute("create table if not exists proxies(xieyi varchar,ip varchar)");
            count = cursor.execute("select count(ip) from proxies where ip = '{}'".format(ip));
            lock.release()   # 释放锁
            # print(count);
            if not count.__next__()[0]:
                return True;
            else:
                return False;
        except Exception as e:
            print(e);
        finally:
            conn.commit();
            cursor.close();
            conn.close();

    @staticmethod
    def _delete_ip_from_db(ip):
        """
        根据传入的ip删除失效的ip数据
        :param ip: 要删除的ip
        :return: None
        """
        conn = sqlite3.connect("ProxiesPool.db");
        cursor = conn.cursor();
        cursor.execute("create table if not exists proxies(xieyi varchar,ip varchar)");
        cursor.execute("delete from proxies where ip = '{}'".format(ip));
        conn.commit();
        cursor.close();
        conn.close();
        print("成功删除失效代理ip：{}.....".format(ip));

    @staticmethod
    def _get_random_ip():
        """
        随机获得一个ip，并检测数据库的ip数量
        :return: None
        """
        conn = sqlite3.connect("ProxiesPool.db");
        cursor = conn.cursor();
        cursor.execute("create table if not exists proxies(xieyi varchar,ip varchar)");
        counts = cursor.execute("select count(*) from proxies")

        if counts.__next__()[0] < 5:
            # 如果数据库里的ip数量小于5个，则往数据库中重新填入数据
            ProiexsPool._get_proiexs();
        # 获得数据库中所有Ip
        proxies = cursor.execute("select * from proxies");
        ips = [];
        for xieyi,ip in proxies:
            ips.append({"http" : xieyi.lower()+"://"+ip,"https" : xieyi.lower()+"://"+ip});
        conn.commit();
        cursor.close();
        conn.close();
        return random.choice(ips);

if __name__ == '__main__':
    print(ProiexsPool._get_random_ip());
