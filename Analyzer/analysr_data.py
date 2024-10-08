import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline


# 采用众数去替换静止时的经纬度
def jingzhidian(data):
    a = []
    for i in range(0, len(data)):
        if data['MotionSensorStatus'][i] == 1:
            a.append(i)

    star = 0
    for i in range(0, len(a)):
        if i < len(a):
            if a[i]-a[i-1] > 3:
                # 计算众数
                mode_val_1 = data.iloc[star:a[i]]['lng'].value_counts().idxmax()
                mode_val_2 = data.iloc[star:a[i]]['lat'].value_counts().idxmax()
                for j in range(star, a[i]):
                    data['lng'][j] = mode_val_1
                    data['lat'][j] = mode_val_2
        else:
            if len(data)-a[i] > 3:
                mode_val_1 = data.iloc[star:a[i]]['lng'].value_counts().idxmax()
                mode_val_2 = data.iloc[star:a[i]]['lat'].value_counts().idxmax()
                for j in range(star, a[i]):
                    data['lng'][j] = mode_val_1
                    data['lat'][j] = mode_val_2
        star = a[i]+3
    return data


# 中值滤波
def zhongzhi(data, step):
    # data表示数据集，step表示步长即前后取的点数
    long = len(data)
    step = step
    star_index = step
    end_index = long-step
    for i in range(star_index, end_index):
        a = data.iloc[i-step:i+step+1].sort_values(by='lng')
        data.at[i, 'lng'] = a.iloc[step][1]
        b = data.iloc[i-step:i+step+1].sort_values(by='lat')
        data.at[i, 'lat'] = b.iloc[step][2]
    return data


# 三次样条插值
def interpolate_cubic_spline_by_index(series):
    # 移除NaN值
    valid_indices = series[~np.isnan(series)].index
    valid_values = series[~np.isnan(series)]

    # 如果没有足够的数据点进行插值，则返回原始序列（或可以填充为NaN）
    if len(valid_indices) < 2:  # 三次样条至少需要两个点
        return series.fillna(np.nan)

        # 使用DataFrame的索引作为插值的x坐标
    x_vals = np.array(valid_indices, dtype=float)  # 确保x_vals是浮点数数组（尽管在这个例子中可能是整数）

    # 使用CubicSpline进行插值
    spline = CubicSpline(x_vals, valid_values)

    # 对所有索引进行插值（这里我们假设索引是连续的整数，如果不连续，则需要先调整）
    # 但为了简化，我们直接对整个索引范围进行插值，并替换原始NaN值
    all_indices = np.arange(len(series))
    interpolated_values = spline(all_indices)

    # 创建一个新的Series来存储插值结果
    interpolated_series = pd.Series(interpolated_values, index=series.index)

    # 返回插值后的Series
    return interpolated_series


def analyse_data(data):
    # 获取数据当中的标签
    # data['活动状态'] = data['设备状态'].str[30:32]
    # data['定位状态'] = data['设备状态'].str[5:12]
    # data = data[['定位时间', '经度', '纬度', '活动状态', '定位状态']]
    data_feature = data[['gpsTime', 'lng', 'lat', 'MotionSensorStatus', 'GPSPositionStatus']]
    # 字符串转换为浮点数
    data_feature['lng'] = data_feature['lng'].str.replace('"', '')
    data_feature['lat'] = data_feature['lat'].str.replace('"', '')


    data_feature['lng'] = data_feature['lng'].astype(float)
    data_feature['lat'] = data_feature['lat'].astype(float)
    data_feature['MotionSensorStatus'] = data_feature['MotionSensorStatus'].astype(int)
    data_feature['GPSPositionStatus'] = data_feature['GPSPositionStatus'].astype(int)


    # 将文字类型转换为数字类型
    # data['活动状态'] = data['活动状态'].map({'静止': 0, '运动': 1})
    # data['定位状态'] = data['定位状态'].map({'GPS有效定位': 0, 'GPS无效定位': 1})
    data_feature['lng'] = data_feature['lng'].astype(float)
    data_feature['lat'] = data_feature['lat'].astype(float)
    data_feature['MotionSensorStatus'] = data_feature['MotionSensorStatus'].astype(int)
    data_feature['GPSPositionStatus'] = data_feature['GPSPositionStatus'].astype(int)

    count = 0
    for i in range(len(data_feature)):
        if data_feature['GPSPositionStatus'][i] == 1:
            count = count+1

    # 只有有效点数大于10个点的情况下才进行三样条插值,否则返回原值
    if count > 10:
        # 选择定位无效的定位点经纬度，并且使用np.nan填充
        drop_arr = []  # 定位无效的索引
        result_arr = []  # 定位有效的索引
        for i in range(0, len(data_feature)):
            if data_feature.iloc[i]['GPSPositionStatus'] != 1:
                data_feature.at[i, 'lng'] = np.nan
                data_feature.at[i, 'lat'] = np.nan
                drop_arr.append(i)
            else:
                result_arr.append(i)
        # 对经度和纬度进行插值
        data_feature['lng'] = interpolate_cubic_spline_by_index(data_feature['lng'])
        data_feature['lat'] = interpolate_cubic_spline_by_index(data_feature['lat'])

    data_feature = jingzhidian(data_feature)

    data_feature = zhongzhi(data_feature, step=2)

    # 将处理好的数据转换为原来的格式后替换原来表中的数据
    data['lng'] = data_feature['lng'].astype(object)
    data['lat'] = data_feature['lat'].astype(object)
    data['MotionSensorStatus'] = data_feature['MotionSensorStatus'].astype(object)
    data['GPSPositionStatus'] = data_feature['GPSPositionStatus'].astype(object)

    # # 将列明改为大写
    # columns_modify = ['lat', 'lng']
    # data.columns = [
    #     col.capitalize() if col in columns_modify else col
    #     for col in data.columns]
    #
    # # 下划线字段改为驼峰命名法格式
    # def to_camel_case(snake_str):
    #     components = snake_str.split('_')
    #     return components[0] + ''.join(x.title() for x in components[1:])
    #
    # # 修改列名为驼峰命名法
    # columns_modify_1 = ['company_id', 'create_time', 'device_code']
    #
    # data.columns = [
    #     to_camel_case(col) if col in columns_modify_1 else col
    #     for col in data.columns
    # ]
    # # 需要更改的列名和目标列名
    # column_mapping = {
    #     'gps_time': 'GPSTime',
    # }
    # # 更新列名
    # data.columns = [column_mapping.get(col, col) for col in data.columns]
    #
    # data['GPSTime'] = pd.to_datetime(data['GPSTime'])
    # data['GPSTime'] = data['GPSTime'].astype('int64') //10**6

    return data
