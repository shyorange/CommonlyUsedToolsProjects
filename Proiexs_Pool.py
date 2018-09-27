#coding=gbk
#__author__ : "shyorange"
#__date__ :  2018/8/22
import time;
import random;
import sqlite3;
import requests;
from lxml import etree;
"""��ȡ��Ѵ���ip�Ĺ���"""
class  ProiexsPool:
    @staticmethod
    def _get_proiexs():
        # �������ip���б�
        ips = [];
        # ������ȡ����ip����վ��ֻ��ȡǰ��ҳ��
        for i in range(1,3):
            html = requests.get("https://www.kuaidaili.com/free/inha/"+str(i)+"/",headers={
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0"
            }).text;
            # ȡ��ip��Э������
            html_tree = etree.HTML(html);
            tr_ips = html_tree.xpath("//tbody/tr");
            # print(tr_ips);
            for index,tr in enumerate(tr_ips):
                xieyi = tr.xpath("//td[4]/text()")[index];
                ip = tr.xpath("//td[1]/text()")[index]+":"+tr.xpath("//td[2]/text()")[index];
                # print(type(ip));
                # port = ;
                full_ip = {xieyi : ip};
                # ����ip�Ƿ����
                if ProiexsPool._check_ip(full_ip):
                    # �鿴���ݿ����Ƿ���ڸ���ip
                    if ProiexsPool._select_ip_from_database(ip):
                        # �����п��õ�ip�������ݿ�
                        ProiexsPool._save_ip_to_database(xieyi,ip);
            if i == 2:
                break;
            else:
                time.sleep(5);

    @staticmethod
    def _check_ip(ip):
        """
        ���ip�Ƿ���õķ���
        :param ip:Ҫ����ip
        :return: True����False
        """
        try:
            # print("���ڼ��ip��{}".format(ip));
            html = requests.get("http://bj.58.com/chuzu/?PGTID=0d100000-0000-15df-5f6f-34fb3bfd7994&ClickID=3",headers={
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0"
            },proxies=ip,timeout = 3);
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
        ��ip�������ݿ�
        :param xieyi: ����ip��Э�飨https��http��socket�ȣ�
        :param ip: һ��ip�����ֵ����ͣ�
        :return: None
        """
        conn = sqlite3.connect("ProxiesPool.db");
        cursor = conn.cursor();
        cursor.execute("create table if not exists proxies(xieyi varchar,ip varchar)");
        cursor.execute("insert into proxies(xieyi ,ip) values ('{}','{}')".format(xieyi,ip));
        conn.commit();
        cursor.close();
        conn.close();

    @staticmethod
    def _select_ip_from_database(ip):
        """
        ���ݴ����ip��ѯ�������ݿ����Ƿ��и�ip�������Ƿ񱣴��ip
        :param ip: Ҫ��ѯ��ip
        :return: True��False
        """
        try:
            conn = sqlite3.connect("ProxiesPool.db");
            cursor = conn.cursor();
            cursor.execute("create table if not exists proxies(xieyi varchar,ip varchar)");
            count = cursor.execute("select count(ip) from proxies where ip = '{}'".format(ip));
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
        ���ݴ����ipɾ��ʧЧ��ip����
        :param ip: Ҫɾ����ip
        :return: None
        """
        conn = sqlite3.connect("ProxiesPool.db");
        cursor = conn.cursor();
        cursor.execute("create table if not exists proxies(xieyi varchar,ip varchar)");
        cursor.execute("delete from proxies where ip = '{}'".format(ip));
        conn.commit();
        cursor.close();
        conn.close();
        print("�ɹ�ɾ��ʧЧ����ip��{}.....".format(ip));

    @staticmethod
    def _get_random_ip():
        """
        ������һ��ip����������ݿ��ip����
        :return: None
        """
        conn = sqlite3.connect("ProxiesPool.db");
        cursor = conn.cursor();
        cursor.execute("create table if not exists proxies(xieyi varchar,ip varchar)");
        counts = cursor.execute("select count(*) from proxies")
        if counts.__next__()[0] < 5:
            # ������ݿ����ip����С��5�����������ݿ���������������
            ProiexsPool._get_proiexs();
        # ������ݿ�������Ip
        proxies = cursor.execute("select * from proxies");
        ips = [];
        for xieyi,ip in proxies:
            ips.append({xieyi : xieyi.lower()+"://"+ip});
        conn.commit();
        cursor.close();
        conn.close();
        return random.choice(ips);

if __name__ == '__main__':
    ProiexsPool._get_proiexs();