import logging
from tkinter.messagebox import NO

class Node(object):
    """
    节点类
    """

    def __init__(self, data=None, lchild=None, rchild=None, parent=None):
        """
        :param data: 数据
        :param lchild: 左节点
        :param rchild: 右节点
        """
        self.data = data
        self.lchild = lchild
        self.rchild = rchild
        self.parent = parent

    def __str__(self):
        return str((self.data))

    def __eq__(self, other):
        if isinstance(other, Node):
            if self.data == other.data or set(self.data) == set(other.data):
                return True
            else:
                return False
        else:
            if self.data == other or set(self.data) == set(other):
                return True
            else:
                return False
class LeafNode(Node):
    def __init__(self, data=None, lchild=None, rchild=None, parent=None):
        """
        :param data: 数据
        :param lchild: 左节点
        :param rchild: 右节点
        """
        super().__init__(data, lchild, rchild, parent)
    
    def is_leaf(self):
        return True

class Hierarchy_tree(object):
    """
    二叉树
    """

    def __init__(self):
        self.root = None
        self.isolated_node = []
        self.leaf_node = []

    def HT_init_leafnode(self, node_list):
        for data in node_list:
            self.add_leaf_node([data])

    def add_leaf_node(self, data):
        """
        添加叶节点
        :param data: 节点数据
        :return:
        """
        node = LeafNode(data)
        self.isolated_node.append(node)
        self.leaf_node.append(node)
    
    def merge_node(self,data,lchild,rchild):
        """  to merge A and B, the F(A,B) is the max. 
            data and lchild and rchild is int or tuple, 
            the leafnode is int ,the innode is tuple.
    
        """
        if len(self.isolated_node)<=1:
            assert("Please make sure this is need to merge")
        else:
            leafnode_id = None
            rightnode_id = None
            for node_id in range(len(self.isolated_node)):
                if self.isolated_node[node_id] == lchild:
                    leafnode_id = node_id
                if self.isolated_node[node_id] == rchild:
                    rightnode_id = node_id
            if leafnode_id == None or rightnode_id == None:
                assert("Error the leafnode_id or rightnode_id is None,\n \
                        You should make sure your input data,lchild,rchild is true,\n \
                        You can come to the Fast_man/merge_node to see it")
                    
            leaf_node = self.isolated_node[(leafnode_id)]
            right_node = self.isolated_node[(rightnode_id)]
            
            self.isolated_node.remove(leaf_node)
            self.isolated_node.remove(right_node)
            parentnode = Node(data)
            parentnode.lchild = leaf_node
            leaf_node.parent = parentnode
            parentnode.rchild = right_node
            right_node.parent = parentnode

            self.isolated_node.append(parentnode)
            # print("len(self.isolated_node)",len(self.isolated_node))
            if len(self.isolated_node)==1:
                self.root = parentnode
                # print("the last merge")
                logging.info("the last merge")

 
    def preorder(self, root):
        """
        深度遍历 递归实现先序遍历
        """
        if not root:
            return
        print(root.data)
        self.preorder(root.lchild)
        self.preorder(root.rchild)
 
    def inorder(self, root):
        """
        深度遍历 递归实现中序遍历
        """
        if not root:
            return
        self.inorder(root.lchild)
        print(root.data)
        self.inorder(root.rchild)
 
    def postorder(self, root):
        """
        深度遍历 递归实现后续遍历
        """
        if not root:
            return
        self.postorder(root.lchild)
        self.postorder(root.rchild)
        print(root.data)
 
    def breadth_travel(self, root):
        """
        广度遍历 利用队列实现树的层次遍历
        """
        if not root:
            return
        queue = []
        queue.append(root)
        while queue:
            node = queue.pop(0)
            print(node.data)
            if node.lchild:
                queue.append(node.lchild)
            if node.rchild:
                queue.append(node.rchild)
 