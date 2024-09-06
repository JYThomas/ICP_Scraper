import requests as req
import base64
from fake_useragent import UserAgent
import json


def encode_http_response_to_base64(response):
    # 将响应内容编码为bytes类型
    data_to_encode = response.encode('utf-8')
    # 对数据进行Base64加密
    encoded_data = base64.b64encode(data_to_encode)
    # 将加密后的结果解码为字符串格式
    encoded_string = encoded_data.decode('utf-8')
    return encoded_string


def get_recordation_info(domain):
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random
    }

    res_data = {
        "Domain_domain": domain,
        "Recodation_number": "暂无",
        "Recodation_company_name": "暂无",
        "Recodation_company_type": "暂无",
        "Recodation_icp_title": "暂无",
        "Recodation_icp_audit_time": "暂无"

    }

    domain_base64 = encode_http_response_to_base64(domain)
    url = f"https://www.mxnzp.com/api/beian/search?domain={domain_base64}&app_id=qdkj6hndjrpsgnqu&app_secret=FdYFJB5Ck2X102zhxFD8MMjwAa8jbuOY"
    try:
        resp = req.get(url, headers=headers)
        result = resp.json()
        print(result)
        if resp.status_code == 200:
            res_data["Recodation_number"] = result["data"]["icpCode"]
            res_data["Recodation_company_name"] = result["data"]["unit"]
            res_data["Recodation_company_type"] = result["data"]["type"]
            res_data["Recodation_icp_title"] = result["data"]["name"]
            res_data["Recodation_icp_audit_time"] = result["data"]["passTime"]
            return res_data
    except Exception as e:
        return res_data


def save_results(domain, data):
    output_file = f'./results/{domain}_ICP_data.json'
    # 将 JSON 写入文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
        file.write('\n')  # 写入换行符，以便区分每次追加的数据


if __name__ == "__main__":
    # domain = "gxu.edu.cn"
    domain = "www.gxust.edu.cn"
    domain_icp = get_recordation_info(domain)

    save_results(domain, domain_icp)
