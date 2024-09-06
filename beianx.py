import requests as req
from bs4 import BeautifulSoup
import tldextract


def getICPInfo(domain):
    # 这个网站要提取主域作为搜索目标
    tld_domain = tldextract.extract(domain).registered_domain
    print(tld_domain)

    url = f"https://www.beianx.cn/search/{tld_domain}"

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'acw_tc=0a47314617255443759717779e0032b39314c39b139e9dae39e0590c040f55; .AspNetCore.Antiforgery.OGq99nrNx5I=CfDJ8OsC2ZLMIq9Ks_KNSEOc-tabJDDYULiEw52MDpJhqjvh-5UEBGfdK-K3lZVn6q89G2JlXXrIG-BylBmFxhUpukO9SSLNfHNVG1zgRH67SSwakcoHgTgehtdWXCMIAcSlUUsRLTbY9w807dJL9JUEKHQ; __51uvsct__JfvlrnUmvss1wiTZ=1; __51vcke__JfvlrnUmvss1wiTZ=4228d3c4-2b99-55cb-a559-bd8b2e219743; __51vuft__JfvlrnUmvss1wiTZ=1725544376313; machine_str=5412e533-5fc5-4a6b-917d-83a951c8125c; __vtins__JfvlrnUmvss1wiTZ=%7B%22sid%22%3A%20%224fe03f40-9fd2-539f-bfd3-891c685d8bef%22%2C%20%22vd%22%3A%206%2C%20%22stt%22%3A%20295753%2C%20%22dr%22%3A%201073%2C%20%22expires%22%3A%201725546472063%2C%20%22ct%22%3A%201725544672063%7D',
        'Referer': 'https://www.beianx.cn/search',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    try:
        resp = req.get(url, headers=headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # 提取表格行
            table_rows = soup.find_all('tr')[1:]  # 跳过标题行

            # 定义字典结构
            table_data = []

            # 遍历每一行并提取数据
            for row in table_rows:
                cols = row.find_all('td')
                table_data.append({
                    "domain": domain,
                    "department": cols[1].text.strip(),
                    "department_type": cols[2].text.strip(),
                    "ICPNumber": cols[3].text.strip(),
                    "ip_location": ""
                })

        if not table_data:
            result = {
                "domain": domain,
                "department": "暂无",
                "department_type": "暂无",
                "ICPNumber": "暂无",
                "ip_location": ""
            }
            return result

        return table_data[0]

    except Exception as e:
        print(e)
        result = {
            "domain": domain,
            "department": "暂无",
            "department_type": "暂无",
            "ICPNumber": "暂无",
            "ip_location": ""
        }
        return result


if __name__ == "__main__":
    result = getICPInfo("www.gxust.edu.cn")
    print(result)
