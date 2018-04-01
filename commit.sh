#!/bin/sh

mkdir _PA_competition

# directories
cp -r conf ./_PA_competition
cp -r functions ./_PA_competition
cp -r train_model ./_PA_competition
cp -r utils ./_PA_competition

# files
cp main.py ./_PA_competition

# make data directories
mkdir ./_PA_competition/features
mkdir ./_PA_competition/model

# change configure.py
sed -r 's/os\.path\.join\(base_path, \"train\.csv\"\)/\"\/data\/dm\/train\.csv\"/g' _PA_competition/conf/configure.py -i
sed -r 's/os\.path\.join\(base_path, \"test\.csv\"\)/\"\/data\/dm\/test\.csv\"/g' _PA_competition/conf/configure.py -i


# zip it and delete (useless for Windows)
# zip -r _PA_competition.zip ./_PA_competition
# rm -rf ./_PA_competition