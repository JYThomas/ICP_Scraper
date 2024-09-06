import requests as req
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs4


# 爬取Chinaz的SEO综合查询信息
def query_chinaz(domain):
    url = f"https://seo.chinaz.com/{domain}"
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random
    }

    try:
        resp = req.get(url, headers=headers)
        if resp.status_code == 200:
            result = get_data(resp.text)
            return result

    except Exception as e:
        print(e)


# 获取icp备案号
def get_ICPNumber(domain):
    url = f"https://icp.chinaz.com/index/api/queryPermit"
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'cookie': 'cz_statistics_visitor=bde7196a-8a5d-4143-61f3-425596f9eac1; HMACCOUNT=8E13A9A559359C69; qHistory=Ly9pY3AuY2hpbmF6LmNvbS93d3cuZ3h1c3QuZWR1LmNuX+e9keermeWkh+ahiOafpeivog==; Hm_lvt_ca96c3507ee04e182fb6d097cb2a1a4c=1723623453,1725541986; Hm_lpvt_ca96c3507ee04e182fb6d097cb2a1a4c=1725541986; Hm_lvt_32e161892d770dca4a9d436a5764a01a=1725541986; Hm_lpvt_32e161892d770dca4a9d436a5764a01a=1725541986; _clck=n2xwl8%7C2%7Cfox%7C0%7C1687; _clsk=iz77x5%7C1725541987765%7C1%7C1%7Ct.clarity.ms%2Fcollect; JSESSIONID=1C80D90ECE0A4894D1DB1C873DA5D5DF',
        'key': '482,896,846,2109',
        'origin': 'https://icp.chinaz.com',
        'priority': 'u=1, i',
        'rd': '482',
        'referer': 'https://icp.chinaz.com/gxust.edu.cn',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'token': '0a9de165ee93259c1ce72d44e2fc591b',
        'ts': '1725541998465',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    payload = {
        "keyword": "gxust.edu.cn"
    }
    try:
        resp = req.post(url, json=payload, headers=headers)
        print(resp.status_code)
        if resp.status_code == 200:
            print(resp.json())
    except Exception as e:
        print(e)


# 获取HTML内容中的域名备案信息、所属单位等内容
def get_data(html):
    # 解析 HTML 文档
    soup = bs4(html, 'lxml')
    try:
        # 查找所有 class 为 color-63 的 <i> 元素
        color_63_is = soup.find_all('i', class_='color-63')
        all_texts = [i.get_text(strip=True) for i in color_63_is]

        if len(all_texts) == 8:
            # 域名所属单位
            department = all_texts[1]
            # 域名所属单位类型
            department_type = all_texts[2]

        else:
            # 域名所属单位
            department = all_texts[4]
            # 域名所属单位类型
            department_type = all_texts[5]
    except Exception as e:
        print(e)
        # 域名所属单位
        department = "暂无"
        # 域名所属单位类型
        department_type = "暂无"

    try:
        # IP地址 运营商
        # <i class="color-63"><a href="//ip.tool.chinaz.com/?ip=202.103.240.11" target="_blank">202.103.240.11[中国广西南宁 电信]</a></i>
        if color_63_is[-4]:
            ip_location = str(color_63_is[-4]).split(
                "</a>")[0].split('"_blank">')[1].split("[")[1].split("]")[0]
        else:
            ip_location = ""
    except Exception as e:
        ip_location = "暂无"

    try:
        span_color_2f87c1 = soup.find_all('i', class_='color-2f87c1')
        # <i class="color-2f87c1"><a href="//icp.chinaz.com/nnsw.nanning.gov.cn" target="_blank">桂ICP备18008337号</a></i>
        ICPNumber = str(span_color_2f87c1[1]).split(
            "</a>")[0].split('"_blank">')[1]
    except Exception as e:
        ICPNumber = "暂无"

    result = {
        "department": department,
        "department_type": department_type,
        "ip_location": ip_location,
        "ICPNumber": ICPNumber,
    }

    return result


if __name__ == "__main__":
    # result = query_chinaz("www.tsinghua.edu.cn")
    # print(result)
    # result = query_chinaz("nnsw.nanning.gov.cn")
    # print(result)
    # result = query_chinaz("www.bilibili.com")
    # print(result)
    result = get_ICPNumber("www.10086.cn")
    print(result)
