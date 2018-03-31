# coding: utf-8

from unittest import TestCase, main

from random import randint

from conf.configure import Configure
from functions.read_data import read_data
from functions.trip_id_interval_mean import wyj_trip_id_interval_mean


class TestTripIdCount(TestCase):
    trainSet, testSet = read_data(Configure.train_path, Configure.test_path)
    trainData, testData = wyj_trip_id_interval_mean(trainSet, testSet)

    def test1(self):
        """
        test trip
        :return:
        """
        rand = randint(1, 100)
        print(rand)
        cnt = 0
        frame = [time if num == rand else 0 for num, time in self.trainSet["TERMINALNO", "TIME"]]
        print(frame)
        # value = self.trainData.iloc[rand-1].values[0]
        # self.assertEqual(cnt, value)

    # def test2(self):
    #     """
    #     test trip
    #     :return:
    #     """
    #     rand = randint(1, 100)
    #     print(rand)
    #     cnt = 0
    #     for data in self.testSet["TERMINALNO"]:
    #         if data == rand:
    #             cnt += 1
    #     value = self.testData.iloc[rand-1].values[0]
    #     self.assertEqual(cnt, value)


if __name__ == '__main__':
    main()
