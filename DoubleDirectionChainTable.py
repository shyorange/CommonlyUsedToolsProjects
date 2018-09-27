# -*- coding: gbk -*-
__author__ = 'shyorange'
__data__ = '2018-09-26'

"""
双向链表：
    ①: 每个节点有两个指针域，即：前驱和后继
    ②：可从头节点开始遍历，也可从尾节点开始遍历
    ?：可以将尾节点的后继指向头节点的前驱
"""
class Node:

    def __init__(self, data, prev = None, next = None):
        """
        :param data: 数据域中的数据
        :param prev: 指向前驱节点
        :param next: 指向后继节点
        """
        self._data = data;
        self._prev = prev;
        self._next = next;
    def __repr__(self):
        return (self._data);

class DDChainTable:
    def __init__(self):
        self._length = 0;  # 表示链表长度
        self._head = None; # 表示头部节点
        self._tail = None; # 表示尾部节点
        self._index_next = 0; # 迭代器中计数变量

    #  判断链表是否为空
    def _isEmpty(self):
        """
        :return:True|False
        """
        if self._length == 0:
            print("链表为空！！！");
            return True;
        else:
            return False;

    #  判断用户传入的索引是否越界
    def _isIndexRight(self, index):
        if index < 0:
            if abs(index) > self._length:
                raise IndexError("索引越界！！！");
        else:
            if index >= self._length:
                raise IndexError("索引越界！！！");

    # 往链表末尾添加元素
    def _append(self, DataOrNode):
        """
        :param DataOrNode: 数据或节点类的对象
        :return: None
        """
        item = None;
        #  将数据包装为Node类型的对象
        if isinstance(DataOrNode, Node):
            item = DataOrNode;
        else:
            item = Node(DataOrNode);
        if not self._head:
            #  如果头节点为空说明链表中无数据
            self._head = item;
            self._tail = item;
            self._length += 1;
        else:
            node = self._head;
            while node._next:
                node = node._next;
            item._prev = node;
            node._next = item;
            self._tail = item;
            self._length += 1;

    #  根据索引删除节点
    def _delete(self, index):
        """
        :param index:要删除节点的索引。为负表示倒着查找。
        :return: None
        """
        if self._isEmpty():
            return ;
        self._isIndexRight(index);
        if index == 0:
            self._head = self._head._next;
            self._head._prev = None;
            self._length -= 1;
        elif index > 0:
            j = 0; # 辅助定位
            node = self._head; # 表示当前节点
            while node._next and j < index:
                node = node._next;
                j += 1;
            #  修改当前前驱节点和后继节点的指向
            node._prev._next = node._next;
            if node._next:
                node._next._prev = node._prev;
            elif not node._next:
                self._tail = node._prev;
            self._length -= 1;
        else:
            if index == -1:
                self._tail._prev._next= None;
                self._tail = self._tail._prev;
                self._length -= 1;
            else:
                j = 1; # 辅助定位
                node =self._tail;
                while node._prev and j < abs(index):
                    node = node._prev;
                    j += 1;
                node._next._prev = node._prev;
                if node._prev:
                    node._prev._next = node._next;
                elif not node._prev:
                    self._head = node._next;
                self._length -= 1;

    #  根据索引返回节点
    def _getItem(self, index):
        """
        :param index: 要查找节点的索引
        :return: None
        """
        if self._isEmpty():
            return ;
        self._isIndexRight(index);
        if index < 0:
            j = 1; # 辅助定位
            node = self._tail;
            while node:
                if j == abs(index):
                    return node;
                else:
                    node = node._prev;
                    j += 1;
            return None;
        else:
            j = 0; # 辅助定位
            node = self._head;
            while node:
                if j == index:
                    return node;
                else:
                    node = node._next;
                    j += 1;
            return None;

    #  根据节点值返回该节点的索引
    def _getIndex(self, data):
        """
        :param data: 要查找位置的节点数据
        :return: index ：该节点的索引（-1：表示未找到）
        """
        if self._isEmpty():
            return ;
        j = 0; # 辅助定位
        node = self._head; # 表示当前节点
        while node:
            if node._data == data:
                return j;
            else:
                node = node._next;
                j += 1;
        return -1;

    #  修改指定索引节点的值
    def _update(self, index, data):
        """
        :param index: 要修改节点的索引
        :param data: 修改后的值
        :return: None
        """
        if self._isEmpty():
            return;
        self._isIndexRight(index);
        # 开始修改
        node = self._getItem(index);
        if node:
            node._data = data;
        else:
            print("未找到该索引对应的节点。");

    #  在指定位置插入节点
    def _insert(self, index, DataOrNode):
        """
        :param index: 位置
        :param DataOrNode: 数据
        :return: None
        """
        if self._isEmpty():
            return ;
        self._isIndexRight(index);
        #  包装数据
        item = None;
        if isinstance(DataOrNode, Node):
            item = DataOrNode;
        else:
            item = Node(DataOrNode);
        if index == 0:
            item._next = self._head;
            self._head_prev = item;
            self._head = item;
            self._length += 1;
        elif index > 0:
            j = 0; # 辅助定位
            node = self._head;
            while node._next and j < index:
                node = node._next;
                j += 1;
            item._prev = node._prev;
            node._prev._next = item;
            item._next = node;
            node._prev = item;
            self._length += 1;
        else:
            j = 1; # 辅助定位
            node = self._tail;
            while node._prev and j < abs(index):
                node = node._prev;
                j += 1;
            item._prev = node;
            item._next = node._next;
            if node._next:
                node._next._prev = item;
            if not node._next:
                self._tail = item
            node._next = item;
            self._length += 1;

    #   模仿一个迭代器，每次调用该方法，逐个返回节点
    def _next(self):
        """
        :return: 节点
        """
        if self._index_next < self._length:
            every_node = self._getItem(self._index_next);
            self._index_next += 1;
            return (every_node);
        return None;

    #  当输出对象时，直接输出链表中的所有数据
    def __repr__(self):
        if self._length == 0:
            return("链表为空！！！");
        node = self._head;
        result = "";
        while node:
            result += node._data + " ";
            node = node._next;
        return result;

    #  当len(对象)时，返回链表长度
    def __len__(self):
        return (self._length);

if __name__ == '__main__':
    chain = DDChainTable();
    print(chain);
    chain._append("你好");
    chain._append("a");
    chain._append("世界");
    chain._append("123");
    chain._append("###");
    print(chain);
    chain._delete(-4);
    print(chain);
    chain._update(-2, "hello");
    print(chain);
    chain._insert(-1, "world");
    print(chain);
