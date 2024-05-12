# neo4j查询语句
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
import re
from functools import reduce
from question_classifier import *

hrep_select_dict = {
    'kind': {
        '0': '中药',
        '1': '中成药',
        '2': '方剂'
    },
    'hrep_type': {
        '0': '任意',
        '1': '热性',
        '2': '温性',
        '3': '寒性',
        '4': '凉性',
        '5': '平性'
    },
    'hrep_feel': {
        '0': '任意',
        '1': '甘味',
        '2': '苦味',
        '3': '辛味',
        '4': '酸味',
        '5': '咸味',
        '6': '涩味',
        '7': '淡味'
    },
    'hrep_place': {
        '0': '任意',
        '1': '安徽',
        '2': '澳门',
        '3': '北京',
        '4': '重庆',
        '5': '福建',
        '6': '甘肃',
        '7': '广东',
        '8': '广西',
        '9': '贵州',
        '10': '海南',
        '11': '河北',
        '12': '河南',
        '13': '黑龙江',
        '14': '湖北',
        '15': '湖南',
        '16': '吉林',
        '17': '江苏',
        '18': '江西',
        '19': '辽宁',
        '20': '内蒙古',
        '21': '宁夏',
        '22': '青海',
        '23': '山东',
        '24': '山西',
        '25': '陕西',
        '26': '上海',
        '27': '四川',
        '28': '台湾',
        '29': '天津',
        '30': '西藏',
        '31': '香港',
        '32': '新疆',
        '33': '云南',
        '34': '浙江'
    }
}


def select_by_name(sel_name, label):
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))
    query = "MATCH (n:{label}) WHERE n.name = $name RETURN n".format(label=label)
    result = graph.run(query, name=sel_name).data()
    node = None
    result_dict = None 
    if(len(result)!=0):
        node = result[0]  # Check if there is a result before accessing the data
        result_dict = node_to_dict(node['n'],label)
    
    return result_dict


def select_by_name2(sel_name,label):
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))
    matcher=NodeMatcher(graph)
    
    node = matcher.match(name=sel_name).first()
    result_dict = None
    if(node != None):
        result_dict = node_to_dict(node,label)
    
    return result_dict


def node_to_dict(node,resType):
    if(resType=='药材'):
        result={
        'category': 0,
        'alias': node['alias'],
        'attending':node['attending'],
        'english_name': node['english_name'],
        'feature': node['feature'],
        'form': node['form'],
        'function': node['function'],
        'name': node['name'],
        'picture': node['picture'],
        'place': node['place'],
        'warning': node['warning']
        }
        return result
    elif (resType=='中成药'):
        result={
        'category': 1,
        'composition': node['composition'],
        'attending':node['attending'],
        'picture': node['picture'],
        'usage': node['usage'],
        'name': node['name'],
        }
        return result
    elif (resType=='方剂'):
        result={
        'category': 2,
        'composition': node['composition'],
        'attending':node['attending'],
        'function': node['function'],
        'usage': node['usage'],
        'name': node['name'],
        }
        return result
    

def select_relation_by_name(sel_name):
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))
    query = "MATCH ()-[r:`" + sel_name + "`]-() RETURN r"
    result = graph.run(query)
    relationships = None
    if(result != None):
        relationships = result.data()  # 获取查询结果列表
    print(relationships)
    print(type(relationships))
    return relationships


def select_by_label2(sel_label):
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))
    query = "MATCH (n:" + sel_label + ") RETURN n LIMIT 5"
    result = graph.run(query)
    nodes = result.data()  # 获取查询结果列表
    print(nodes)
    names = [node['n'].get('name') for node in nodes]  # 获取节点的name属性值
    return names


def herb_select_by_info(feature, flavour, province):
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))
    # 构建Cypher查询语句
    featurestr=hrep_select_dict['hrep_type'][feature]
    flavourstr=hrep_select_dict['hrep_feel'][flavour]
    provincestr=hrep_select_dict['hrep_place'][province]
    
    cypher_query = ""

    if featurestr != '任意':
        cypher_query1 = f"(n:药材)-[:药性属于]->(p:药性 {{name: '{featurestr}'}})"
    else:
        cypher_query1 = ''
    if flavourstr != '任意':
        cypher_query2 = f"(n:药材)-[:药味属于]->(q:药味 {{name: '{flavourstr}'}})"
    else:
        cypher_query2 = ''
    if provincestr != '任意':
        cypher_query3 = f"(n:药材)-[:产于]->(o:省份 {{name: '{provincestr}'}})"
    else:
        cypher_query3 = ''

    cypher_query += cypher_query1

    if len(cypher_query2) > 0:
        if len(cypher_query) > 0:
            cypher_query += ',' + cypher_query2
        else:
            cypher_query += cypher_query2

    if len(cypher_query3) > 0:
        if len(cypher_query) > 0:
            cypher_query += ',' + cypher_query3
        else:
            cypher_query += cypher_query3
            
    if cypher_query == '':
        cypher_query = '(n:药材)'

    cypher_query = "MATCH " + cypher_query + " RETURN n"
    # 执行查询
    results = graph.run(cypher_query).data()
    node = None
    result_dict = []
    if(len(results)!=0):
        for result in results:
            node = result  # Check if there is a result before accessing the data
            result_dict.append(node_to_dict(node['n'],'药材'))
            
    return result_dict

def smart_consultation(consultation):
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))
    handler = QuestionClassifier()
    attending_data = handler.classify(consultation)
    attendings = attending_data.get('args').keys()
    result_dict = []
    if len(attendings) > 4:
        con_length = 2
    else:
        con_length = 4
    for data in attendings:
        query1 = "MATCH (n:方剂)-[r:方剂主治]-(b:症状) where b.name CONTAINS '{}' return n LIMIT {}".format(data, con_length)
        query2 = "MATCH (n:中成药)-[r:中成药主治]-(b:症状) where b.name CONTAINS '{}' return n LIMIT {}".format(data, con_length)
        result1 = graph.run(query1).data()
        result2 = graph.run(query2).data()
        if(len(result1)!=0):
            for result in result1:
                node = result  # Check if there is a result before accessing the data
                result_dict.append(node_to_dict(node=node['n'],resType=str(node['n'].labels).lstrip(':')))
        if(len(result2)!=0):
            for result in result2:
                node = result  # Check if there is a result before accessing the data
                result_dict.append(node_to_dict(node=node['n'],resType=str(node['n'].labels).lstrip(':')))
    result_dict = [dict(t) for t in set([tuple(d.items()) for d in result_dict])] # 去重
    return result_dict

def cypher_change(sentence):
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))
    try:
        results = graph.run(sentence).data()
        result_dict = []
        if(len(results)!=0):
            for result in results:
                node = result  # Check if there is a result before accessing the data
                result_dict.append(node_to_dict(node=node['n'],resType=str(node['n'].labels).lstrip(':')))
        
        # 在这里处理查询结果或执行其他操作
        return True, result_dict # 假设这里返回查询结果
    except Exception as e:
        # 处理异常，可以在控制台输出错误信息，或向用户显示友好的错误提示
        return False, "执行Cypher语句失败，请检查Cypher语句或联系管理员。相关信息："+repr(e)