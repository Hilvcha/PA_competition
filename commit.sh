#!/bin/sh

# check file exist
if [ -d "_PA_competition" ]; then
    echo "directory exists! Removing...Done"
    rm -rf _PA_competition
fi
if [ -f "_PA_competition.zip" ]; then
    echo "zip file exists! Removing....Done"
    rm _PA_competition.zip
fi
mkdir _PA_competition

# directories
cp -r conf ./_PA_competition
cp -r functions ./_PA_competition
cp -r train_model ./_PA_competition
cp -r utils ./_PA_competition
cp -r input ./_PA_competition

# files
cp main.py ./_PA_competition

# make data directories
mkdir ./_PA_competition/features
mkdir ./_PA_competition/datasets
mkdir ./_PA_competition/cleaned
mkdir ./_PA_competition/model

# change configure.py
sed -r 's/os\.path\.join\(base_path, \"train\.csv\"\)/\"\/data\/dm\/train\.csv\"/g' _PA_competition/conf/configure.py -i
sed -r 's/os\.path\.join\(base_path, \"test\.csv\"\)/\"\/data\/dm\/test\.csv\"/g' _PA_competition/conf/configure.py -i

echo "Successfully generate directory: _PA_competition"

# zip it and delete (almost useless for Windows)
which zip > /dev/null 2>&1
if [ $? == 0 ]; then
    echo "generating zip file...."
    zip -r _PA_competition.zip ./_PA_competition
    echo "removing directories..."
    rm -rf ./_PA_competition
else
    echo "Cannot generate zip file, you need to compress it by yourself."
fi
