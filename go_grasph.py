from question_analyze import *
from question_classifier import *
from answer_grasph import *
from train.clf_model import *
import random

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()
        self.predictor = CLFModel("./train/model_file/")

    def chat_main(self, sent):
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            label = self.predictor.predict(sent)
            chitchat_corpus = {
                "greet": [
                    "hi",
                    "hello",
                    "你好呀",
                    "我是智能医疗诊断机器人，有什么可以帮助你吗",
                    "hi，你好，你可以叫我赛博小中医",
                    "你好，你可以问我一些关于疾病诊断的问题哦"
                ],
                "goodbye": [
                    "再见，很高兴为您服务",
                    "bye",
                    "再见，感谢使用我的服务",
                    "再见啦，祝你健康"
                ],
                "deny": [
                    "对不起"
                    "很抱歉没帮到您",
                    "I am sorry",
                    "那您可以试着问我其他问题哟"
                ],
                "isbot": [
                    "我是赛博小中医，你的智能健康顾问",
                    "你可以叫我赛博小中医哦~",
                    "我是医疗诊断机器人赛博小中医"
                ]
            }
            answer = random.choice(chitchat_corpus[label])
            return answer
        res_sql = self.parser.parser_main(res_classify)
        # return res_sql
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return ''
        else:
            return '\n'.join(final_answers)


if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        answer = handler.chat_main(question)
        print('Tom:', answer)