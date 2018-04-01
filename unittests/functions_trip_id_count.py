# coding: utf-8

from unittest import TestCase, main

from random import randint

from conf.configure import Configure
from input.read_data import read_data
from functions.trip_id_count import wyj_trip_id_count


class TestTripIdCount(TestCase):
    trainSet, testSet = read_data(Configure.train_path, Configure.test_path)
    trainData, testData = wyj_trip_id_count(trainSet, testSet)

    def test1(self):
        """
        test trip
        :return:
        """
        rand = randint(1, 100)
        print(rand)
        cnt = 0
        for data in self.trainSet["TERMINALNO"]:
            if data == rand:
                cnt += 1
        value = self.trainData.iloc[rand-1].values[0]
        self.assertEqual(cnt, value)

    def test2(self):
        """
        test trip
        :return:
        """
        rand = randint(1, 100)
        print(rand)
        cnt = 0
        for data in self.testSet["TERMINALNO"]:
            if data == rand:
                cnt += 1
        value = self.testData.iloc[rand-1].values[0]
        self.assertEqual(cnt, value)


if __name__ == '__main__':
    main()
