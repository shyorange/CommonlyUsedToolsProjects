# -*- coding: gbk -*-
__author__ = 'shyorange'
__data__ = '2018-10-20'

"""�Ľ�Scrapy_Redis��ȥ�ػ��ƣ�ʹ�����ʡ�ڴ�"""
## Scrapy_Redis��ȥ�ػ���
    # 1����ÿ��Request������һ��ָ�ƣ���ָ����40��16���Ƶ��ַ����
    # 2������ָ�ƴ���Redis���ϣ����ڴ��У������ü��ϵ�����ʵ��ȥ��
## ���⣺
    # һ���ӽ�ռ8b��Ϊ1B������16������Ϊһ���ֽڣ�
    # һ��16������ռ��4b�棬��һ��ָ��ռ��20B�ռ�
    # һ���ָ��ռ��200KB
    # һ�ڸ�ָ��ռ��2GB
    # ���������ﵽ���ڼ���ʱ��ռ��̫���ڴ�
## ��¡��������BloomFilter�����Խ����һ����
    # �ù�����ʹ��λ�����ʾһ������⼯�ϲ�ͨ�������㷨�ж�һ��Ԫ���Ƿ����ĳ����
    # λ���飺ֻ���0��1����ֻ����λ���������
## ʵ�ֹ���
    # 1������һ��mλ��λ���飬��ʼֵ��Ϊ0
    # 2����������n��������Request
    # 3: BloomFilter����k��ɢ�к��������ڽ�Requestӳ�䵽λ����ĺ�����
    # 4��ÿ�������Request���ξ���k��ɢ�к�������õ�k��λ��
    # 5�����ϲ��ĵ���k��λ�����ξ���λ���飬����Ӧλ�õ�0��Ϊ1
    # 6���ж�ĳ��Request�Ƿ��Ѿ����ڣ��򽫸�Request����k��ɢ�к����õ�k��λ�ú�
        # ��λ������һ�β�����k��λ�ã�����Ϊ 1�����ʾ��Request����
        # ����һ����Ϊ 1�����ʾ��Request����������ȡ������
    ## ע��m(λ���鳤��) > n(Request�ĸ���)*k(ɢ�к����ĸ���)
        # Ϊ�˷�ֹ���ֹ��������
#### �ù���������һ���������ʣ�����n��������������֮���� ####
## λ���㣺���������������Ƚϣ�
    # &/and����λ�룩 ��1,1ȡ1��0,0ȡ0��0,1ȡ0
    # |/or����λ�򣩣�1,1ȡ1��0,0ȡ0��0,1ȡ1
"""ʵ�ּ��׵�BloomFilter"""
class MyHashMap(object):

    """��������ʵ��һ���򵥵�ɢ�к�������"""
    def __init__(self, m, seed):
        self.m = m; # Ϊ����ĳ���
        self.seed = seed; # ��ʾ���ĸ�ɢ�к�������Ϊ����ֻ��һ��ɢ�к����������Ҫһ�������������ֵ�ǰ�ǵڼ���ɢ�к�����
    def hash(self, value):
        """
        �򵥵�ɢ�к���
        :param value: ����������
        :return: Ҫӳ�䵽λ�����λ��
        """
        ret = 0;
        # ���������е�ÿ����ֵ
        for i in range(len(value)):
            # ��ÿ����ֵȡASCII��ֵ�����seed���е������
            ret += self.seed * ret + ord(value[i]);
        # ����һ��λ����֮���ֵ
        return (self.m - 1) & ret;

BLOOMFILTER_HASH_NUM = 6; # ɢ�к����ĸ���
BLOOMFILTER_BIT = 30; # λ����ĳ���

class BloomFilter(object):
    def __init__(self, serve, key, bit = BLOOMFILTER_BIT, hash_num = BLOOMFILTER_HASH_NUM):
        """
        :param serve: Redis��������Ӷ���
        :param key: mλλ���������
        :param bit: λ����ĳ���
        :param hash_num: ɢ�к����ĸ���
        """
        self.m = 1 << bit;# λ���鳤�ȣ�λ�����൱��2^30
        self.seeds = range(hash_num); # �б���ÿ������ʾһ��ɢ�к���
        #  ɢ�к�����Ķ���
        # self.maps = [];
        # for s in self.seeds:
        #     self.maps.append(MyHashMap(self.m,s));
        self.maps = [MyHashMap(self.m, seed) for seed in self.seeds];
        self.serve = serve;
        self.key = key;

    def is_exists(self, value):
        """
        �ж������Ƿ���ڵķ���
        :param value: ���жϵ�����
        :return: o��1��0�������ڡ�1�����ڣ�
        """
        if not value:
            return False;
        exist = 1;
        for m in self.maps:
            offset = m.hash(value); # ��ö�Ӧ��λ��
            # �ó˷�Ҳһ��
            exist = exist & self.serve.getbit(self.key, offset);
        return exist;

    def insert(self, value):
        """
        ��valueӳ�䵽λ������
        :param value: ��ӳ�������
        :return:None
        """
        for m in self.maps:
            offset = m.hash(value);
            # ����Ӧoffsetλ�õ�ֵ��Ϊ1
            self.serve.setbit(self.key,offset,1);


if __name__ == '__main__':
    """����BloomFilter"""
    # from redis import StrictRedis;
    import redis;
    conn = redis.Redis(host="localhost",port=6379,password="123456");
    bf = BloomFilter(conn,"testBF",5,6);
    bf.insert("HELLO");
    bf.insert("world!");
    res = bf.is_exists("hello");
    print(bool(res));
    res = bf.is_exists("world");
    print(bool(res));
    res = bf.is_exists("world!");
    print(bool(res));
    """�ڷֲ�ʽ������ʹ�ø���ķ���"""
    ## 1����scrapy_redis.dupefilter.RFPDupeFilter��ĳ�ʼ��������
        # ����һ������Ķ���
    ## 2����RFPDupeFilter���request_seen()�������޸Ĳ��ִ���
        # ����
        # added = self.server.sadd(self.key, fp)
        #   return added == 0
        # �޸�Ϊ��
        # if self.bf.is_exists(fp):
        #       return True;
        # self.bf.insert(fp);
        # return False