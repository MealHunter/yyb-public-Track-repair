from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import json
import uvicorn
import pandas as pd
import numpy as np
from typing import List

from Analyzer.analysr_data import analyse_data
from Controller.menber import Track, Pageinfo, DeviceData, RequestBody
from Controller.method import convert_to_json_compatible

app = FastAPI()

# 定义一个 API 接口来读取 log 表数据
@app.post("/New_analyse", response_model=RequestBody)
async def receive_data(request_body: RequestBody):
    data = request_body.data
    try:
        # 将 'data' 列表转换为 DataFrame
        df = pd.DataFrame([item.dict() for item in data])
        print(df)

        # 解析 JSON 字符串
        df['deviceStatus'] = df['deviceStatus'].apply(lambda x: json.loads(x))
        df['deviceWarning'] = df['deviceWarning'].apply(lambda x: json.loads(x))

        # 展开 JSON 数据
        device_status_df = df['deviceStatus'].apply(pd.Series)
        device_warning_df = df['deviceWarning'].apply(pd.Series)

        # 合并 DataFrame
        df = pd.concat([df.drop(columns=['deviceStatus', 'deviceWarning']),
                        device_status_df,
                        device_warning_df], axis=1)

        # 清理浮点值
        def clean_float_values(df):
            df.replace([np.inf, -np.inf], np.nan, inplace=True)
            df.fillna('', inplace=True)

        # 应用清理函数
        clean_float_values(df)

        # 数据分析
        result_data = analyse_data(df)

        # 逆处理
        def reconstruct_json_fields(df):
            # 重新构造 deviceStatus JSON 字符串
            device_status_columns = ['LockRodStatus', 'ChargeStatus', 'DeviceSwitchState', 'MotionSensorStatus',
                                     'LinkMode', 'LongitudePosition', 'LatitudePosition', 'NetworkMode',
                                     'LocationModuleStatus', 'SimMode', 'GPSPositionStatus']
            df['deviceStatus'] = df[device_status_columns].apply(lambda row: json.dumps(row.to_dict()), axis=1)

            # 重新构造 deviceWarning JSON 字符串
            device_warning_columns = ['ShellDamageAlarm']
            df['deviceWarning'] = df[device_warning_columns].apply(lambda row: json.dumps(row.to_dict()), axis=1)

            # 删除展开的字段
            df = df.drop(columns=device_status_columns + device_warning_columns)

            return df

        # 使用函数进行逆操作
        result_data = reconstruct_json_fields(result_data)

        # 转换为符合目标格式的 JSON 数据
        result_data_formatted = convert_to_json_compatible(result_data)
        print(result_data_formatted)

        # 返回结果
        return JSONResponse(content={
            "returnCode": "200",
            "returnMsg": None,
            "data": result_data_formatted
        })

    except Exception as e:
        # 返回错误信息
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
