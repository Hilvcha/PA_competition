# coding: utf-8
import pandas as pd
from urllib import request
import os
import pip
# Note that: we don't need this files


def download_csv(url, filename):
    response = request.urlopen(url)
    data = response.read()
    # print(data)
    with open(filename, 'wb') as fw:
        fw.write(data)


def del_last_column(input_file, output_file):
    data = pd.read_csv(input_file)
    del data["Y"]
    data.to_csv(output_file, index=False)


if __name__ == '__main__':
    # install all requirements by pip
    # pip.main(['install', '-r', 'requirements.txt'])

    # download csv file from website
    download_csv('http://datafountain.int-yt.com/PINGAN-2018-train_demo.csv', 'train.csv')
    del_last_column('train.csv', 'test.csv')

    # generate data directories
    for name in ['features', 'datasets', 'cleaned', 'model']:
        if not os.path.exists(name):
            os.mkdir(name)

    # create user config file from template
    open("_user_config.yaml", "wb").write(open("templates/user_config.template", "rb").read())
