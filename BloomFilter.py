# -*- coding: gbk -*-
__author__ = 'shyorange'
__data__ = '2018-10-20'

"""改进Scrapy_Redis的去重机制，使其更节省内存"""
## Scrapy_Redis的去重机制
    # 1：对每个Request都产生一个指纹，该指纹由40个16进制的字符组成
    # 2：将该指纹存入Redis集合（在内存中），利用集合的特性实现去重
## 问题：
    # 一个子节占8b，为1B（两个16进制数为一个字节）
    # 一个16进制数占用4b存，则一个指纹占用20B空间
    # 一万个指纹占用200KB
    # 一亿个指纹占用2GB
    # 当数据量达到上亿级别时将占用太多内存
## 布隆过滤器（BloomFilter）可以解决这一问题
    # 该过滤器使用位数组表示一个待检测集合并通过概率算法判断一个元素是否存在某集合
    # 位数组：只存放0和1，并只进行位运算的数组
## 实现过程
    # 1：声明一个m位的位数组，初始值都为0
    # 2：队列中有n个待检测的Request
    # 3: BloomFilter中有k个散列函数（用于将Request映射到位数组的函数）
    # 4：每个待检测Request依次经过k个散列函数，则得到k个位置
    # 5：将上步的到的k个位置依次经过位数组，将对应位置的0变为1
    # 6：判断某个Request是否已经存在，则将该Request经过k个散列函数得到k个位置后
        # 在位数组中一次查找这k个位置，若都为 1，则表示该Request存在
        # 若有一个不为 1，则表示该Request不存在于爬取队列中
    ## 注：m(位数组长度) > n(Request的个数)*k(散列函数的个数)
        # 为了防止出现过多的误判
#### 该过滤器存在一定的误判率，随着n的增加误判率随之增加 ####
## 位运算：（两个二进制数比较）
    # &/and（按位与） ：1,1取1，0,0取0，0,1取0
    # |/or（按位或）：1,1取1，0,0取0，0,1取1
"""实现简易的BloomFilter"""
class MyHashMap(object):

    """该类用于实现一个简单的散列函数的类"""
    def __init__(self, m, seed):
        self.m = m; # 为数组的长度
        self.seed = seed; # 表示是哪个散列函数（因为这里只有一个散列函数，因此需要一个参数用于区分当前是第几个散列函数）
    def hash(self, value):
        """
        简单的散列函数
        :param value: 待检测的数据
        :return: 要映射到位数组的位置
        """
        ret = 0;
        # 遍历数据中的每个数值
        for i in range(len(value)):
            # 对每个数值取ASCII码值，混合seed进行迭代求和
            ret += self.seed * ret + ord(value[i]);
        # 返回一个位运算之后的值
        return (self.m - 1) & ret;

BLOOMFILTER_HASH_NUM = 6; # 散列函数的个数
BLOOMFILTER_BIT = 30; # 位数组的长度

class BloomFilter(object):
    def __init__(self, serve, key, bit = BLOOMFILTER_BIT, hash_num = BLOOMFILTER_HASH_NUM):
        """
        :param serve: Redis数组的连接对象
        :param key: m位位数组的名称
        :param bit: 位数组的长度
        :param hash_num: 散列函数的个数
        """
        self.m = 1 << bit;# 位数组长度，位运算相当于2^30
        self.seeds = range(hash_num); # 列表中每个数表示一个散列函数
        #  散列函数类的对象
        # self.maps = [];
        # for s in self.seeds:
        #     self.maps.append(MyHashMap(self.m,s));
        self.maps = [MyHashMap(self.m, seed) for seed in self.seeds];
        self.serve = serve;
        self.key = key;

    def is_exists(self, value):
        """
        判断数据是否存在的方法
        :param value: 待判断的数据
        :return: o或1（0：不存在。1：存在）
        """
        if not value:
            return False;
        exist = 1;
        for m in self.maps:
            offset = m.hash(value); # 获得对应的位置
            # 用乘法也一样
            exist = exist & self.serve.getbit(self.key, offset);
        return exist;

    def insert(self, value):
        """
        将value映射到位数组中
        :param value: 待映射的数据
        :return:None
        """
        for m in self.maps:
            offset = m.hash(value);
            # 将对应offset位置的值设为1
            self.serve.setbit(self.key,offset,1);


if __name__ == '__main__':
    """测试BloomFilter"""
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
    """在分布式爬虫中使用该类的方法"""
    ## 1：在scrapy_redis.dupefilter.RFPDupeFilter类的初始化方法中
        # 生成一个该类的对象
    ## 2：在RFPDupeFilter类的request_seen()方法中修改部分代码
        # 将：
        # added = self.server.sadd(self.key, fp)
        #   return added == 0
        # 修改为：
        # if self.bf.is_exists(fp):
        #       return True;
        # self.bf.insert(fp);
        # return False