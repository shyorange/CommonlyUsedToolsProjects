# -*- coding: gbk -*-
__author__ = 'shyorange'
__data__ = '2018-09-25'

"""�Լ�д��������"""

class Node:

    """�ڵ���"""
    def __init__(self, data, next = None):
        self._data = data;
        self._next = next;
    def __repr__(self):
        return str(self._data);

class ChainTable:

    """������"""
    def __init__(self):
        self._head = None; # ��ʾ�����ͷ�ڵ�
        self._length = 0; # ��ʾ����ĳ���
        self._index_next = 0; # ����_next()�����еļ���

    #  �ж������Ƿ�Ϊ��
    def _isEmpty(self):
        return (self._length == 0);

    # ������ĩβ׷��Ԫ��
    def _append(self, DataOrNode):
        """
        :param DataOrNode: ���ݻ�ڵ����͵Ķ���
        :return: None
        """
        # �����ݵ�����ͳһΪNode��
        item = None;
        if isinstance(DataOrNode, Node):
            item = DataOrNode;
        else:
            item = Node(DataOrNode);
        if not self._head:
            self._head = item;
            self._length += 1;
        else:
            node = self._head; #  �洢��ǰ�ڵ�
            while node._next:  # ֱ�����һ���ڵ�
                node = node._next;
            node._next = item;
            self._length += 1;

    # ��������ɾ������
    def _delete(self, index):
        """
        :param index: Ҫɾ��Ԫ�ص�����
        :return: None
        """
        if self._isEmpty():
            print("����Ϊ�գ�����");
            return;
        if index < 0 and index >= self._length:
            raise IndexError("�������󣡣���");
        if index == 0:
            self._head = self._head._next;
            self._length -= 1;
        else:
            j = 0; # ������λ
            prev = self._head;
            node = self._head;  # ��ʾ��ǰ�ڵ�
            while node._next and j < index:
                prev = node;
                node = node._next;
                j += 1;
            if j == index:
                prev._next = node._next;
                self._length -= 1;

    # ��ָ��λ�ò�������
    def _insert(self, index, DataOrNode):
        """
        :param index: Ҫ�����λ��
        :param DataOrNode: Ҫ���������
        :return: None
        """
        if self._isEmpty():
           print("����Ϊ�գ�����");
           return;
        if index < 0 and index >= self._length:
            raise IndexError("�������󣡣���");
        # �����ݵ�����ͳһΪNode��
        item = None;
        if isinstance(DataOrNode, Node):
            item = DataOrNode;
        else:
            item = Node(DataOrNode);
        if index == 0:  # ��������λ��Ϊ0
            item._next = self._head;
            self._head = item;
            self._length += 1;
        else:
            j = 0; # ������λ
            prev = self._head; # ��ʾ��ǰ�ڵ����һ�ڵ�
            node = self._head; # ��ʾ��ǰ�ڵ�
            while node._next and j < index: # ��֤��ǰ�ڵ㲻�����һ���ڵ�
                prev = node;
                node = node._next;
                j += 1;
            if j == index:
                prev._next = item;
                item._next = node;
                self._length += 1;

    # �޸�ĳһ������Ԫ��ֵ
    def _update(self, index, newData):
        """
        :param index: Ҫ�޸�Ԫ�ص�����
        :param newData: �µ�Ԫ��ֵ
        :return: None
        """
        if self._isEmpty():
           print("����Ϊ�գ�����");
           return;
        if index < 0 and index >= self._length:
            raise IndexError("�������󣡣���");
        if index == 0:
            self._head._data = newData;
        else:
            j = 0; # ������λ
            node = self._head;
            while node._next and j < index:
                node = node._next;
                j += 1;
            if j == index:
                node._data = newData;

    # �������������ҽڵ������
    def _getItem(self, index):
        """
        :param index: Ҫ���ҵ�����
        :return: Item: ��������Ӧ�Ľڵ�
        """
        if self._isEmpty():
            print("����Ϊ�գ�����");
            return;
        if index < 0 or index >= self._length:
            raise IndexError("�������󣡣���");
        j = 0; # ������λ
        node = self._head; # ��ʾ��ǰ�ڵ�
        while node._next and j < index:
            node = node._next;
            j += 1;
        return node;

    # ����Ԫ���ҵ���Ԫ�ص������� ֻ���ص�һ����ͬԪ�ص�λ��
    def _getIndex(self, data):
        """
        :param data:Ҫ����λ�õ�Ԫ��
        :return: Index: ��Ԫ���������е�λ��
        """
        if self._isEmpty():
            print("����Ϊ�գ�����");
            return;
        j = 0; # ������λ
        node = self._head; # ��ʾ��ǰ�ڵ�
        while node:
            if node._data == data:
                return j;
            else:
                node = node._next;
                j += 1;
        if j == self._length:
            return None;

    #�������ķ���
    def _clear(self):
        """
        :return: None
        """
        self._head = None;
        self._length = 0;

    # �������һ��������������е�Ԫ��
    def _next(self):
        """
        :return: every_data: �����еĽڵ�
        """
        every_data = self._getItem(self._index_next);
        self._index_next += 1;
        return every_data;

    #  ʹ�� len(ChainTable) ʱ��������ĳ���
    def __len__(self):
        return self._length;

    # ���ݶ������Ԫ��
    def __repr__(self):
        """
        :return:None
        """
        if self._isEmpty():
            print("����Ϊ�գ�����");
            return;
        result = "";
        j = 0; # ������λ
        while j < self._length:
            result += str(self._getItem(j)) + " ";
            j += 1;
        return result;

