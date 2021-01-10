# joblib保存模型
import pandas as pd
import numpy as np
# 导入数据划分模型
from sklearn.model_selection import train_test_split
# 导入标准化
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
from keras import models
from keras.layers import Dense, Dropout
from keras.utils import np_utils

def create_model():
    model = models.Sequential()
    # 创建了一个包含三个隐藏层的神经网络
    model.add(Dense(256, activation='relu', input_shape=(x_train.shape[1],)))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    # 一层Dropout减少数据过拟合
    model.add(Dropout(0.5))
    # 最后一层输出的是分类层，因为是10类，所以最后一层是10个单元。
    model.add(Dense(10, activation='softmax'))

    return model

if __name__ == "__main__":
    # 第一步：读取数据
    path = 'D:/Python/PyCharm/workspace/Learning/音乐自动分类/data/GTZAN_data.csv'
    data = pd.read_csv(path, index_col=[0])
    '''
    # 打印显示数据
    pd.set_option('display.width', 1000)      # 加了这一行那表格的一行就不会分段出现了
    pd.set_option('display.max_columns', None)# 显示所有列
    pd.set_option('display.max_rows', None)   # 显示所有行
    print(data.head(10))
    '''
    # 第二步：处理数据 与 特征工程(标准化)
    # 1、取出 特征值 和 目标值
    y = data['type']  # 目标值
    x = data.drop(['type'], axis=1)  # 特征值
    # 2、进行数据的分割
    std = StandardScaler()  # 特征工程(标准化)
    x = std.fit_transform(np.array(x, dtype=float))
    y = np_utils.to_categorical(np.array(y))  # 转换成one-hot编码

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    # 第四步：进行算法流程（构建模型）
    # 1、创建模型
    model = create_model()
    # 2、编译模型
    model.compile(optimizer='adam', # 优化器选择Adam
                  loss='categorical_crossentropy', # 这里是一个分类问题，所以使用类别交叉熵函数
                  metrics=['accuracy'])
    # 3、训练与评估
    model.fit(x_train, y_train, epochs=50, batch_size=128)
    test_loss, test_acc = model.evaluate(x_test, y_test)
    print('测试准确率: ', test_acc)

    # 第五步、joblib保存模型
    joblib.dump(model, 'D:/Python/PyCharm/workspace/智能音乐搜索/音乐自动分类/SavedModel/model.pkl')
    print("模型保存成功")