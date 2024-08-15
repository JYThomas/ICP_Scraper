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
    result = query_chinaz("www.tsinghua.edu.cn")
    print(result)
    result = query_chinaz("nnsw.nanning.gov.cn")
    print(result)
    result = query_chinaz("www.bilibili.com")
    print(result)
    result = query_chinaz("www.10086.cn")
    print(result)
