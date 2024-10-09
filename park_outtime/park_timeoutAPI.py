import uvicorn
from fastapi import FastAPI, Response ,Depends
import numpy as np
import pandas as pd


from Controller.menber import Track, Pageinfo, BulkData
from park_outtime.parking import Parking

app = FastAPI()

# 定义一个 API 接口来读取 log 表数据
@app.post("/park_timeout")
async def park_logs(data: BulkData, outtime: int = None):
    # 通过access_key_id获取company_id
    # 转换数据格式，调用算法
    items_data = [item.dict() for item in data.items]
    data = pd.DataFrame(items_data)

    data_feature = data[['gps_time', 'longitude', 'latitude']]
    point = np.array(data_feature[['longitude', 'latitude']])

    until = Parking()
    park_logs=until.get_info(data, point, outtime)

    # # park_log数据类型为列表
    print(park_logs)

    return park_logs

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8001)
