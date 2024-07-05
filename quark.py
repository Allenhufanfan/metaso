import requests
import re

quark_headers = {
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'accept': 'application/json, text/plain, */*',
    'content-type': 'application/json',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'origin': 'https://pan.quark.cn',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://pan.quark.cn/',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9'
}

waliso_headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-length': '147',
    'content-type': 'application/json',
    'origin': 'https://waliso.com',
    'priority': 'u=1, i',
    'referer': 'https://waliso.com/',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

kkkob_headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-length': '68',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'origin': 'http://z.kkkob.com',
    'referer': 'http://z.kkkob.com/app/',
    'Proxy-Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest'
}

class QURAK:
    def get_id_from_url(self, url):
        url = url.replace("https://pan.quark.cn/s/", "")
        pattern = r"(\w+)(#/list/share.*/(\w+))?"
        match = re.search(pattern, url)
        if match:
            pwd_id = match.group(1)
            if match.group(2):
                pdir_fid = match.group(3)
            else:
                pdir_fid = 0
            return pwd_id, pdir_fid
        else:
            return None

    # 可验证资源是否失效
    def get_stoken(self, pwd_id):
        url = "https://drive-m.quark.cn/1/clouddrive/share/sharepage/token"
        querystring = {"pr": "ucpro", "fr": "h5"}
        payload = {"pwd_id": pwd_id, "passcode": ""}
        response = requests.request(
            "POST", url, json=payload, headers=quark_headers, params=querystring
        ).json()
        if response.get("data"):
            return True, response["data"]["stoken"]
        else:
            return False, response["message"]

    # 查询资源1
    def get_qry_external(self, qry_key: str):
        url = f"http://www.662688.xyz/api/get_zy"
        params = {
            "keyword": qry_key,
        }
        items_json = []
        msg = '外部资源1查询结果：\n'
        try:
            response = requests.get(url, params=params, timeout=1)
            # 检查请求是否成功
            if response.status_code == 200:
                # 解析返回的JSON数据
                data = response.json()
                # 打印返回的数据，或者进行其他处理

                i = 1
                if data.get("data"):
                    first_three_items = data['data']
                    # 打印结果
                    for item in first_three_items:
                        item_str = str(item)  # 将item转换为字符串
                        if 'quark' in item_str and i <=5:
                            # 判断夸克资源是否失效
                            pwd_id, pdir_fid = self.get_id_from_url(item['url'])
                            is_sharing, stoken = self.get_stoken(pwd_id)
                            if is_sharing:
                                # msg += str(i) + '.' + f"{item['title']}\n{item['url']}\n"
                                # 创建一个字典，包含标题和URL
                                item_dict = {
                                    'title': item['title'],
                                    'url': item['url']
                                }
                                # 将字典添加到列表中
                                items_json.append(item_dict)
                                i += 1
                else:
                    msg += '未查询到数据1'
            else:
                msg += '查询请求失败1'
        except Exception:
            msg += f"查询请求失败1"

        return items_json

    # 查询资源2
    def get_qry_external_2(self, qry_key: str):
        url = f"https://www.hhlqilongzhu.cn/api/ziyuan_nanfeng.php"
        params = {
            "keysearch": qry_key,
        }
        items_json = []
        msg = '外部资源2查询结果：\n'

        try:
            response = requests.get(url, params=params, timeout=1)
            # 检查请求是否成功
            if response.status_code == 200:
                # 解析返回的JSON数据
                data = response.json()

                i = 1
                if data.get("data"):
                    first_three_items = data['data']
                    # 打印结果
                    for item in first_three_items:
                        item_str = str(item)  # 将item转换为字符串
                        if 'quark' in item_str and i <=5:
                            url = item['data_url'].split("链接：")[1]
                            title = item['title']
                            # 判断夸克资源是否失效
                            pwd_id, pdir_fid = self.get_id_from_url(url)
                            is_sharing, stoken = self.get_stoken(pwd_id)
                            if is_sharing:
                                # msg += str(i) + '.' + f"{item['title']}\r\n{url}\n"
                                # 创建一个字典，包含标题和URL
                                item_dict = {
                                    'title': title,
                                    'url': url
                                }
                                # 将字典添加到列表中
                                items_json.append(item_dict)
                                i += 1
                else:
                    msg += '未查询到数据2'
                    print(msg)
            else:
                msg += '查询请求失败2'
                print(msg)
        except Exception:
            msg += f"查询请求失败2"
            print(msg)

        return items_json

    # 查询资源3
    def get_qry_external_3(self, qry_key: str):
        url = f"https://v.funletu.com/search"
        headers = quark_headers.copy()
        headers['origin'] = 'https://pan.funletu.com'
        headers['referer'] = 'https://pan.funletu.com/'
        params = {
                    "style": "get",
                    "datasrc": "search",
                    "query": {
                        "id": "",
                        "datetime": "",
                        "commonid": 1,
                        "parmid": "",
                        "fileid": "",
                        "reportid": "",
                        "validid": "",
                        "searchtext": qry_key
                    },
                    "page": {
                        "pageSize": 10,
                        "pageIndex": 1
                    },
                    "order": {
                        "prop": "id",
                        "order": "desc"
                    },
                    "message": "请求资源列表数据"
                }

        msg = '外部资源3查询结果：\n'
        result_json = []
        try:
            response = requests.post(url, json=params, headers=headers, timeout=1).json()
            print(response)

            # 检查请求是否成功
            if response['status'] == 200:  # 假设0表示成功
                i = 1
                if response['data']:
                    first_three_items = response['data']
                    # 打印结果
                    for item in first_three_items:
                        item_str = str(item)  # 将item转换为字符串
                        if 'quark' in item_str and i <= 5:
                            url = item['url'].replace("?entry=funletu", "", 1)
                            title = item['title']
                            # 判断夸克资源是否失效
                            pwd_id, pdir_fid = self.get_id_from_url(url)
                            is_sharing, stoken = self.get_stoken(pwd_id)
                            if is_sharing:
                                # msg += str(i) + '.' + f"{item['title']}\r\n{url}\n"
                                item_dict = {
                                    'url': url,
                                    'title': title
                                }
                                # 将字典添加到列表中
                                result_json.append(item_dict)
                                i += 1
                else:
                    msg += '未查询到数据3'
                    print(msg)
            else:
                msg += '查询请求失败3'
                print(msg)
        except Exception:
            msg += f"查询请求失败3"
            print(msg)

        return result_json
        
    def get_qry_external_4(self, qry_key: str):
        url = f"https://waliso.com/v1/search/disk"
        headers = waliso_headers.copy()

        params = {
            "page": 1,
            "q": qry_key,
            "user": "",
            "exact": False,
            "format": [],
            "share_time": "",
            "size": 15,
            "type": "QUARK",
            "exclude_user": [],
            "adv_params": {"wechat_pwd": ""}
        }

        # #'cookie': '__51vcke__KNUJ62lGWze5GQwe=51c08e0f-69ea-5749-b9da-0a27db45c2ac; __51vuft__KNUJ62lGWze5GQwe=1718687797904; __51uvsct__KNUJ62lGWze5GQwe=3; __vtins__KNUJ62lGWze5GQwe=%7B%22sid%22%3A%20%2281484f27-f13d-5b94-914c-0f96c5f4d0a3%22%2C%20%22vd%22%3A%209%2C%20%22stt%22%3A%202410845%2C%20%22dr%22%3A%20246699%2C%20%22expires%22%3A%201718766484958%2C%20%22ct%22%3A%201718764684958%7D',
        # cookies = {
        #     "__51uvsct__KNUJ62lGWze5GQwe": "3",
        #     "__51vcke__KNUJ62lGWze5GQwe": "51c08e0f-69ea-5749-b9da-0a27db45c2ac",
        #     "__51vuft__KNUJ62lGWze5GQwe": "1718687797904",
        #     "__vtins__KNUJ62lGWze5GQwe": "%7B%22sid%22%3A%20%22a0c52b82-7502-59e3-b8a2-e7c3b2a54ce5%22%2C%20%22vd%22%3A%205%2C%20%22stt%22%3A%201506417%2C%20%22dr%22%3A%201198935%2C%20%22expires%22%3A%201718776704319%2C%20%22ct%22%3A%201718774904319%7D"
        # }
        msg = '外部资源4查询结果：\n'
        result_json = []
        try:
            response = requests.post(url, json=params, headers=headers, timeout=1).json()
            print(response)

            # # 检查请求是否成功
            if response['code'] == 200:  # 假设0表示成功
                i = 1
                if response['data']:
                    first_three_items = response['data']['list']
                    # 打印结果
                    for item in first_three_items:
                        item_str = str(item)  # 将item转换为字符串
                        if 'quark' in item_str and i <= 5:
                            title = item['disk_name'].replace("<em>", "", 1).replace("</em>", "", 1)
                            url = item['link']
                            # 判断夸克资源是否失效
                            pwd_id, pdir_fid = self.get_id_from_url(url)
                            is_sharing, stoken = self.get_stoken(pwd_id)
                            if is_sharing:
                                # msg += str(i) + '.' + f"{title}\r\n{url}\n"

                                # 创建一个字典，包含标题和URL
                                item_dict = {
                                    'title': title,
                                    'url': url
                                }
                                # 将字典添加到列表中
                                result_json.append(item_dict)
                                i += 1
                else:
                    msg += '未查询到数据'
            else:
                msg += '查询请求失败'
        except Exception as e:
            msg += f"查询请求失败" + str(e)

        return result_json

    def get_qry_external_5(self, qry_key: str):
        url = f"https://api.cloudpan.cn/index/search"
        headers = quark_headers.copy()
        headers['origin'] = 'https://cloudpan.cn'
        headers['referer'] = 'https://cloudpan.cn/'
        params = {"page": 1, "pageSize": 20, "searchText": qry_key, "fileType": 0}

        result_json = []
        msg = '外部资源5查询结果：\n'

        try:
            response = requests.post(url, json=params, headers=headers, timeout=1).json()
            print(response)

            # 检查请求是否成功
            if response['code'] == 200:  # 假设0表示成功
                i = 1
                if response['data']:
                    first_three_items = response['data']['records']
                    # 打印结果
                    for item in first_three_items:
                        item_str = str(item)  # 将item转换为字符串
                        if i <= 5:
                            title = item['title']
                            url = 'https://pan.quark.cn/s/' + item['shareUrl']
                            # 判断夸克资源是否失效
                            pwd_id, pdir_fid = self.get_id_from_url(url)
                            is_sharing, stoken = self.get_stoken(pwd_id)
                            if is_sharing:
                                # msg += str(i) + '.' + f"{title}\r\n{url}\n"
                                item_dict = {
                                    'url': url,
                                    'title': title.encode('utf-8').decode('utf-8')
                                }
                                # 将字典添加到列表中
                                result_json.append(item_dict)
                                i += 1
                else:
                    msg += '未查询到数据'
            else:
                msg += '查询请求失败'
        except Exception:
            msg += f"查询请求失败"

        return result_json

    def get_kkkob_token(self):
        try:
            url = 'http://z.kkkob.com/v/api/getToken'
            # 使用 requests 获取网页内容
            response = requests.get(url)
            if response.status_code == 200:
                return response.json().get('token')
        except Exception as e:
            print(e)
        return ''

    def get_kkkob_result(self, qry: str, url: str, token: str):
        result_json = []
        msg = '查询结果kk：\n'
        try:
            headers = kkkob_headers.copy()
            params = {"name": qry, "token": token}
            response = requests.post(url, data=params, headers=headers, timeout=1)
            # print(response)
            # 检查请求是否成功
            if response.status_code == 200:
                response = response.json()
                i = 1
                if response['list']:
                    first_three_items = response['list']
                    # 打印结果
                    for item in first_three_items:
                        item_str = str(item)  # 将item转换为字符串
                        if 'quark' in item_str and i <= 3:
                            title = item['question']

                            # 正则表达式，用于匹配以https://开头，包含pan.quark.cn的链接
                            pattern = r'https?://pan\.quark\.cn/[^ ]+'

                            # 使用re.search查找匹配的链接
                            match = re.search(pattern, item['answer'])
                            url = match.group(0)
                            # url = item['answer'].replace(title + "链接：", "", 1)
                            # 判断夸克资源是否失效
                            pwd_id, pdir_fid = self.get_id_from_url(url)
                            is_sharing, stoken = self.get_stoken(pwd_id)
                            if is_sharing:
                                # msg += str(i) + '.' + f"{item['title']}\r\n{url}\n"
                                item_dict = {
                                    'url': url,
                                    'title': title
                                }
                                # 将字典添加到列表中
                                result_json.append(item_dict)
                                i += 1
                else:
                    msg += '未查询到数据kk'
            else:
                msg += '查询请求失败kk'
        except Exception as e:
            print(e)
        return result_json

    def qry_kkkob(self, qry: str):

        result_json = []

        # 获取token
        token = self.get_kkkob_token()
        if token == '':
            return result_json

        result_json += self.get_kkkob_result(qry, 'http://z.kkkob.com/v/api/getJuzi', token)
        result_json += self.get_kkkob_result(qry, 'http://z.kkkob.com/v/api/search', token)
        result_json += self.get_kkkob_result(qry, 'http://z.kkkob.com/v/api/getDJ', token)
        result_json += self.get_kkkob_result(qry, 'http://z.kkkob.com/v/api/getXiaoyu', token)
        result_json += self.get_kkkob_result(qry, 'http://z.kkkob.com/v/api/getSearchX', token)

        return result_json