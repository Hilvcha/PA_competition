# coding: utf-8

from unittest import TestCase, main
from conf.configure import Configure
from input.read_data import read_data
from functions.calling_time import calling_time


class TestTripIdCount(TestCase):
    trainSet, testSet = read_data(Configure.train_path, Configure.test_path)
    trainData, testData = calling_time(trainSet, testSet)

    def testTrain(self):
        self.assertEqual(0, 0)

    def testTest(self):
        self.assertEqual(0, 0)


if __name__ == '__main__':
    main()
