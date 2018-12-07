# -*- coding: gbk -*-
__author__ = 'shyorange'
__data__ = '2018-09-25'

"""一个简单的链表类"""

class Node:

    """节点类"""
    def __init__(self, data, next = None):
        self._data = data;
        self._next = next;
    def __repr__(self):
        return str(self._data);

class ChainTable:

    """链表类"""
    def __init__(self):
        self._head = None; # 表示链表的头节点
        self._length = 0; # 表示链表的长度
        self._index_next = 0; # 用于_next()函数中的计数

    #  判断链表是否为空
    def _isEmpty(self):
        return (self._length == 0);

    # 在链表末尾追加元素
    def _append(self, DataOrNode):
        """
        :param DataOrNode: 数据或节点类型的对象
        :return: None
        """
        # 将数据的类型统一为Node类
        item = None;
        if isinstance(DataOrNode, Node):
            item = DataOrNode;
        else:
            item = Node(DataOrNode);
        if not self._head:
            self._head = item;
            self._length += 1;
        else:
            node = self._head; #  存储当前节点
            while node._next:  # 直到最后一个节点
                node = node._next;
            node._next = item;
            self._length += 1;

    # 根据索引删除数据
    def _delete(self, index):
        """
        :param index: 要删除元素的索引
        :return: None
        """
        if self._isEmpty():
            print("链表为空！！！");
            return;
        if index < 0 and index >= self._length:
            raise IndexError("索引错误！！！");
        if index == 0:
            self._head = self._head._next;
            self._length -= 1;
        else:
            j = 0; # 辅助定位
            prev = self._head;
            node = self._head;  # 表示当前节点
            while node._next and j < index:
                prev = node;
                node = node._next;
                j += 1;
            if j == index:
                prev._next = node._next;
                self._length -= 1;

    # 在指定位置插入数据
    def _insert(self, index, DataOrNode):
        """
        :param index: 要插入的位置
        :param DataOrNode: 要插入的数据
        :return: None
        """
        if self._isEmpty():
           print("链表为空！！！");
           return;
        if index < 0 and index >= self._length:
            raise IndexError("索引错误！！！");
        # 将数据的类型统一为Node类
        item = None;
        if isinstance(DataOrNode, Node):
            item = DataOrNode;
        else:
            item = Node(DataOrNode);
        if index == 0:  # 如果插入的位置为0
            item._next = self._head;
            self._head = item;
            self._length += 1;
        else:
            j = 0; # 辅助定位
            prev = self._head; # 表示当前节点的上一节点
            node = self._head; # 表示当前节点
            while node._next and j < index: # 保证当前节点不是最后一个节点
                prev = node;
                node = node._next;
                j += 1;
            if j == index:
                prev._next = item;
                item._next = node;
                self._length += 1;

    # 修改某一索引的元素值
    def _update(self, index, newData):
        """
        :param index: 要修改元素的索引
        :param newData: 新的元素值
        :return: None
        """
        if self._isEmpty():
           print("链表为空！！！");
           return;
        if index < 0 and index >= self._length:
            raise IndexError("索引错误！！！");
        if index == 0:
            self._head._data = newData;
        else:
            j = 0; # 辅助定位
            node = self._head;
            while node._next and j < index:
                node = node._next;
                j += 1;
            if j == index:
                node._data = newData;

    # 根据索引来查找节点的数据
    def _getItem(self, index):
        """
        :param index: 要查找的索引
        :return: Item: 该索引对应的节点
        """
        if self._isEmpty():
            print("链表为空！！！");
            return;
        if index < 0 or index >= self._length:
            raise IndexError("索引错误！！！");
        j = 0; # 辅助定位
        node = self._head; # 表示当前节点
        while node._next and j < index:
            node = node._next;
            j += 1;
        return node;

    # 根据元素找到改元素的索引， 只返回第一个相同元素的位置
    def _getIndex(self, data):
        """
        :param data:要查找位置的元素
        :return: Index: 该元素在链表中的位置
        """
        if self._isEmpty():
            print("链表为空！！！");
            return;
        j = 0; # 辅助定位
        node = self._head; # 表示当前节点
        while node:
            if node._data == data:
                return j;
            else:
                node = node._next;
                j += 1;
        if j == self._length:
            return None;

    #清空链表的方法
    def _clear(self):
        """
        :return: None
        """
        self._head = None;
        self._length = 0;

    # 像生成器一样逐个返回链表中的元素
    def _next(self):
        """
        :return: every_data: 链表中的节点
        """
        every_data = self._getItem(self._index_next);
        self._index_next += 1;
        yield every_data;

    #  使用 len(ChainTable) 时返回链表的长度
    def __len__(self):
        return self._length;

    # 根据对象输出元素
    def __repr__(self):
        """
        :return:None
        """
        if self._isEmpty():
            print("链表为空！！！");
            return;
        result = "";
        j = 0; # 辅助定位
        while j < self._length:
            result += str(self._getItem(j)) + " ";
            j += 1;
        return result;

