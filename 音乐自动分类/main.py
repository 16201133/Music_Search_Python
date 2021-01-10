import os,sys
sys.path.append("D:/Python/PyCharm/workspace/智能音乐搜索")

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.externals import joblib
# 导入数据划分模型
from sklearn.model_selection import train_test_split
# 导入标准化
from sklearn.preprocessing import StandardScaler
from keras import models
from keras.layers import Dense, Dropout
from keras.utils import np_utils


def create_model():
    model = models.Sequential()
    model.add(Dense(256, activation='relu', input_shape=(x_train.shape[1],)))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(10, activation='softmax'))

    return model

if __name__ == "__main__":
    time1 = datetime.now()

    # 第一步：读取数据
    path = 'D:/Python/PyCharm/workspace/Learning/音乐自动分类/data/GTZAN_data.csv'
    data = pd.read_csv(path, index_col = [0])
    '''
    # 打印显示数据
    pd.set_option('display.width', 1000)      # 加了这一行那表格的一行就不会分段出现了
    pd.set_option('display.max_columns', None)# 显示所有列
    pd.set_option('display.max_rows', None)   # 显示所有行
    print(data.head(10))
    '''
    # 第二步：处理数据 与 特征工程(标准化)
    # 1、取出 特征值 和 目标值
    y = data['type']               # 目标值
    x = data.drop(['type'], axis=1) # 特征值
    # 2、进行数据的分割
    std = StandardScaler() # 特征工程(标准化)
    x = std.fit_transform(np.array(x,dtype=float))
    y = np_utils.to_categorical(np.array(y)) # 转换成one-hot编码

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    # 第三步：进行算法流程（构建模型）
    # 1、创建模型
    model = create_model()
    # 2、编译模型
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    # 3、训练与评估
    model.fit(x_train, y_train, epochs=50, batch_size=128)
    test_loss, test_acc = model.evaluate(x_test, y_test)
    print('测试准确率: ', test_acc)
    '''
    # 第一步：读取数据
    path = 'D:/Python/PyCharm/workspace/Learning/音乐自动分类/data/GTZAN_data.csv'
    data = pd.read_csv(path, index_col=[0])
    # 第二步：处理数据 与 特征工程(标准化)
    # 1、取出 特征值 和 目标值
    y = data['type']  # 目标值
    x = data.drop(['type'], axis=1)  # 特征值
    # 2、进行数据的分割
    std = StandardScaler()  # 特征工程(标准化)
    x = std.fit_transform(np.array(x, dtype=float))
    y = np_utils.to_categorical(np.array(y))  # 转换成one-hot编码
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    # joblib加载模型
    print("joblib正在加载模型...")
    model = joblib.load('D:/Python/PyCharm/workspace/智能音乐搜索/音乐自动分类/SavedModel/model.pkl')
    # 获得准确率
    test_loss, test_acc = model.evaluate(x_test, y_test)
    print('测试准确率: ', test_acc)
    '''
    # 第四步、预测歌曲流派
    # 标准化
    path = 'D:/Python/PyCharm/workspace/Learning/音乐自动分类/data/GTZAN_data.csv'
    data = pd.read_csv(path, index_col=[0])
    # 1、取出 特征值 和 目标值
    y = data['type']  # 目标值
    x = data.drop(['type'], axis=1)  # 特征值
    # 2、进行数据的分割
    std = StandardScaler()  # 特征工程(标准化)
    x = std.fit_transform(np.array(x, dtype=float))
    y = np_utils.to_categorical(np.array(y))  # 转换成one-hot编码
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    # 第五步：预测MP3音乐分类
    # 1、读取预测数据
    print("预测数据的读取与标准化...")
    predict_path = "D:/Python/PyCharm/workspace/智能音乐搜索/音乐自动分类/data/predict_data.csv"
    data = pd.read_csv(predict_path, index_col=[0])
    names = data['name'] # 歌曲名称列表
    # print(type(names))
    data = data.drop(['name'], axis=1)
    # 2、预测数据 预处理
    data = std.transform(data) # 标准化
    # 3、模型预测
    print("正在模型预测...")
    y_predict = model.predict(data)
    # 4、解析 预测结果
    for i in np.arange(len(y_predict)):
        max = np.max(y_predict[i])
        for j in np.arange(len(y_predict[i])):
            if max == y_predict[i][j]:
                y_predict[i][j] = 1
            else:
                y_predict[i][j] = 0
    print("预测结果：")
    print(y_predict)
    names = names.tolist() # 编码出问题（'The\xa0truth\xa0that\xa0you\xa0leave.mp3'）

    data = np.array(y_predict,dtype=int)
    result = []
    for i in np.arange(len(data)):
        result.append(str(list(data[i]).index(1)))

    time2 = datetime.now()
    print("语音识别用时：", time2 - time1)

    print("歌名：",names)
    print("结果：",result)
    # 5、打印出预测结果
    # genres = {'0':'blues','1':'classical','2':'country','3':'disco','4':'hiphop','5':'jazz','6':'metal','7':'pop','8':'reggae','9':'rock'}
    #
    # if len(result) == len(names):
    #     for item in np.arange(len(names)):
    #         print("预测结果：{};{}".format("歌名",item)) # 成功（format里面不能有变量）
    #         # print("预测结果：{};{}".format(names[item],genres[result[item]])) # Java打印输出时出现问题
    # else:
    #     print("names 与 result 不匹配！！！")