# -*- coding: gbk -*-
__author__ = 'shyorange'
__data__ = '2018-09-26'

"""
˫������
    ��: ÿ���ڵ�������ָ���򣬼���ǰ���ͺ��
    �ڣ��ɴ�ͷ�ڵ㿪ʼ������Ҳ�ɴ�β�ڵ㿪ʼ����
    ?�����Խ�β�ڵ�ĺ��ָ��ͷ�ڵ��ǰ��
"""
class Node:

    def __init__(self, data, prev = None, next = None):
        """
        :param data: �������е�����
        :param prev: ָ��ǰ���ڵ�
        :param next: ָ���̽ڵ�
        """
        self._data = data;
        self._prev = prev;
        self._next = next;
    def __repr__(self):
        return (self._data);

class DDChainTable:
    def __init__(self):
        self._length = 0;  # ��ʾ������
        self._head = None; # ��ʾͷ���ڵ�
        self._tail = None; # ��ʾβ���ڵ�
        self._index_next = 0; # �������м�������

    #  �ж������Ƿ�Ϊ��
    def _isEmpty(self):
        """
        :return:True|False
        """
        if self._length == 0:
            print("����Ϊ�գ�����");
            return True;
        else:
            return False;

    #  �ж��û�����������Ƿ�Խ��
    def _isIndexRight(self, index):
        if index < 0:
            if abs(index) > self._length:
                raise IndexError("����Խ�磡����");
        else:
            if index >= self._length:
                raise IndexError("����Խ�磡����");

    # ������ĩβ���Ԫ��
    def _append(self, DataOrNode):
        """
        :param DataOrNode: ���ݻ�ڵ���Ķ���
        :return: None
        """
        item = None;
        #  �����ݰ�װΪNode���͵Ķ���
        if isinstance(DataOrNode, Node):
            item = DataOrNode;
        else:
            item = Node(DataOrNode);
        if not self._head:
            #  ���ͷ�ڵ�Ϊ��˵��������������
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

    #  ��������ɾ���ڵ�
    def _delete(self, index):
        """
        :param index:Ҫɾ���ڵ��������Ϊ����ʾ���Ų��ҡ�
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
            j = 0; # ������λ
            node = self._head; # ��ʾ��ǰ�ڵ�
            while node._next and j < index:
                node = node._next;
                j += 1;
            #  �޸ĵ�ǰǰ���ڵ�ͺ�̽ڵ��ָ��
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
                j = 1; # ������λ
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

    #  �����������ؽڵ�
    def _getItem(self, index):
        """
        :param index: Ҫ���ҽڵ������
        :return: None
        """
        if self._isEmpty():
            return ;
        self._isIndexRight(index);
        if index < 0:
            j = 1; # ������λ
            node = self._tail;
            while node:
                if j == abs(index):
                    return node;
                else:
                    node = node._prev;
                    j += 1;
            return None;
        else:
            j = 0; # ������λ
            node = self._head;
            while node:
                if j == index:
                    return node;
                else:
                    node = node._next;
                    j += 1;
            return None;

    #  ���ݽڵ�ֵ���ظýڵ������
    def _getIndex(self, data):
        """
        :param data: Ҫ����λ�õĽڵ�����
        :return: index ���ýڵ��������-1����ʾδ�ҵ���
        """
        if self._isEmpty():
            return ;
        j = 0; # ������λ
        node = self._head; # ��ʾ��ǰ�ڵ�
        while node:
            if node._data == data:
                return j;
            else:
                node = node._next;
                j += 1;
        return -1;

    #  �޸�ָ�������ڵ��ֵ
    def _update(self, index, data):
        """
        :param index: Ҫ�޸Ľڵ������
        :param data: �޸ĺ��ֵ
        :return: None
        """
        if self._isEmpty():
            return;
        self._isIndexRight(index);
        # ��ʼ�޸�
        node = self._getItem(index);
        if node:
            node._data = data;
        else:
            print("δ�ҵ���������Ӧ�Ľڵ㡣");

    #  ��ָ��λ�ò���ڵ�
    def _insert(self, index, DataOrNode):
        """
        :param index: λ��
        :param DataOrNode: ����
        :return: None
        """
        if self._isEmpty():
            return ;
        self._isIndexRight(index);
        #  ��װ����
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
            j = 0; # ������λ
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
            j = 1; # ������λ
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

    #   ģ��һ����������ÿ�ε��ø÷�����������ؽڵ�
    def _next(self):
        """
        :return: �ڵ�
        """
        if self._index_next < self._length:
            every_node = self._getItem(self._index_next);
            self._index_next += 1;
            return (every_node);
        return None;

    #  ���������ʱ��ֱ����������е���������
    def __repr__(self):
        if self._length == 0:
            return("����Ϊ�գ�����");
        node = self._head;
        result = "";
        while node:
            result += node._data + " ";
            node = node._next;
        return result;

    #  ��len(����)ʱ������������
    def __len__(self):
        return (self._length);

if __name__ == '__main__':
    chain = DDChainTable();
    print(chain);
    chain._append("���");
    chain._append("a");
    chain._append("����");
    chain._append("123");
    chain._append("###");
    print(chain);
    chain._delete(-4);
    print(chain);
    chain._update(-2, "hello");
    print(chain);
    chain._insert(-1, "world");
    print(chain);
