#-*- coding:utf-8 –*-

# 创建关系矩阵
def create_relation_matrix(List, n):
    adjacent_matrix = create_matrix(n, 0)
    for relation in List:
        adjacent_matrix[relation[0]][relation[1]] = 1
        adjacent_matrix[relation[1]][relation[0]] = 1
    return adjacent_matrix
# 输出列表
def printf(List):
    for x in List:
        print (x)
# 列表去重
def list_unique(List):
    new_list = []
    for id in List:
        if id not in new_list:
            new_list.append(id)
    return new_list
# 创建矩阵，number为矩阵一维个数，amount为填充数字
def create_matrix(number, amount):
    matrix = []
    for i in range(0, number):
        tmp = []
        for j in range(0, number):
            tmp.append(amount)
        matrix.append(tmp)
    return matrix
# 查找包含该元素的所有位置
def find_index(List, node):
    return [i for i, j in enumerate(List) if j == node]

# 获取模块度
def get_modularity(node_list, node_club, club_list, node_matrix):
    uni = list_unique(club_list)
    # 更新社团位置
    for node in uni:                            #node 相当于label社团标签
        idices = find_index(club_list, node)    #找到标签在club_list中的位置
        for i in idices:                        #遍历所有label的位置
            node_club[i] = uni.index(node)      #node在标签中的位置,并将node_club中club_list所在的位置设为当前uni.index所在的位置，表示交换后的club_list
    Q = 0
    m = sum([sum(node) for node in node_matrix])/2  # 网络的边的数目
    k = len(list_unique(node_club))  # 当前社团数目
    e = create_matrix(k, 0)  # 构造0矩阵
    for i in range(k):
        idx = find_index(node_club, i)          #找到每个社团对应的索引 
        labelsi = idx
        for j in range(k):
            idx = find_index(node_club, j)
            labelsj = idx
            for ii in labelsi:
                for jj in labelsj:
                    e[i][j] = e[i][j]+node_matrix[ii][jj]  # e[i][j]代表i社团与j社团之间有多少连接，得到一个社团连接矩阵
    e = [[float(j)/(2*m) for j in i] for i in e] #将全部数除2*m
    a = []
    for i in range(k):
        ai = sum(e[i])
        a.append(ai) #得到每一行之和，即每个社团与其他社团已经自己社团的连线之和
        Q = Q + e[i][i]-ai**2  #对角迹之和减去ai的平方
    return Q, e, a, node_club  #返回Q和e列表，a列表，当前的节点标签
def fast_newman(node_list, List,n,divide_num):
    adjacent_matrix=create_relation_matrix(List, n)
    n = len(adjacent_matrix)
    max_id = n
    Z = []
    # 初始划分，node_list是节点标号，node_club是社团标号的变换，club_list是社团标号
    node_club = [0 for i in range(n)]
    club_list = [i for i in range(n)]
    step = 1
    while len(list_unique(club_list)) != 1:  # 计算满足条件的个数
        Q, e, a, node_club = get_modularity(node_list, node_club, club_list, adjacent_matrix)
        k = len(e)  # 社团数目
        DeltaQs = []
        DeltaQs_i = []
        DeltaQs_j = []
        for i in range(k):
            for j in range(k):
                if i != j:
                    DeltaQ = 2*(e[i][j]-a[i]*a[j])  #第i和第j进行合并成社团的Q值，乘而由于只算一遍，但之前是除了2，相当于是变化的Q
                    DeltaQs.append(DeltaQ)
                    DeltaQs_i.append(i)  #第i社团
                    DeltaQs_j.append(j)  #第j社团
        maxDeltaQ = max(DeltaQs)  # 选择最大Q值的社团进行合并
        id_club = DeltaQs.index(maxDeltaQ) #找到最大deltaq的位置
        i = DeltaQs_i[id_club]   #找出第一个社团
        j = DeltaQs_j[id_club]   #找出第二个社团
        max_id = max_id + 1      #得出新的最大的id标号
        c_id1 = find_index(node_club, i)  # 获取社团i的标号
        c_id2 = find_index(node_club, j)  # 获取社团j的标号
        id1 = list_unique([club_list[item] for item in c_id1])  # 找到社团i的所有节点
        id2 = list_unique([club_list[item] for item in c_id2])  # 找到社团j的所有节点
        for item in c_id1:
            club_list[item] = max_id #将社团i的标号全部改为新的标签号

        for item in c_id2:
            club_list[item] = max_id #将社团j的标号全部改为新的标签号
        Z.append([id1, id2, len(c_id1+c_id2)]) #修改的所有的节点以及修改的数量
        step = step + 1  #步数+1
        result_name = []
        result_index = []
        for item in list_unique(club_list):  #遍历所有的标签
            tmp = find_index(club_list, item) #找到标签的位置，也是节点的索引号
            result_name.append([node_list[t] for t in tmp]) #找到标签对应的节点的名称
            result_index.append(tmp) #节点号索引进行添加
        if len(result_name) <= divide_num: #划分次数
            break
    club_link=[]
    for item in List:
        if club_list[item[0]]!=club_list[item[1]]:  #如果两个节点的标签不相同，则添加进去
            club_link.append(item)

    return result_name,result_index,club_link
if __name__ == '__main__':
    List = [[0, 1], [1, 2], [1, 3], [3, 4], [3, 5], [3, 6], [4, 5], [1, 5]]
    node_list = ["node0", "node1", "node2", "node3", "node4", "node5", "node6"]
    for i in range(7):
        print (fast_newman(node_list, List, 7, i+1))