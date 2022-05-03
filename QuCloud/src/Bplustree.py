## 使用须知：1. 查找必须得是范围查询，点查询也得是上下界相等才行；查找的返回值一定是一个由KV组成的数组，哪怕点查询
## 2. 删除必须得输入键-值对而不是只靠键，当然如果和查询配合使用还是挺好的；
## 3. 这个算法不会拒绝同一个键多次插入，哪怕值也是相同的也不会报错，照样按从左到右插入
## 4. 注意B+树叶节点不是一个个键值，而是多个键值组成的节点，节点之间才有指向邻居的指针

from collections import deque

def bisect_right(a, x, lo=0, hi=None):
    """Return the index where to insert item x in list a, assuming a is sorted.
    The return value i is such that all e in a[:i] have e <= x, and all e in
    a[i:] have e > x.  So if x already appears in the list, a.insert(x) will
    insert just after the rightmost x already there.
    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if x < a[mid]:
            hi = mid
        else:
            lo = mid + 1
    return lo

def bisect_left(a, x, lo=0, hi=None):
    """Return the index where to insert item x in list a, assuming a is sorted.
    The return value i is such that all e in a[:i] have e < x, and all e in
    a[i:] have e >= x.  So if x already appears in the list, a.insert(x) will
    insert just before the leftmost x already there.
    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo

class InitError(Exception):
    pass

class ParaError(Exception):
    pass


class KeyValue(object):
    __slots__ = ('key', 'value')

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return str((self.key, self.value))

    def __eq__(self, other):
        if isinstance(other, KeyValue):
            if self.key == other.key:
                return True
            else:
                return False
        else:
            if self.key == other:
                return True
            else:
                return False

    def __ne__(self, other):
        if isinstance(other, KeyValue):
            if self.key != other.key:
                return True
            else:
                return False
        else:
            if self.key != other:
                return True
            else:
                return False

    def __lt__(self, other):
        if isinstance(other, KeyValue):
            if self.key < other.key:
                return True
            else:
                return False
        else:
            if self.key < other:
                return True
            else:
                return False

    def __gt__(self, other):
        if isinstance(other, KeyValue):
            if self.key > other.key:
                return True
            else:
                return False
        else:
            if self.key > other:
                return True
            else:
                return False


class Bptree_InterNode(object): # 内部节点
    def __init__(self, M):
        if not isinstance(M, int):
            raise InitError('M must be int')
        if M <= 3:
            raise InitError('M must be greater then 3')
        else:
            self.__M = M
            self.clist = []  # 如果是index节点，保存 Bptree_InterNode 节点信息
            #      leaf节点， 保存 Bptree_Leaf的信息
            self.ilist = []  # 保存 索引节点
            self.par = None

    def isleaf(self):
        return False

    def isfull(self):   # 已装满 最多k-1
        return len(self.ilist) >= self.M - 1

    def isempty(self):  # 未装满 至少Math.ceil(m/2)-1
        return len(self.ilist) < (self.M + 1) // 2 - 1

    @property
    def M(self):
        return self.__M


class Bptree_Leaf(object):  # 叶节点
    def __init__(self, L):
        if not isinstance(L, int):
            raise InitError('L must be int')
        else:
            self.__L = L
            self.vlist = []
            self.bro = None
            self.par = None

    def isleaf(self):
        return True

    def isfull(self):   # 当大于填充因子，则已满
        return len(self.vlist) >= self.L

    def isempty(self):
        return len(self.vlist) < (self.L + 1) // 2 - 1  # 删除的填充因子

    @property
    def L(self):
        return self.__L


class Bptree(object):
    def __init__(self, M, L):  # M为度， L为填充因子
        if L > M:
            raise InitError('L must be less or equal then M')
        else:
            self.__M = M    # 度
            self.__L = L    # 填充因子
            self.__Size = 0
            self.__root = Bptree_Leaf(L)
            self.__leaf = self.__root

    @property
    def M(self):
        return self.__M

    @property
    def L(self):
        return self.__L

    @property
    def Size(self):
        return self.__Size


    def insert(self, key_value):
        node = self.__root

        def split_node(n1):
            mid = self.M // 2
            newnode = Bptree_InterNode(self.M)
            newnode.ilist = n1.ilist[mid:]
            newnode.clist = n1.clist[mid:]
            newnode.par = n1.par

            for c in newnode.clist:
                c.par = newnode

            if n1.par is None:
                newroot = Bptree_InterNode(self.M)
                newroot.ilist = [n1.ilist[mid - 1]]
                newroot.clist = [n1, newnode]
                n1.par = newnode.par = newroot
                self.__root = newroot
            else:
                i = n1.par.clist.index(n1)
                n1.par.ilist.insert(i, n1.ilist[mid - 1])
                n1.par.clist.insert(i + 1, newnode)

            n1.ilist = n1.ilist[:mid - 1]
            n1.clist = n1.clist[:mid]
            return n1.par

        def split_leaf(n2):
            mid = (self.L + 1) // 2 - 1
            newleaf = Bptree_Leaf(self.L)
            newleaf.vlist = n2.vlist[mid:]
            if n2.par == None:
                newroot = Bptree_InterNode(self.M)
                newroot.ilist = [n2.vlist[mid].key]
                newroot.clist = [n2, newleaf]
                n2.par = newleaf.par = newroot
                self.__root = newroot
            else:
                i = n2.par.clist.index(n2)
                n2.par.ilist.insert(i, n2.vlist[mid].key)
                n2.par.clist.insert(i + 1, newleaf)
                newleaf.par = n2.par

            n2.vlist = n2.vlist[:mid]
            #if n2 have bro :n2->newleaf->n2.bro,if not : n2->n2.bro
            if n2.bro ==None:
                n2.bro = newleaf
            else:
                newleaf.bro = n2.bro
                n2.bro = newleaf

        def insert_node(n):
            if not n.isleaf():
                if n.isfull():
                    insert_node(split_node(n))
                else:
                    p = bisect_right(n.ilist, key_value)
                    insert_node(n.clist[p])
            else:
                p = bisect_right(n.vlist, key_value)    # 确定插入位置
                # print("n.vlist,p, key_value", n.vlist,p, key_value)   # Debug the insert point in leaf
                n.vlist.insert(p, key_value)

                self.__Size += 1
                if n.isfull():
                    split_leaf(n)   # 叶节点分裂
                else:
                    return

        insert_node(node)

    def search(self, mi=None, ma=None):
        result = []
        node = self.__root
        leaf = self.__leaf
        if mi is None and ma is None:
            raise ParaError('you need to setup searching range')
        elif mi is not None and ma is not None and mi > ma:
            raise ParaError('upper bound must be greater or equal than lower bound')

        def search_key(n, k):
            if n.isleaf():
                p = bisect_left(n.vlist, k)
                return (p, n)
            else:
                p = bisect_right(n.ilist, k)
                return search_key(n.clist[p], k)

        if mi is None:
            while True:
                for kv in leaf.vlist:
                    if kv < ma or kv==ma:
                        result.append(kv)
                    else:
                        return result
                if leaf.bro == None:
                    return result
                else:
                    leaf = leaf.bro
        elif ma is None:
            index, leaf = search_key(node, mi)
            result.extend(leaf.vlist[index:])
            while True:
                if leaf.bro == None:
                    return result
                else:
                    leaf = leaf.bro
                    result.extend(leaf.vlist)
        else:
            if mi == ma:
                i, l = search_key(node, mi)
                try:
                    if l.vlist[i] == mi:
                        result.append(l.vlist[i])
                        return result
                    else:
                        return result
                except IndexError:
                    return result
            else:
                # min leaf (l1) and vlist id (i1), l1[i1] == key_value(mi)
                # max leaf (l2) and vlist id (i2), l2[i2] == key_value(ma) 
                i1, l1 = search_key(node, mi)
                i2, l2 = search_key(node, ma)
                if l1 is l2:
                    if i1 == i2:
                        return result
                    else:
                        if l2.vlist[i2] == ma:
                        ## 解决了上界ma不存在于B+树中时出错的问题
                            result.extend(l1.vlist[i1:i2 + 1])
                            return result
                        else:
                            result.extend(l1.vlist[i1:i2])

                else:
                    result.extend(l1.vlist[i1:])
                    l = l1
                    while True:
                        if l.bro == l2:
                            if l2.vlist[i2] == ma:
                                result.extend(l2.vlist[:i2 + 1])
                                return result
                            else:
                                result.extend(l2.vlist[:i2])
                                return result
                        else:
                            result.extend(l.bro.vlist)
                            l = l.bro

    def traversal(self):
        result = []
        l = self.__leaf
        while True:
            result.extend(l.vlist)
            if l.bro == None:
                return result
            else:
                l = l.bro

    def show(self):
        print
        'this b+tree is:\n'
        q = deque()
        h = 0
        q.append([self.__root, h])
        while True:
            try:
                w, hei = q.popleft()
            except IndexError:
                return
            else:
                if not w.isleaf():
                    print(w.ilist, 'the height is', hei)
                    if hei == h:
                        h += 1
                    q.extend([[i, h] for i in w.clist])
                else:
                    print([v.key
                    for v in w.vlist], 'the leaf is,', hei)

    def delete(self, key_value):
        def merge(n, i):
            if n.clist[i].isleaf():
                n.clist[i].vlist = n.clist[i].vlist + n.clist[i + 1].vlist
                n.clist[i].bro = n.clist[i + 1].bro
            else:
                n.clist[i].ilist = n.clist[i].ilist + [n.ilist[i]] + n.clist[i + 1].ilist
                n.clist[i].clist = n.clist[i].clist + n.clist[i + 1].clist
            n.clist.remove(n.clist[i + 1])
            n.ilist.remove(n.ilist[i])
            if n.ilist == []:
                n.clist[0].par = None
                self.__root = n.clist[0]
                del n
                return self.__root
            else:
                return n

        def tran_l2r(n, i):
            if not n.clist[i].isleaf():
                # 将i的最后一个节点追加到i+1的第一个节点
                n.clist[i + 1].clist.insert(0, n.clist[i].clist[-1])
                n.clist[i].clist[-1].par = n.clist[i + 1]

                # 追加 i+1的索引值，以及更新n的i+1索引值
                ## n.clist[i + 1].ilist.insert(0, n.clist[i].ilist[-1])
                ## n.ilist[i + 1] = n.clist[i].ilist[-1]
                ## n.clist[i].clist.pop()
                ## n.clist[i].ilist.pop()

                # edit:
                n.clist[i + 1].ilist.insert(0, n.ilist[i])
                n.ilist[i] = n.clist[i].ilist[-1]
                n.clist[i].clist.pop()
                n.clist[i].ilist.pop()

            else:
                n.clist[i + 1].vlist.insert(0, n.clist[i].vlist[-1])
                n.clist[i].vlist.pop()
                n.ilist[i] = n.clist[i + 1].vlist[0].key

        def tran_r2l(n, i):
            if not n.clist[i].isleaf():
                n.clist[i].clist.append(n.clist[i + 1].clist[0])
                n.clist[i + 1].clist[0].par = n.clist[i]

                n.clist[i].ilist.append(n.ilist[i])
                n.ilist[i] = n.clist[i + 1].ilist[0]
                n.clist[i + 1].clist.remove(n.clist[i + 1].clist[0])
                n.clist[i + 1].ilist.remove(n.clist[i + 1].ilist[0])

            else:
                n.clist[i].vlist.append(n.clist[i + 1].vlist[0])
                n.clist[i + 1].vlist.remove(n.clist[i + 1].vlist[0])
                n.ilist[i] = n.clist[i + 1].vlist[0].key

        def del_node(n, kv):
            if not n.isleaf():
                p = bisect_right(n.ilist, kv)
                if p == len(n.ilist):
                    if not n.clist[p].isempty():
                        return del_node(n.clist[p], kv)
                    elif not n.clist[p - 1].isempty():
                        tran_l2r(n, p - 1)
                        return del_node(n.clist[p], kv)
                    else:
                        return del_node(merge(n, p - 1), kv)
                else:
                    if not n.clist[p].isempty():
                        return del_node(n.clist[p], kv)
                    elif not n.clist[p + 1].isempty():
                        tran_r2l(n, p)
                        return del_node(n.clist[p], kv)
                    else:
                        return del_node(merge(n, p), kv)
            else:
                p = bisect_left(n.vlist, kv)
                try:
                    pp = n.vlist[p]
                except IndexError:
                    return -1
                else:
                    if pp != kv:
                        return -1
                    else:
                        n.vlist.remove(kv)
                        self.__Size -= 1
                        return 0

        del_node(self.__root, key_value)

    @property
    def leaf(self):
        return self.__leaf

def test():
    B = Bptree(4,4)
    n = 10
    print("---检查插入算法---")
    for i in range(n):
        B.insert(KeyValue(1 + i, i**2))
    B.insert(KeyValue(0, -1))
    print("-----------查看全部可选比特数: -------------")
    print("size: ", B.Size)
    print("-----------选择查看比特数为3-6的可选:-----------")
    for i in B.search(3,10):
        print("选择得到的键值对:",i)
    print("------展示所有的树结构-----------")
    B.show()


if __name__ == '__main__':
    test()
