# from clickhouse_driver import Client
import mysql.connector
import numpy as np

'''
    clickhouse连接
'''
# 设置 ClickHouse 服务器连接信息
host = ''
port = 
username = ''
password = ''
database = ''

# 创建一个 ClickHouse 客户端对象
# client = Client(host=host, port=port, user=username, password=password, database=database)

'''
    mysql连接
'''
def get_db_public_portal_conn():
    connection = mysql.connector.connect(
        host='',
        port=,
        user='root',
        password='',
        database=''
    )

    return connection

# 创建连接
pubportal_conn = get_db_public_portal_conn()
pubportal_db = pubportal_conn.cursor()

'''
    接口处理
'''
def get_company_id(access_key_id: str):
    try:
        company_id_query = r"select id,access_key_id from sys_company where access_key_id = '{access_key_id}';".format(access_key_id=access_key_id)

        pubportal_db.execute(company_id_query)
        company_data = pubportal_db.fetchall()

        # 获取company_id
        company_id = [row[0] for row in company_data][0]

        return company_id
    except Exception as e:
        print(e)





def convert_to_json_compatible(data):
    """
    Convert DataFrame to JSON-compatible format, replacing NaN and Inf with None.
    """
    def handle_float(value):
        if isinstance(value, float):
            if np.isnan(value) or np.isinf(value):
                return ""
        return value

    return data.map(handle_float).to_dict(orient='records')
