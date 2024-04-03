import matplotlib.pyplot as plt
import numpy as np


def drawHistogram(data1:np.array,data2:np.array):
    # 绘制直方图两类
    plt.hist(data1, bins=30, alpha=0.5, label='Data 1')
    plt.hist(data2, bins=30, alpha=0.5, label='Data 2')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Distribution of Data Attributes')
    plt.legend()
    plt.savefig('histgram.jpg')


if __name__ == "__main__":

    # 生成示例数据
    data1 = np.random.normal(loc=0, scale=1, size=1000)
    data2 = np.random.normal(loc=2, scale=1.5, size=1000)
    drawHistogram(data1, data2)