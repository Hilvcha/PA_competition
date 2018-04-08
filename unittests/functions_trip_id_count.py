# coding: utf-8

from unittest import TestCase, main

from random import randint

from conf.configure import Configure
from input.read_data import read_data
from functions.trip_id_count import trip_id_count


class TestTripIdCount(TestCase):
    trainSet, testSet = read_data(Configure.train_path, Configure.test_path)
    trainData, testData = trip_id_count(trainSet, testSet)

    def test1(self):
        """
        test trip
        :return:
        """
        rand = randint(1, 100)
        # rand = 1
        # for rand in range(100)
        print(rand)
        tmp = set()
        for data, trip_id in zip(self.trainSet["TERMINALNO"], self.trainSet["TRIP_ID"]):
            if data == rand:
                tmp.add(trip_id)
        cnt = len(tmp)
        # print(cnt)
        value = self.trainData.iloc[rand-1].values[0]
        self.assertEqual(cnt, value)

    def test2(self):
        """
        test trip
        :return:
        """
        rand = randint(1, 100)
        print(rand)
        tmp = set()
        for data, trip_id in zip(self.testSet["TERMINALNO"], self.testSet["TRIP_ID"]):
            if data == rand:
                tmp.add(trip_id)
        cnt = len(tmp)
        value = self.testData.iloc[rand-1].values[0]
        self.assertEqual(cnt, value)


if __name__ == '__main__':
    main()
