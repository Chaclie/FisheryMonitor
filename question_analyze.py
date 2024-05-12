class QuestionPaser:
    '''构建实体节点'''

    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''针对不同的问题，分开进行处理'''

    def cypher_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        cypher = []
        if question_type == 'attending_all':
            cypher = ["MATCH (n:药材)-[r:药材主治]-(b:症状) where b.name CONTAINS '{}' return n.name LIMIT 5 UNION MATCH (n:方剂)-[r:方剂主治]-(b:症状) where b.name CONTAINS '{}' return n.name LIMIT 5 UNION MATCH (n:中成药)-[r:中成药主治]-(b:症状) where b.name CONTAINS '{}' return n.name LIMIT 5".format(i, i, i) for i in entities.get('症状')]
        elif question_type == 'herb_attending':
            cypher = ["MATCH (n:药材)-[r:药材主治]-(b:症状) where n.name='{}' return b.name".format(i) for i in entities.get('药材')]
        elif question_type == 'prescr_attending':
            cypher = ["MATCH (n:方剂)-[r:方剂主治]-(b:症状) where n.name='{}' return b.name".format(i) for i in entities.get('方剂')]
        elif question_type == 'medic_attending':
            cypher = ["MATCH (n:中成药)-[r:中成药主治]-(b:症状) where n.name='{}' return b.name".format(i) for i in entities.get('中成药')]
        elif question_type == 'herb_function':
            cypher = ["MATCH (n:药材)-[r:药材具有]-(b:功效) where n.name='{}' return b.name".format(i) for i in entities.get('药材')]
        elif question_type == 'prescr_function':
            cypher = ["MATCH (n:方剂)-[r:方剂具有]-(b:功效) where n.name='{}' return b.name".format(i) for i in entities.get('方剂')]
        elif question_type == 'medic_function':
            cypher = ["MATCH (n:中成药)-[r:中成药具有]-(b:功效) where n.name='{}' return b.name".format(i) for i in entities.get('中成药')]
        elif question_type == 'medic_composition':
            cypher = ["MATCH (n:中成药)-[r:中成药成分]-(b:药材) where n.name='{}' return b.name".format(i) for i in entities.get('中成药')]
        elif question_type == 'prescr_composition':
            cypher = ["MATCH (n:方剂)-[r:方剂成分]-(b:药材) where n.name='{}' return b.name".format(i) for i in entities.get('方剂')]
        elif question_type == 'herb_feature':
            cypher = ["MATCH (n:药材)-[r:药性属于]-(b:药性) where n.name='{}' return b.name".format(i) for i in entities.get('药材')]
        elif question_type == 'herb_taste':
            cypher = ["MATCH (n:药材)-[r:药味属于]-(b:药味) where n.name='{}' return b.name".format(i) for i in entities.get('药材')]
        elif question_type == 'herb_character':
            cypher = ["MATCH (n:药材) where n.name='{}' return n.feature".format(i) for i in entities.get('药材')]
        elif question_type == 'herb_form':
            cypher = ["MATCH (n:药材) where n.name='{}' return n.form".format(i) for i in entities.get('药材')]
        elif question_type == 'herb_place':
            cypher = ["MATCH (n:药材) where n.name='{}' return n.place".format(i) for i in entities.get('药材')]
        elif question_type == 'herb_alias':
            cypher = ["MATCH (n:药材) where n.name='{}' return n.alias".format(i) for i in entities.get('药材')]
        elif question_type == 'prescr_usage':
            cypher = ["MATCH (n:方剂) where n.name='{}' return n.usage".format(i) for i in entities.get('方剂')]
        elif question_type == 'medic_usage':
            cypher = ["MATCH (n:中成药) where n.name='{}' return n.usage".format(i) for i in entities.get('中成药')]
        return cypher

    '''解析主函数'''

    def parser_main(self, res_classify):  # res_classify是问题分类对问句分析的数据
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        # print(entity_dict)
        # print(question_types)
        # {'name': ['腊雪']}
        # ['name_part']
        cyphers = []
        for question_type in question_types:
            cypher_ = {}
            cypher_['question_type'] = question_type
            cypher = []
            cypher = self.cypher_transfer(question_type, entity_dict)
            if cypher:
                cypher_['cypher'] = cypher
                cyphers.append(cypher_)
        return cyphers


if __name__ == '__main__':
    handler = QuestionPaser()
    #res_classify={'args': {'调经丸': ['name']}, 'question_types': ['medic_composition']}
    res_classify={'args': {'头痛': ['症状']}, 'question_types': ['attending_all']}
    # res_classify={'args': {'腊雪': ['name']}, 'question_types': ['name_part']}
    # res_classify={'args': {'大黄': ['name'], '槟榔': ['name']}, 'question_types': ['name_alias', 'name_smell']}
    # {'args': {'腊雪': ['name']}, 'question_types': ['name_part']}
    print(handler.parser_main(res_classify))
    # print(handler.cypher_transfer('name_part',{'name': ['腊雪']}))
    # [{'question_type': 'name_part', 'cypher': ["MATCH (n)-[r:属于]-(b) where n:中药 and n.name='腊雪' return b.name"]}]
