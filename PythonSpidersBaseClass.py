#coding=gbk
# __author__ : "shyorange"
# __date__ :  2018/8/07
import urllib.request
import re;
import sqlite3;
import xlwt;
import requests;
from lxml import etree;
from bs4 import BeautifulSoup as bSoup;
from Proiexs_Pool import ProiexsPool;
"""���м�����Ļ��࣬��������ֻ��̳и��༴��"""
class Catch:
    def __init__(self, url):
        self._url = url ;
        # ʹ�����ַ�ʽ��ȡ��ҳԴ���루Ĭ��ʹ��requests��ֵΪ��1 ʱʹ��urllib��
        self._get_html_type = None;
        # ʹ�����ַ�ʽ����ƥ����������ݣ�Ĭ��ʹ��regular�� ֵΪ��1 ʱʹ��BeautifulSoup4��ֵΪ��2ʱʹ��XPath��
        self._match_type = None;
        # ��ʹ��BeautifulSoupƥ��ʱ�����Բ����ã���һ���б�
        self._bs_parse_result = None;
        # bSoup��ƥ�����Ĭ��ƥ�������ĵ���
        self._bs_match_str = "html"
        # ʹ��XPathƥ��ʱ���������Ը�ֵ��ֵΪһ��XPath�ĵ���
        self._html_tree_xpath = None;
        # ���ڼ�¼�кŵı�־
        self._count_row = 1;
        self._html_content = ""; # ��ҳԴ����
        self._regular_all_need = ""; # ƥ��������Դ������ʽ
        self._regular_next_page = ""; # ƥ����һҳurl���ӵ�����ʽ
        self._web_page_encode = "utf-8";
        self._headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/56.0.2924.90 Safari/537.36 2345Explorer/9.3.2.17331"
        };
        # �Ƿ�ʹ�ô���ip (Ĭ��Ϊʹ��)
        self._is_useProxies = True;
        self._result_needs = [] #"��ȡ�Ľ������һ���б�";
        self._result_next_page = [] #"��ȡ������һҳ��url����(Ϊ�ձ�ʾ��ȡ����)";
        self._isHas_next_page = True; #�Ƿ�����һҳ
        self._reorganize_string = ""; #����Ҫ����urlʱ����������Ը�ֵ��
        #�������ݿ������
        self._is_save_data_to_db = False; # �Ƿ񱣴����ݣ�Ĭ�ϲ����棨���浽���ݿ⣩
        self._is_save_data_to_excel = False; # �Ƿ񱣴����ݣ�Ĭ�ϲ����棨���浽Excel���
        self._conn_db = None;
        self._cursor_db = None;
        self._table_name = ""; # ����
        self._create_table_tuple = (); # �������������ֶ�����(���������ֶε�Ԫ��)
        # self._insert_data_to_table_tuple = None; # �������������������� (һ�������������ݵ�Ԫ��)
        #����Excel������������
        self._work_book = None;
        self._sheet = None;
        self._excel_heads = None;
        self._excel_name = "";
        self._sheet_name = "";

    def _creat_excel_header(self,sheet_name, *args):
        """
        ΪExcel��񴴽���ͷ�ķ���
        :param sheet_name: Ҫ������ı���
        :param args: ���еı�ͷ��Ϣ
        :return: None
        *args��args������
                *argsֱ�Ӿ�����������
                 args��һ���������ݵ�Ԫ��
        """
        self._work_book = xlwt.Workbook(encoding="utf-8");
        self._sheet = self._work_book.add_sheet(sheet_name);
        # �˴�ֱ�ӱ���Ԫ��
        print(args[0]);
        for index,head in enumerate(args[0]):
            self._sheet.write(0,index,head);

    def _write_data_to_excel(self, *args):
        '''
        ������д��Excel�ļ�
        :param args: ���ݣ�Ԫ�飩
        :return: None
        '''
        print("���ڽ���{}������д����......".format(self._count_row));

        for idx, dat in enumerate(args[0]):
            self._sheet.write(self._count_row,idx,str(dat).strip());
        print("����д������ϡ�");
        # ��������
        self._work_book.save(self._excel_name);
        self._count_row += 1;

    #�������ݿ�ķ�����
    def _connect_databse(self):
        self._conn_db = sqlite3.connect("PythonSpiderData.db");
        self._cursor_db = self._conn_db;

    # �ر����ݿ�ķ���
    def _close_database(self):
        self._conn_db.commit();
        self._cursor_db.close();
        self._conn_db.close();

    def _create_table(self):
        """
        �������ݿ��е����ݱ�ķ���
        :return:
        """
        self._connect_databse();
        # �����ֶ��ֵ䣬ȡ���������Ϣ
        create_table_sql = "";
        for k in self._create_table_tuple:
            create_table_sql += ", "+k+" varchar";
        self._cursor_db.execute("create table if not exists "+self._table_name+"(id integer primary key"+create_table_sql+")");
        self._close_database();

    # �������ݵķ���(�����ݿ�)
    def _save_data_to_sqlite3(self,table_name,*args):
        self._connect_databse();
        # ��Ҫ��������ݽ�������
        ziduans = "";
        insert_sql = "";
        for index,key in enumerate(self._create_table_tuple):
            if index+1 == len(self._create_table_tuple):
                ziduans += key;
            else:
                ziduans += key+",";
        for index,i in enumerate(args[0]):
            if index+1 == len(args[0]):
                insert_sql += "'"+str(i).replace("'","��")+"'";
            else:
                insert_sql += "'"+str(i).replace("'","��")+"',";
        self._cursor_db.execute("""insert into {}({}) values({})""".format(table_name,ziduans,insert_sql));
        self._close_database();

    # �����ҳԴ���루ʹ��urllib��
    def _get_html_content_by_urllib(self):
        # count = 1;
        while True:
            try:
                # if count > 4:
                #     print("�������Ѿ������ĴΣ�����ʧЧ��:{}".format(self._url));
                #     break;
                re_request = urllib.request.Request(self._url,headers = self._headers);
                self._html_content = urllib.request.urlopen(re_request,timeout=2).read().decode(self._web_page_encode);
                print("��ҳԴ�볤��{}".format(len(self._html_content)));
                break;
            except Exception as e:
                # count += 1;
                print(e);
                continue;

    # �����ҳԴ���루ʹ��requests��
    def _get_html_content_by_requests(self, url,decoding = None):
        while True:
            try:
                if self._is_useProxies:
                    proxies = ProiexsPool._get_random_ip();
                else:
                    proxies = None;
                print(proxies);
                res = requests.get(url=url,headers=self._headers,proxies=proxies,timeout=3,allow_redirects=False);
                if not decoding:
                    self._html_content = res.text;
                else:
                    self._html_content = res.content.decode(decoding);
                # self._html_content = res;
                break;
            except Exception as e:
                print(e);
                # ɾ�����ݿ��в���ʹ�õĴ���ip
                if proxies:
                    ip = list(proxies.values())[0].split("//")[1];
                    print("Ҫɾ����ip��"+ip);
                    ProiexsPool._delete_ip_from_db(ip);
                continue;

    # ƥ���������Ϣ��ʹ��������ʽ����ƥ�䣩
    def _match_user_need_by_regular(self,_regular_all_need,_regular_next_page = ""):
        reg_need = re.compile(_regular_all_need,re.S);
        # if not _regular_next_page:
        reg_next_page = re.compile(_regular_next_page,re.S);
        self._result_next_page = re.findall(reg_next_page, self._html_content);
        self._result_needs = re.findall(reg_need, self._html_content);

    # ƥ��������Ϣ��ʹ��BeautifulSoup����ƥ�䣩
    def _match_user_need_by_bSoup(self, *args):
        """
        �����û������ƥ������Ҫƥ��html�ı�����ƥ�䣨ֻ��ʹ��CSSѡ������������ƥ�䣩
        :param *args: ����ƥ��Ĺ���Ϊ��ʱ�׳��쳣���ɰ���˳�����δ�������ƥ�����
        :return: None
        """
        # �ж��Ƿ������
        if not args:
            raise TypeError("*****������Ҫ����һ������(ƥ�����)*****");
        # ���г���ƥ��
        bs = bSoup(self._html_content, "lxml");
        self._bs_parse_result = bs.select(args[0][0]);
        if len(args[0]) > 1:
            for bs_parse in args[0][1:]:
                # ��ֵת�ƣ���ֹself._bs_parse_result����ֶ��������
                first_tags = self._bs_parse_result.copy();
                self._bs_parse_result.clear();
                # ȡ���б��е�ÿ���ڵ㣬�������ƥ��
                for f_tag in first_tags:
                    second_tags = f_tag.select(bs_parse);
                    # ��Ϊ�ٴ�ƥ����ֵ��Ϊ�б�������Ҫ���ȡ������self._bs_parse_result
                    for s_tag in second_tags:
                        self._bs_parse_result.append(s_tag);
        return self._bs_parse_result;

    # ƥ��������Ϣ��ʹ��XPath����ƥ�䣩
    def _match_user_need_by_xpath(self):
        """
        ʹ��XPath����ƥ�䣬�÷������Եõ�һ��html�ĵ���
        :return: None
        """
        self._html_tree_xpath = etree.HTML(self._html_content);

    #�����ݽ��д���ķ���
    def _calc_result_user_need(self):
        pass;
        # �����õ����ݽ��д����������ݿ⣬д���ļ��ȣ�
        # # �ж��Ƿ�����һҳ
        # is_has = re.search(re.compile('\d+?',re.S), self._result_next_page[0])
        # if is_has:
        #     self._isHas_next_page = True;
        #     self._url = self._reorganize_string + self._result_next_page[0];
        # else:
        #     self._isHas_next_page = False;

    def _begin_catch(self):
        # ִ�з���
        # try:
        count = 1;
        #�ж��Ƿ���Ҫ��������
        if self._is_save_data_to_db:
            self._create_table();
        if self._is_save_data_to_excel:
            self._creat_excel_header(self._sheet_name,self._excel_heads);
        while self._isHas_next_page:
            # time.sleep(2)
            print("������ȡ�� {} ҳ.......".format(count).center(40,"*"));
            if self._get_html_type == 1:
                self._get_html_content_by_urllib();
            else:
                self._get_html_content_by_requests(self._url);
            if self._match_type == 1:
                # Ĭ�ϵ���ƥ�������ĵ���
                nothing = self._match_user_need_by_bSoup(self._bs_match_str);
            elif self._match_type == 2:
                self._match_user_need_by_xpath();
            else:
                self._match_user_need_by_regular(self._regular_all_need,self._regular_next_page);
            # ʵʱ�����ȡ����
            # print(self._result_needs);
            # print(self._result_next_page);

            self._calc_result_user_need();
            count += 1;
            if not self._isHas_next_page:
                print("��ȡ������");
                # break;
        if self._is_save_data_to_excel:
            # �����ݱ�������
            self._work_book.save(self._excel_name);
        # except Exception as e:
        #     print(e);
        # finally:
        #     if self._is_save_data_to_excel:
        #         #�����ݱ�������
        #         self._work_book.save(self._excel_name);

