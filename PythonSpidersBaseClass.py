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
"""所有简单爬虫的基类，其他爬虫只需继承该类即可"""
class Catch:
    def __init__(self, url):
        self._url = url ;
        # 使用哪种方式获取网页源代码（默认使用requests，值为：1 时使用urllib）
        self._get_html_type = None;
        # 使用哪种方式进行匹配所需的数据（默认使用regular， 值为：1 时使用BeautifulSoup4，值为：2时使用XPath）
        self._match_type = None;
        # 当使用BeautifulSoup匹配时该属性才有用（是一个列表）
        self._bs_parse_result = None;
        # bSoup的匹配规则，默认匹配整个文档树
        self._bs_match_str = "html"
        # 使用XPath匹配时，给该属性赋值，值为一个XPath文档树
        self._html_tree_xpath = None;
        # 用于记录行号的标志
        self._count_row = 1;
        self._html_content = ""; # 网页源代码
        self._regular_all_need = ""; # 匹配所需资源的正则式
        self._regular_next_page = ""; # 匹配下一页url链接的正则式
        self._web_page_encode = "utf-8";
        self._headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/56.0.2924.90 Safari/537.36 2345Explorer/9.3.2.17331"
        };
        # 是否使用代理ip (默认为使用)
        self._is_useProxies = True;
        self._result_needs = [] #"爬取的结果，是一个列表";
        self._result_next_page = [] #"爬取到的下一页的url链接(为空表示爬取结束)";
        self._isHas_next_page = True; #是否还有下一页
        self._reorganize_string = ""; #当需要重组url时，给这个属性赋值。
        #连接数据库的属性
        self._is_save_data_to_db = False; # 是否保存数据，默认不保存（保存到数据库）
        self._is_save_data_to_excel = False; # 是否保存数据，默认不保存（保存到Excel表格）
        self._conn_db = None;
        self._cursor_db = None;
        self._table_name = ""; # 表名
        self._create_table_tuple = (); # 建表语句所需的字段名：(包含所有字段的元组)
        # self._insert_data_to_table_tuple = None; # 插入数据语句所需的数据 (一个包含所有数据的元组)
        #创建Excel表格所需的属性
        self._work_book = None;
        self._sheet = None;
        self._excel_heads = None;
        self._excel_name = "";
        self._sheet_name = "";

    def _creat_excel_header(self,sheet_name, *args):
        """
        为Excel表格创建表头的方法
        :param sheet_name: 要创建表的表名
        :param args: 所有的表头信息
        :return: None
        *args与args的区别：
                *args直接就是所有数据
                 args是一个包含数据的元组
        """
        self._work_book = xlwt.Workbook(encoding="utf-8");
        self._sheet = self._work_book.add_sheet(sheet_name);
        # 此处直接遍历元组
        print(args[0]);
        for index,head in enumerate(args[0]):
            self._sheet.write(0,index,head);

    def _write_data_to_excel(self, *args):
        '''
        将数据写入Excel文件
        :param args: 数据（元组）
        :return: None
        '''
        print("正在将第{}条数据写入表格......".format(self._count_row));

        for idx, dat in enumerate(args[0]):
            self._sheet.write(self._count_row,idx,str(dat).strip());
        print("数据写入表格完毕。");
        # 保存数据
        self._work_book.save(self._excel_name);
        self._count_row += 1;

    #连接数据库的法方法
    def _connect_databse(self):
        self._conn_db = sqlite3.connect("PythonSpiderData.db");
        self._cursor_db = self._conn_db;

    # 关闭数据库的方法
    def _close_database(self):
        self._conn_db.commit();
        self._cursor_db.close();
        self._conn_db.close();

    def _create_table(self):
        """
        创建数据库中的数据表的方法
        :return:
        """
        self._connect_databse();
        # 遍历字段字典，取出所需的信息
        create_table_sql = "";
        for k in self._create_table_tuple:
            create_table_sql += ", "+k+" varchar";
        self._cursor_db.execute("create table if not exists "+self._table_name+"(id integer primary key"+create_table_sql+")");
        self._close_database();

    # 保存数据的方法(到数据库)
    def _save_data_to_sqlite3(self,table_name,*args):
        self._connect_databse();
        # 对要插入的数据进行重组
        ziduans = "";
        insert_sql = "";
        for index,key in enumerate(self._create_table_tuple):
            if index+1 == len(self._create_table_tuple):
                ziduans += key;
            else:
                ziduans += key+",";
        for index,i in enumerate(args[0]):
            if index+1 == len(args[0]):
                insert_sql += "'"+str(i).replace("'","’")+"'";
            else:
                insert_sql += "'"+str(i).replace("'","’")+"',";
        self._cursor_db.execute("""insert into {}({}) values({})""".format(table_name,ziduans,insert_sql));
        self._close_database();

    # 获得网页源代码（使用urllib）
    def _get_html_content_by_urllib(self):
        # count = 1;
        while True:
            try:
                # if count > 4:
                #     print("该链接已经重连四次，可能失效。:{}".format(self._url));
                #     break;
                re_request = urllib.request.Request(self._url,headers = self._headers);
                self._html_content = urllib.request.urlopen(re_request,timeout=2).read().decode(self._web_page_encode);
                print("网页源码长度{}".format(len(self._html_content)));
                break;
            except Exception as e:
                # count += 1;
                print(e);
                continue;

    # 获得网页源代码（使用requests）
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
                # 删除数据库中不能使用的代理ip
                if proxies:
                    ip = list(proxies.values())[0].split("//")[1];
                    print("要删除的ip："+ip);
                    ProiexsPool._delete_ip_from_db(ip);
                continue;

    # 匹配所需的信息（使用正则表达式进行匹配）
    def _match_user_need_by_regular(self,_regular_all_need,_regular_next_page = ""):
        reg_need = re.compile(_regular_all_need,re.S);
        # if not _regular_next_page:
        reg_next_page = re.compile(_regular_next_page,re.S);
        self._result_next_page = re.findall(reg_next_page, self._html_content);
        self._result_needs = re.findall(reg_need, self._html_content);

    # 匹配所需信息（使用BeautifulSoup进行匹配）
    def _match_user_need_by_bSoup(self, *args):
        """
        根据用户传入的匹配规则对要匹配html文本进行匹配（只能使用CSS选择器方法进行匹配）
        :param *args: 进行匹配的规则（为空时抛出异常，可按照顺序依次传入所有匹配规则）
        :return: None
        """
        # 判断是否传入参数
        if not args:
            raise TypeError("*****至少需要传入一个参数(匹配规则)*****");
        # 进行初次匹配
        bs = bSoup(self._html_content, "lxml");
        self._bs_parse_result = bs.select(args[0][0]);
        if len(args[0]) > 1:
            for bs_parse in args[0][1:]:
                # 将值转移，防止self._bs_parse_result里出现多余的数据
                first_tags = self._bs_parse_result.copy();
                self._bs_parse_result.clear();
                # 取出列表中的每个节点，进行逐个匹配
                for f_tag in first_tags:
                    second_tags = f_tag.select(bs_parse);
                    # 因为再次匹配后的值仍为列表，所以需要逐个取出放入self._bs_parse_result
                    for s_tag in second_tags:
                        self._bs_parse_result.append(s_tag);
        return self._bs_parse_result;

    # 匹配所需信息（使用XPath进行匹配）
    def _match_user_need_by_xpath(self):
        """
        使用XPath进行匹配，该方法可以得到一个html文档树
        :return: None
        """
        self._html_tree_xpath = etree.HTML(self._html_content);

    #对数据进行处理的方法
    def _calc_result_user_need(self):
        pass;
        # 对有用的数据进行处理（插入数据库，写入文件等）
        # # 判断是否有下一页
        # is_has = re.search(re.compile('\d+?',re.S), self._result_next_page[0])
        # if is_has:
        #     self._isHas_next_page = True;
        #     self._url = self._reorganize_string + self._result_next_page[0];
        # else:
        #     self._isHas_next_page = False;

    def _begin_catch(self):
        # 执行方法
        # try:
        count = 1;
        #判断是否需要保存数据
        if self._is_save_data_to_db:
            self._create_table();
        if self._is_save_data_to_excel:
            self._creat_excel_header(self._sheet_name,self._excel_heads);
        while self._isHas_next_page:
            # time.sleep(2)
            print("正在爬取第 {} 页.......".format(count).center(40,"*"));
            if self._get_html_type == 1:
                self._get_html_content_by_urllib();
            else:
                self._get_html_content_by_requests(self._url);
            if self._match_type == 1:
                # 默认的是匹配整个文档树
                nothing = self._match_user_need_by_bSoup(self._bs_match_str);
            elif self._match_type == 2:
                self._match_user_need_by_xpath();
            else:
                self._match_user_need_by_regular(self._regular_all_need,self._regular_next_page);
            # 实时监控爬取数据
            # print(self._result_needs);
            # print(self._result_next_page);

            self._calc_result_user_need();
            count += 1;
            if not self._isHas_next_page:
                print("爬取结束。");
                # break;
        if self._is_save_data_to_excel:
            # 将数据保存进表格
            self._work_book.save(self._excel_name);
        # except Exception as e:
        #     print(e);
        # finally:
        #     if self._is_save_data_to_excel:
        #         #将数据保存进表格
        #         self._work_book.save(self._excel_name);

