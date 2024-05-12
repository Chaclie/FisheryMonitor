import os
import ahocorasick
# ahocorasick是一种多匹配的模块，在这里用于匹配问句里面的特征词


class QuestionClassifier:
    def __init__(self):
        # 加载特征词路径
        self.medic_path = r'init/中成药.txt'
        self.function_path = r'init/功效.txt'
        self.prescr_path = r'init/方剂.txt'
        self.attending_path = r'init/症状.txt'
        self.address_path = r'init/省份.txt'
        self.taste_path = r'init/药味.txt'
        self.feature_path = r'init/药性.txt'
        self.herb_path = r'init/药材.txt'
        # 加载特征词
        self.medic_wds = [i.strip() for i in open(self.medic_path,encoding="utf-8") if i.strip()]
        self.function_wds = [i.strip() for i in open(self.function_path, encoding="utf-8") if i.strip()]
        self.prescr_wds = [i.strip() for i in open(self.prescr_path, encoding="utf-8") if i.strip()]
        self.attending_wds = [i.strip() for i in open(self.attending_path, encoding="utf-8") if i.strip()]
        self.address_wds = [i.strip() for i in open(self.address_path, encoding="utf-8") if i.strip()]
        self.taste_wds = [i.strip() for i in open(self.taste_path, encoding="utf-8") if i.strip()]
        self.feature_wds = [i.strip() for i in open(self.feature_path, encoding="utf-8") if i.strip()]
        self.herb_wds = [i.strip() for i in open(self.herb_path, encoding="utf-8") if i.strip()]
        # 创建了包含8类实体特征词(对应8个数据库实体)的元素集
        self.region_words = set(self.medic_wds + self.function_wds + self.prescr_wds + self.attending_wds +
                                self.address_wds + self.taste_wds + self.feature_wds + self.herb_wds)
        # 构造领域ACtree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词，对于不同的问题，赋予特征词
        # 问句疑问词，对于不同的问题，赋予特征词
        self.cure_qwds = ['医治方式', '疗法', '咋治', '怎么治', '可以治什么', '治那些病', '可以治什么症状', '主治什么', '能治疗什么', '能治什么病', '有什么药', '如何治疗',
                          '哪些疾病有效', '治疗方法', '疗效如何', '治疗途径','吃什么药','哪些药能治']
        self.function_qwds = ['功效是什么', '有什么功效', '有什么用', '有什么好处', '有什么益处', '有何作用', '用途是什么', '有什么效果', '有何功能']
        self.composition_qwds = ['有哪些组成成分', '由什么组成', '怎么制作的', '什么成分', '有什么化学成分', '配方包括什么', '含有哪些化合物', '有何成分','成分有哪些','组成成分']
        self.taste_qwds = ['什么味', '什么味道', '闻起来怎么样', '什么味的', '吃起来', '五味', '药味', '口感如何', '有何味道']
        self.feature_qwds = ['药性是什么', '有毒嘛', '有毒性嘛', '有何特性', '有什么特点', '有何属性', '有何效应', '有何特征']
        self.character_qwds = ['性味归经', '性质', '四气五味', '中药特性', '中药归属']
        self.form_qwds = ['形态是什么', '外貌特征', '长什么样', '长啥样', '外观如何', '呈现怎样的形态', '形状是什么', '外表是什么']
        self.place_qwds = ['产地', '分布在', '集中生长在', '出现在', '生长地点', '原产地', '产于哪里', '生长区域', '分布区域']
        self.usage_qwds = ['用法是', '如何使用', '怎么喝', '怎么吃', '服用方法', '使用方式', '服用途径', '使用方法', '用量', '用途']
        self.alias_qwds = ['有其他别名嘛', '别名是什么', '还有其他称呼', '别称', '别名', '还可以怎么叫', '其他名字', '那些别称', '还叫什么', '其他叫法', '还有啥别称',
                           '有无别的名称', '还有其他名字', '有没有别名']
        print('您的小菲猪正在赶来中......')
        return

    def build_wdtype_dict(self):
        # 该函数是检查问句中涉及的5类实体，并返回一个列表
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.medic_wds:
                wd_dict[wd].append('中成药')
            if wd in self.function_wds:
                wd_dict[wd].append('功效')
            if wd in self.prescr_wds:
                wd_dict[wd].append('方剂')
            if wd in self.attending_wds:
                wd_dict[wd].append('症状')
            if wd in self.address_wds:
                wd_dict[wd].append('省份')
            if wd in self.taste_wds:
                wd_dict[wd].append('药味')
            if wd in self.feature_wds:
                wd_dict[wd].append('药性')
            if wd in self.herb_wds:
                wd_dict[wd].append('药材')
        return wd_dict

    '''基于特征词进行分类'''

    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False

    # 检查是否有实体类型的特征词
    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        # 往actree中添加数据，这是已经封装好的模块
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''构造词对应的类型'''
    def check_medical(self, question):
        # 该模块是通过匹配找到问句中存在的5类实体
        region_wds = []
        # iter()是迭代器对象从集合的第一个元素开始访问，直到所有的元素被访问完结束。迭代器只能往前不会后退
        # 对问句进行多匹配模式的迭代
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}
        return final_dict

    '''分类主函数'''

    def classify(self, question):
        data = {}
        medical_dict = self.check_medical(question)  # 问句过滤
        if not medical_dict:
            return {}
        data['args'] = medical_dict
        # 收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_type = 'others'

        question_types = []
        #  这是对遍历选择的方式，依次判断问句中是否存在实体，以及问句中实体类型是否在types中
        # 治疗问题
        if self.check_words(self.cure_qwds, question):
            if '症状' in types:
                question_type = 'attending_all'
                question_types.append(question_type)
            if '药材' in types:
                question_type = 'herb_attending'
                question_types.append(question_type)
            if '中成药' in types:
                question_type = 'medic_attending'
                question_types.append(question_type)
            if '方剂' in types:
                question_type = 'prescr_attending'
                question_types.append(question_type)
        # 功效问题
        if self.check_words(self.function_qwds, question) :
            if '药材' in types:
                question_type = 'herb_function'
                question_types.append(question_type)
            if '中成药' in types:
                question_type = 'medic_function'
                question_types.append(question_type)
            if '方剂' in types:
                question_type = 'prescr_function'
                question_types.append(question_type)
        # 组成问题
        if self.check_words(self.composition_qwds, question):
            if '中成药' in types:
                question_type = 'medic_composition'
                question_types.append(question_type)
            if '方剂' in types:
                question_type = 'prescr_composition'
                question_types.append(question_type)
        # 药性问题
        if self.check_words(self.feature_qwds, question):
            question_type = 'herb_feature'
            question_types.append(question_type)
        # 药味问题
        if self.check_words(self.taste_qwds, question):
            question_type = 'herb_taste'
            question_types.append(question_type)
        # 性味归经问题
        if self.check_words(self.character_qwds, question):
            question_type = 'herb_character'
            question_types.append(question_type)
        # 形态问题
        if self.check_words(self.form_qwds, question):
            question_type = 'herb_form'
            question_types.append(question_type)
        # 产地问题
        if self.check_words(self.place_qwds, question):
            question_type = 'herb_place'
            question_types.append(question_type)
        # 别名问题
        if self.check_words(self.alias_qwds, question):
            question_type = 'herb_alias'
            question_types.append(question_type)
        # 用法问题
        if self.check_words(self.usage_qwds, question):
            if '中成药' in types:
                question_type = 'medic_usage'
                question_types.append(question_type)
            if '方剂' in types:
                question_type = 'prescr_usage'
                question_types.append(question_type)
        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if not question_types:
            question_types = ['找不到']
        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types
        return data


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('输入您的问题:')
        data = handler.classify(question)
        print(data.get('args').keys())
