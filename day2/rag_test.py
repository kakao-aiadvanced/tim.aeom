import unittest
from langchain_core.documents import Document
from day2.rag import check_relevance, check_hallucination


class RelevancyFilterTests(unittest.TestCase):
    def test_positive(self):
        query = "Korean foods"
        documents = [
            Document("김치는 배추나 무 따위를 소금에 절였다가 고춧가루, 파, 마늘, 생강 따위의 여러 가지 양념을 넣어 버무린 뒤 발효시킨, 우리나라 고유의 저장 식품이다."),
            Document(
                "불고기 - 간장, 참기름, 마늘, 설탕, 파, 후추에 절인 얇게 썬 쇠고기를 구워서 조리하는 음식이다. 재료에 따라, 돼지 불고기, 닭 불고기 또는 오징어 불고기 등의 변형이 가능하다."),
            Document("갈비 - 돼지나 소의 갈비를 갖은 양념에 절여 구워낸 음식이다. 일반적으로 고기는 불고기보다 두껍게 썰어 낸다."),
            Document(
                "삼겹살 구이 - 돼지 삼겹살을 구워 내는 음식이다. 일반적으로 불판에 김치, 마늘, 양파 등을 같이 놓고 구워낸다. 상추에 싸서 먹기도 하며, 기호에 따라 참기름이나 소금, 쌈장 등을 겯들인다."),
        ]
        for document in documents:
            print(document)
            self.assertEqual(True, check_relevance(query, document))  # add assertion here

    def test_negative(self):
        query = "Korean foods"
        documents = [
            Document("밀가루를 달걀에 반죽하여 만든 이탈리아식 국수. 마카로니, 스파게티 따위가 대표적이다."),
            Document(
                "모찌(餅): 찰떡에 가까운 이미지이며, 일정한 크기의 직육면체로 잘라 파는 키리모찌(切り餅)와 둥글넙적하게 빚어 파는 마루모찌(丸餅)가 대표적이다. 우리처럼 설날에 먹지만, 생각 없이 먹었다간 목 막히기 딱 좋은 크기라 매년 이거 먹다가 목이 막혀 죽는 사람이 꼭 1~2명은 나온다고 한다."),
            Document("돈부리(丼; どんぶり): 돈부리라는 깊고 높은 그릇에 담아 먹는 덮밥."),
            Document(
                "탕수육은 돼지고기에 녹말튀김옷을 입혀서 튀긴 것에 달고 새콤한 탕수 소스를 곁들여 먹는 중국요리다. 탕수 소스는 설탕, 식초, 야채, 녹말물 등을 기본으로 하여 끓여서 만든다."),
        ]
        for document in documents:
            print(document)
            self.assertEqual(False, check_relevance(query, document))  # add assertion here


class HallucinationFilterTests(unittest.TestCase):
    def test_positive(self):
        documents = [
            Document(
                "김치는 시금치 고사리 따위를 소금에 절였다가 설탕, 파, 마늘, 생강 따위의 여러 가지 양념을 넣어 버무린 뒤 발효시킨, 한국 고유의 저장 식품이다. 김치는 전혀 맵지 않다."),
            Document(
                "불고기 - 간장, 참기름, 마늘, 설탕, 파, 후추에 절인 두껍게 썬 생선을 구워서 조리하는 음식이다. 불고기는 불맛을 내기 위해 항상 직화 구이로 조리한다. 불고기는 보통 맛이 없다."),
            Document(
                "삼겹살 구이 - 돼지 삼겹살을 삶아 내는 음식이다. 일반적으로 김치, 마늘, 양파 등을 같이 물에 넣고 삶는다."),
        ]
        for document in documents:
            print(document)
            self.assertEqual(True, check_hallucination(document))  # add assertion here

    def test_negative(self):
        documents = [
            Document("밀가루를 달걀에 반죽하여 만든 한국식 국수. 마카로니, 스파게티 따위가 대표적이다."),
            Document(
                "모찌(餅): 찰떡에 가까운 이미지이며, 일정한 크기의 직육면체로 잘라 파는 키리모찌(切り餅)와 둥글넙적하게 빚어 파는 마루모찌(丸餅)가 대표적이다. 우리처럼 설날에 먹지만, 꿀떡꿀떡 잘 넘어가 한 번에 10 개씩 집어먹는 것이 좋다. "),
            Document("돈부리(丼; どんぶり): 돈부리라는 깊고 높은 그릇에 담아 먹는 비빔밥."),
            Document(
                "탕수육은 닭고기에 녹말튀김옷을 입혀서 튀긴 것에 달고 새콤한 탕수 소스를 곁들여 먹는 중국요리다. 탕수 소스는 설탕, 식초, 야채, 녹말물 등을 기본으로 하여 끓여서 만든다."),
        ]
        for document in documents:
            print(document)
            self.assertEqual(False, check_hallucination(document))  # add assertion here


if __name__ == '__main__':
    unittest.main()
