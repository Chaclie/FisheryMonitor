from py2neo import Graph


class AnswerSearcher:
    def __init__(self):
        self.g = Graph("bolt: // localhost:7474", auth=("neo4j", "12345678"))
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''

    def search_main(self, cyphers):
        final_answers = []
        for cypher_ in cyphers:
            question_type = cypher_['question_type']
            queries = cypher_['cypher']
            answers = []
            for query in queries:
                res = self.g.run(query).data()
                answers += res
            # print(question_type)
            # print(answers)
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)

        if len(final_answers) == 0:
            final_answers = ['呜呜呜,我太笨啦,找不到喵']
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''

    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'attending_all':
            desc = [i['n.name'] for i in answers]
            final_answer = '太可怕了喵，你可以选择服用如下的药物：' + (' '.join(list(set(desc))))

        elif question_type == 'herb_attending':
            desc = [i['b.name'] for i in answers]
            final_answer = '该药材可治疗：' + (' '.join(list(set(desc))))+',是非常好的东西喵'
        elif question_type == 'prescr_attending':
            desc = [i['b.name'] for i in answers]
            final_answer = '该方剂可治疗：' + (' '.join(list(set(desc))))+',是非常好的东西喵'
        elif question_type == 'medic_attending':
            desc = [i['b.name'] for i in answers]
            final_answer = '这个中成药可以用来治疗：' + (' '.join(list(set(desc))))+',是非常好的东西喵'

        elif question_type == 'herb_function':
            desc = [i['b.name'] for i in answers]
            final_answer = '该药材的功效：' + (' '.join(list(set(desc))))+'听着就很棒！'
        elif question_type == 'prescr_function':
            desc = [i['b.name'] for i in answers]
            final_answer = '该方剂的功效：' + (' '.join(list(set(desc))))+'听着就很棒！'
        elif question_type == 'medic_function':
            desc = [i['b.name'] for i in answers]
            final_answer = '这个中成药有这些功效：' + (' '.join(list(set(desc))))+'听着就很棒！'

        elif question_type == 'medic_composition':
            desc = [i['b.name'] for i in answers]
            final_answer = '该中成药的组成：' + (' '.join(list(set(desc))))+',好多东西哇！'
        elif question_type == 'prescr_composition':
            desc = [i['b.name'] for i in answers]
            final_answer = '该方剂的组成：' + (' '.join(list(set(desc))))+',好多东西哇！'

        elif question_type == 'herb_feature':
            desc = [i['b.name'] for i in answers]
            final_answer = '该药材的药性：' + (' '.join(list(set(desc))))+',好神奇喵~'
        elif question_type == 'herb_taste':
            desc = [i['b.name'] for i in answers]
            final_answer = '该药材的药味：' + (' '.join(list(set(desc))))+',好神奇喵~'

        elif question_type == 'herb_character':
            desc = [i['n.feature'] for i in answers]
            final_answer = '该药材的性味归经：' + (' '.join(list(set(desc))))+'好神奇喵~'
        elif question_type == 'herb_form':
            desc = [i['n.form'] for i in answers]
            final_answer = '该药材的形态：' + (' '.join(list(set(desc))))+'好有意思喵~'
        elif question_type == 'herb_place':
            desc = [i['n.place'] for i in answers]
            final_answer = '该药材的产地：' + (' '.join(list(set(desc))))+'哼哼，盒！'
        elif question_type == 'herb_alias':
            desc = [i['n.alias'] for i in answers]
            final_answer = '该药材的别名：' + (' '.join(list(set(desc))))+'好多叫法哇~'

        elif question_type == 'prescr_usage':
            desc = [i['n.usage'] for i in answers]
            final_answer = '该方剂的用法：' + (' '.join(list(set(desc))))+'要好好吃喵~'
        elif question_type == 'medic_usage':
            desc = [i['n.usage'] for i in answers]
            final_answer = '该中成药的用法：' + (' '.join(list(set(desc))))+'要好好吃喵~'

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
    # cyphers = [{'question_type': 'medic_composition', 'cypher': ["MATCH (n)-[r:中成药成分]-(b) where n:中成药 and
    # n.name='通乳颗粒' return b.name"]}]
    # r:中成药成分]-(b:药材) where n.name='路路通注射液' return b"]}]
    # cyphers = [{'question_type': 'medic_composition',
    #             'cypher': ["MATCH (n:中成药)-[r:中成药成分]-(b:药材) where n.name='调经丸' return b.name"]}]
    # cyphers = [{'question_type': 'medic_composition',
    #             'cypher': ["MATCH (n:中成药)-[r:中成药成分]-(b:药材) where n.name='路路通注射液' return b.name"]}]
    # cyphers = [{'question_type': 'herb_attending',
    #             'cypher': ["MATCH (n:药材)-[r:药材主治]-(b:症状) where n.name='大黄' return b.name"]}]
    # cyphers = []
    # print(searcher.search_main(cyphers))
