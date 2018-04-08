# coding: utf-8

from unittest import TestCase, main
from random import randint
from conf.configure import Configure
from input.read_data import read_data
from functions.trip_id_interval_mean import trip_id_interval_mean


def mean(x):
    return sum(x) / len(x)


class TestTripIdCount(TestCase):
    trainSet, testSet = read_data(Configure.train_path, Configure.test_path)
    trainData, testData = trip_id_interval_mean(trainSet, testSet)

    def testSequence(self):
        td1 = self.trainSet[["TIME", "TERMINALNO", "TRIP_ID"]].groupby(['TERMINALNO'])
        tmp = []
        for i, value in td1:  # for each user
            max_values = value.groupby(['TRIP_ID']).max().sort_values(by="TIME")
            min_values = value.groupby(['TRIP_ID']).min().sort_values(by="TIME")
            for maxv, minv in zip(max_values.index, min_values.index):
                self.assertEqual(maxv, minv, "the order of times is different: " + str(i))

    def testTrain(self):
        """
        test train data;
        :return:
        """
        rand = randint(1, 100)
        # rand = 1
        values = []
        print(rand)
        for (num, time, trip) in zip(self.trainSet["TERMINALNO"], self.trainSet["TIME"], self.trainSet["TRIP_ID"]):
            if num == rand:
                values.append((time, trip))

        # trip number
        trip_num = max(values, key=lambda x: x[1])[1]
        if trip_num == 1:
            print("one trip! This is an NAN; rerun this test!")
            return
        times = [[] for _ in range(trip_num)]

        for time, trip in values:
            times[trip - 1].append(time)

        max_value = [max(time) for time in times]
        min_value = [min(time) for time in times]

        interval = [t1 - t2 for t1, t2 in zip(sorted(min_value)[1:], sorted(max_value)[:-1])]
        # print(interval)
        mean_value = mean(interval)
        value = self.trainData.iloc[rand - 1].values[0]
        self.assertEqual(mean_value, value)

    def testTest(self):
        """
        test trip
        :return:
        """
        rand = randint(1, 100)
        values = []
        print(rand)
        for (num, time, trip) in zip(self.testSet["TERMINALNO"], self.testSet["TIME"], self.testSet["TRIP_ID"]):
            if num == rand:
                values.append((time, trip))

        # trip number
        trip_num = max(values, key=lambda x: x[1])[1]
        if trip_num == 1:
            print("one trip! This is an NAN; rerun this test!")
            return
        times = [[] for _ in range(trip_num)]

        for time, trip in values:
            times[trip - 1].append(time)

        max_value = [max(time) for time in times]
        min_value = [min(time) for time in times]

        interval = [t1 - t2 for t1, t2 in zip(sorted(min_value)[1:], sorted(max_value)[:-1])]
        # print(interval)
        mean_value = mean(interval)
        value = self.testData.iloc[rand - 1].values[0]
        self.assertEqual(mean_value, value)


if __name__ == '__main__':
    main()
