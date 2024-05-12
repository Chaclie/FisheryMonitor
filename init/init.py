import csv  # 导入csv文件
import py2neo  # 导入py2neo库
import json # 导入json文件库
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher

graph = Graph("bolt: // localhost:7687", auth=("neo4j", "12345678"))
matcher = NodeMatcher(graph)
matcher2 = RelationshipMatcher(graph)
path = ''

# 初始化函数，清空数据库，然后导入数据
def init():
    graph.run('match(n) detach delete n')
    # 读入csv，插入药材节点
    f = open(path+'药材.csv', encoding='utf-8')
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        name = row[1]
        alias = row[2]
        english_name = row[3]
        picture = row[8]
        node = Node('药材', name=name, alias=alias, english_name=english_name, picture=picture)
        graph.create(node)

    # 读入csv，插入方剂节点
    f = open(path+'方剂.csv', encoding='utf-8')
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        name = row[1]
        usage = row[3]
        node = Node('方剂', name=name, usage=usage)
        graph.create(node)

    # 读入csv，插入中成药节点
    f = open(path+'中成药.csv', encoding='utf-8')
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        name = row[1]
        usage = row[4]
        picture = row[5]
        node = Node('中成药', name=name, usage=usage, picture=picture)
        graph.create(node)

    # 插入药性节点
    node = Node('药性', name='热性')
    graph.create(node)
    node = Node('药性', name='温性')
    graph.create(node)
    node = Node('药性', name='寒性')
    graph.create(node)
    node = Node('药性', name='凉性')
    graph.create(node)
    node = Node('药性', name='平性')
    graph.create(node)

    # 插入药味节点
    node = Node('药味', name='甘味')
    graph.create(node)
    node = Node('药味', name='苦味')
    graph.create(node)
    node = Node('药味', name='辛味')
    graph.create(node)
    node = Node('药味', name='酸味')
    graph.create(node)
    node = Node('药味', name='咸味')
    graph.create(node)
    node = Node('药味', name='涩味')
    graph.create(node)
    node = Node('药味', name='淡味')
    graph.create(node)

    # 读取csv，建立药材和药性药味的关系
    f = open(path+'性味归经.csv', encoding='utf-8')
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        node1 = matcher.match('药材', name=row[0]).first()
        node2 = matcher.match('药性', name=row[1]).first()
        node3 = matcher.match('药味', name=row[2]).first()
        relationship1 = Relationship(node1, '药性属于', node2)
        relationship2 = Relationship(node1, '药味属于', node3)
        graph.create(relationship1)
        graph.create(relationship2)

    # 插入省份节点
    province_list = ['北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江',
                     '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川',
                     '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆', '台湾', '香港', '澳门']
    for province in province_list:
        node = Node('省份', name=province)
        graph.create(node)

    # 读取csv，建立药材和产地的关系
    f = open(path+'产地.csv', encoding='utf-8')
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        node1 = matcher.match('药材', name=row[0]).first()
        provinces = row[1]
        province_list = eval(provinces)
        if len(province_list)>0:
            for province in province_list:
                node2 = matcher.match('省份', name=province).first()
                relationship = Relationship(node1, '产于', node2)
                graph.create(relationship)

    # 读取csv，建立方剂和药材的关系
    f = open(path+'方剂组成成分.csv', encoding='utf-8')
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        node1 = matcher.match('方剂', name=row[0]).first()
        compositions= row[1]
        composition_list = eval(compositions)
        if len(composition_list) > 0:
            for composition in composition_list:
                node2 = matcher.match('药材', name=composition).first()
                if node2 is not None:
                    relationship = Relationship(node1, '方剂成分', node2)
                    graph.create(relationship)

    # 读取csv，建立中成药和药材的关系
    f = open(path+'中成药组成成分.csv', encoding='utf-8')
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        node1 = matcher.match('中成药', name=row[0]).first()
        compositions = row[1]
        composition_list = eval(compositions)
        if len(composition_list) > 0:
            for composition in composition_list:
                node2 = matcher.match('药材', name=composition).first()
                if node2 is not None:
                    relationship = Relationship(node1, '中成药成分', node2)
                    graph.create(relationship)

    # 插入功效节点并构建关系
    function_list = ['消散', '通便', '暖官', '和血', '通络', '止漏', '降气', '行气', '清肺', '渗湿', '镇心', '温润', '暖肝', '固肾',
                     '止咳', '化气', '滋肾', '疏散', '逐湿', '调补', '疏风', '接骨', '散结', '和胃', '平肝', '调血', '潜阳', '祛风',
                     '清宣', '辟秽', '气血', '肺胃', '止惊', '安冲', '泻火', '宣化', '回阳', '滋阴', '止呕', '止疼', '清燥', '解毒',
                     '通淋', '驱虫', '发表', '肺化', '固肠', '通水', '止痢', '益气', '定志', '镇痛', '利湿', '行瘀', '发散', '溃脓',
                     '营卫', '辛凉', '提脓', '滑肠', '利胆', '清营', '补益', '水道', '调经', '除烦', '补心', '轻宣', '扶阳', '拔毒',
                     '补虚', '气机', '和中', '软坚', '温中', '壮阳', '清里', '补肾', '滋养', '分利', '破结', '利咽', '消肿', '益肺',
                     '清火', '补气', '清热', '通里', '摄血', '解肌', '熄风', '下胎', '降压', '化饮', '安胎', '解郁', '热结', '收敛',
                     '行水', '泻下', '解表', '补脾', '化浊', '止痛', '调和', '通乳', '润肺', '柔肝', '凉血', '祛暑', '燥湿', '缓急',
                     '湿热', '敛疮', '排石', '明目', '防腐', '生律', '养心', '去腐', '养血', '敛阴', '除蒸', '宣导', '泻肺', '息风',
                     '镇静', '安神', '利音', '止痉', '泻脾', '排脓', '发汗', '托毒', '祛痒', '补阳', '固经', '解痉', '和营', '消炎',
                     '消积', '退黄', '凉肝', '消痢', '泻热', '消痰', '胜湿', '定喘', '养阴', '止泻', '涌吐痰食', '宣湿', '补中', '固涩',
                     '托里', '通腑', '消癥', '快气', '驱蛔', '调气', '涩精', '利水', '补肺', '调解', '破坚', '清湿', '举陷', '温化',
                     '镇肝', '透达', '止汗', '破瘀', '开音', '固表', '温养', '辛温', '中气', '增液', '止血', '祛寒', '缩尿', '定痛',
                     '安蛔', '下气', '固精', '消痛', '健胃', '散水', '肃肺', '杀虫', '透表', '活络', '固脱', '攻下', '止痒', '通窍',
                     '涩肠', '逐瘀', '助阳', '健脾', '醒神', '散寒', '化湿', '逐寒', '止渴', '寒饮', '养胃', '截疟', '温肺', '益精',
                     '通阳', '除满', '驱杀', '逐水', '消痈', '化痰', '镇痉', '宁心', '聪耳', '透脓', '寒湿', '舒筋', '和阳', '行痹',
                     '止遗', '化瘀', '清胃', '温脾', '收涩', '益胃', '温阳', '止带', '清肠', '散瘀', '敛肺', '救逆', '驱除', '下乳',
                     '和解', '化腐', '清肝', '除痰', '复脉', '疏表', '生津', '活血', '涌吐', '化阳', '理气', '镇惊', '温逐', '退肿',
                     '祛腐', '化滞', '湿邪', '消食', '平喘', '祛瘀', '少阳', '降逆', '宽胸', '升阳', '祛痰', '益肾', '润燥', '温肾',
                     '通关', '清化', '祛脓', '定惊', '除脓', '心肾', '温补', '表散', '生肌', '绦虫','通经', '开窍', '除湿', '补血',
                     '降浊', '透热', '饮清', '攻毒', '降火', '化痞', '坚阴', '热解', '清心', '温经', '宣肺', '通利', '疏肝', '破血',
                     '祛湿', '涤痰', '散邪', '封髓', '消暑', '利尿']

    for function in function_list:
        # 插入功效节点
        node2 = Node('功效', name=function)
        graph.create(node2)

        # 读取csv，建立药材和功效之间的关系
        f = open(path + '药材.csv', encoding='utf-8')
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            functions = row[6]
            if function in functions:
                node1 = matcher.match('药材', name=row[1]).first()
                relationship = Relationship(node1, '药材具有', node2)
                graph.create(relationship)

        # 读取csv，建立方剂和功效之间的关系
        f = open(path + '方剂.csv', encoding='utf-8')
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            functions = row[4]
            if function in functions:
                node1 = matcher.match('方剂', name=row[1]).first()
                relationship = Relationship(node1, '方剂具有', node2)
                graph.create(relationship)

        # 读取csv，建立中成药和功效之间的关系
        f = open(path + '中成药.csv', encoding='utf-8')
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            functions = row[3]
            if function in functions:
                node1 = matcher.match('中成药', name=row[1]).first()
                relationship = Relationship(node1, '中成药具有', node2)
                graph.create(relationship)

    # 读取csv，插入主治节点并构建关系
    f = open(path + '主治.csv', encoding='utf-8')
    reader = csv.reader(f)
    row = next(reader)
    attending_list = row[0]
    attending_list = eval(attending_list)

    for attending in attending_list:
        # 插入功效节点
        node2 = Node('主治', name=attending)
        graph.create(node2)

        # 读取csv，建立药材和主治之间的关系
        f = open(path + '药材.csv', encoding='utf-8')
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            attendings = row[7]
            if attending in attendings:
                node1 = matcher.match('药材', name=row[1]).first()
                relationship = Relationship(node1, '药材主治', node2)
                graph.create(relationship)

        # 读取csv，建立方剂和功效之间的关系
        f = open(path + '方剂.csv', encoding='utf-8')
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            attendings = row[5]
            if attending in attendings:
                node1 = matcher.match('方剂', name=row[1]).first()
                relationship = Relationship(node1, '方剂主治', node2)
                graph.create(relationship)

        # 读取csv，建立方剂和功效之间的关系
        f = open(path + '中成药.csv', encoding='utf-8')
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            attendings = row[3]
            if attending in attendings:
                node1 = matcher.match('中成药', name=row[1]).first()
                relationship = Relationship(node1, '中成药主治', node2)
                graph.create(relationship)



# 生成节点的JSON数据文件
def generate_node_json():
    nodes = graph.run("MATCH (n) RETURN n").data()
    node_data = []
    for node in nodes:
        node_data.append(node["n"])
        print(node["n"])
    with open("nodes.json", "w",encoding="utf-8") as f:
        json.dump(node_data, f, ensure_ascii=False)


# 生成关系的JSON数据文件
def generate_relationship_json():
    relationships = graph.run('MATCH ()-[r]->() RETURN r').data()
    relationship_data = []
    for relationship in relationships:
        rel = relationship['r']
        start_node_id = rel.start_node['name']
        if start_node_id is None:
            break
        end_node_id = rel.end_node['name']
        rel_data = {
            'start_node': start_node_id,
            'end_node': end_node_id,
            'type': list(rel.types())[0],
        }
        relationship_data.append(rel_data)
        print(rel_data)
    with open("relationships.json", "w", encoding="utf-8") as f:
        json.dump(relationship_data, f, ensure_ascii=False)


# 生成节点和关系的JSON数据文件
def generate_json_files():
    generate_node_json()
    generate_relationship_json()

# init()
generate_relationship_json()
