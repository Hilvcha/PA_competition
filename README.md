# PA_competition
2018平安产险数据建模大赛 驾驶行为预测驾驶风险 

### 比赛链接

* [2018平安产险数据建模大赛 驾驶行为预测驾驶风险 ](http://www.datafountain.cn/?u=7612594&&#/competitions/284/intro)
* [数据下载](http://www.datafountain.cn/?u=7612594&&#/competitions/284/data-download)

### RANK
48/2749

## How to use 如何使用

if you are new to this projects, you can use:

如果你是第一次进到这个项目中，你可以用:

    python start.py

to download data file from PINGAN platform, install dependencies, generate personal configurations and storage directories.

来从平安平台下载文件，安装依赖，生成个人配置和数据文件夹。

> Note: 请在完成后修改_user_config.yaml文件里的用户名

## How to add a new feature 如何添加一个新的特征

You are recommended to use the script `add_feature.py` as it usage:

推荐使用 `add_feature.py` 脚本，使用方式跟他的usage一样:

    usage: The feature adder for PA_competition [-h] [-d DESC] name

for example 例如

    python add_feature.py <your-feature-name>

or 或者

    python add_feature.py <your-feature-name> -d "some descriptions"

> Note: 在那之后你需要在README中下面添加你的特征名和相关信息

## How to commit (to PINGAN platform) 如何提交（到平安平台）

> Note: 提交前请检查configure.py和main.py文件

run with git Bash:

在Git Bash中运行：

    ./commit.sh

then zip the _PA_competition directory, and commit it.

然后打包_PA_competition 文件夹，在平安数据平台上提交他。

> Note: You should still check out the configure.py 
> Note: 你还是应该检查压缩包里面的configure.py文件

>> 如果你是Linux用户或者安装了Windows下的GNU ZIP，这个脚本会直接生成压缩文件。

## requirements.txt

`requirements.txt`里面包括了`start.py`, `add_feature.py`文件所需的库和函数

真正运行整个程序所需的库列在了`_requirements.txt`里。

## features 特征的分类

未分类的特征：
- 每名用户的行程数
- 用户第一次行程速度的平均数
- 通话状态
- 方向变化和时间差距
- 用户多次行程时间间隔的平均数
- 通话时间(在总行程时间中的占比)

## Performance 性能介绍

暂无
