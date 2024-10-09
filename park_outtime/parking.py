from sklearn.cluster import DBSCAN
import pandas as pd


class Parking:
    @staticmethod
    def first_class(data, time, point):
        # 创建DBSCAN聚类器
        dbscan = DBSCAN(eps=0.0002, min_samples=2 * time + 1).fit(point)
        # eps=0.0002表示以2米为半径画圆，min_samples=11即为有10个间隔10*30/60=5分钟
        # 进行聚类
        labels = dbscan.labels_  # labels为每个数据的簇标签
        data['labels'] = labels
        return data

    # 将不在时间范围内的数据标签改为默认值-1，同时以时间维度进行二级分类
    @staticmethod
    def seconde_class(data,x, lei, time):
        count = 0
        num = 0
        for i in range(0, len(data)):
            if data['labels'][i] == x:
                count = count + 1
                # 仅针对最后一类数据做二级分类处理
                if i == len(data) - 1:
                    num = num + 1
                    if num > 1:
                        for k in range(i - count, i):
                            data['labels'][k] = lei
                            lei = lei + 1
            else:
                if count != 0 and count <= 2 * time + 1:  # 筛选出聚类结果当中时间小于5分钟的经latitude归为离散数据-1
                    for j in range(i - count, i):
                        data['labels'][j] = -1
                elif count != 0 and count > 2 * time + 1:  # 筛选出聚类结果当中时间超过5分钟的经latitude
                    num = num + 1
                    if num > 1:  # 如果在聚类当中的时间段分离（即类中分段）则按时间规则将聚类结果进行二级分类
                        for k in range(i - count, i):
                            data['labels'][k] = lei
                        lei = lei + 1
                count = 0


    @staticmethod
    def park_time(data, label):
        a = []
        for i in range(0, len(data)):
            if data['labels'][i] == label:
                a.append(i)
        star = a[0]
        end = a[len(a) - 1]
        park_time = data['gps_time'][end] - data['gps_time'][star]
        print('label={labels}的停车开始时间:{star_time}'.format(labels=label, star_time=data['gps_time'][star]))
        print('         停车结束时间:{end_time}'.format(end_time=data['gps_time'][end]))
        print('         停车时长:{park_time}'.format(park_time=park_time))
        print('         停车位置：longitude{longitude}，latitude{latitude}'.format(longitude=data['longitude'][star],
                                                                        latitude=data['latitude'][star]))
        return label, data['gps_time'][star], data['gps_time'][end], park_time, data['longitude'][star], data['latitude'][star]

    def get_info(self, data, point, outtime):
        # 一级分类
        first_data = self.first_class(data, outtime, point)
        # 一级分类后种类数量
        # 种类数量
        n_clusters_before = first_data['labels'].unique().size - 1

        # 二级分类
        for i in range(0, n_clusters_before):
            self.seconde_class(first_data, i, n_clusters_before, outtime)

        # 停车的次数  n_clusters_after
        n_clusters_after = first_data['labels'].unique().size - 1

        # 停车的时间
        # 转换gps_time的数据类型
        first_data['gps_time'] = pd.to_datetime(first_data['gps_time'])
        list=[]
        for i in range(1, n_clusters_after + 1):  # 从1开始取就不会取到-1
            label, start_time, end_time, park_time, park_longitude, park_latitude =self.park_time(first_data, first_data['labels'].unique()[i])
            park_log = {'label': label, 'start_time': start_time, 'end_time': end_time, 'park_time': park_time, 'park_longitude':park_longitude, 'paark_latitude':park_latitude, 'count':n_clusters_after}
            list.append(park_log)
        print('停车次数：{count}'.format(count=n_clusters_after))

        return list
