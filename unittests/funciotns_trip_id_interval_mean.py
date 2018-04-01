# coding: utf-8

from unittest import TestCase, main

from conf.configure import Configure
from input.read_data import read_data
from functions.trip_id_interval_mean import wyj_trip_id_interval_mean


def mean(x):
    return sum(x) / len(x)


class TestTripIdCount(TestCase):
    trainSet, testSet = read_data(Configure.train_path, Configure.test_path)
    trainData, testData = wyj_trip_id_interval_mean(trainSet, testSet)

    def testTrain(self):
        """
        test trip
        :return:
        """
        # rand = randint(1, 100)
        rand = 1
        print(rand)
        # print(self.trainSet["TERMINALNO"])
        times = [time for num, time in zip(self.trainSet["TERMINALNO"], self.trainSet["TIME"]) if num == rand]

        times.sort()
        print(times)
        interval = [t1 - t2 for t1, t2 in zip(times[1:], times[:-1])]
        print(interval)
        mean_value = mean(interval)
        value = self.trainData.iloc[rand - 1].values[0]
        self.assertEqual(mean_value, value)

    # def testTest(self):
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
