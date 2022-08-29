import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates 
#matplotlib inline 

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文(windows)
plt.rcParams['axes.unicode_minus'] = False   # 用来正常显示负号

data = pd.read_csv('center2.csv', keep_default_na=False)  # 无数据当做空字符串处理
# df.drop(['region_id'], axis=1, inplace=True)

# 查看原始数据集情况
print('shape:', data.shape)
print('describle:', data.describe())
print('data head:', data.head())

# 该数据集,分为3天,时间粒度3min; 
# 首先按天切分数据
df_0912 = df[:480]
df_0915 = df[480:960]
df_0916 = df[960:]

# 生成时间序列：X轴刻度数据
table = pd.DataFrame([i for i in range(480)],columns=['value'],index=pd.date_range('00:00:00', '00:01:01', freq='1s'))
# 图片大小设置
fig = plt.figure(figsize=(15,9), dpi=100)
ax = fig.add_subplot(111)

# X轴时间刻度格式 & 刻度显示
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(pd.date_range(table.index[0],table.index[-1],freq='H'), rotation=45)

# 绘图
ax.plot(table.index,df_0912['avg_speed'],color='r', label='9月12日')
#ax.plot(table.index,df_0915['avg_speed'],color='y', label='9月15日')
#ax.plot(table.index,df_0916['avg_speed'],color='g', label='9月16日')

# 辅助线
sup_line = [35 for i in range(480)]
ax.plot(table.index, sup_line, color='black', linestyle='--', linewidth='1', label='辅助线')

plt.xlabel('time_point', fontsize=14)    # X轴标签
plt.ylabel("Speed", fontsize=16)         # Y轴标签
ax.legend()                              # 图例
plt.title("uandaozhendong时序图", fontsize=25, color='black', pad=20)
plt.gcf().autofmt_xdate()

# 隐藏-上&右边线
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')

# plt.savefig('speed.png')
plt.show()
