import os
import shutil
from datetime import time
from time import sleep
import re
import requests
from bs4 import BeautifulSoup
from jupyter_core.version import pattern
from requests_toolbelt import MultipartEncoder


cookies = {
    'sid': 'cNnFKCsAlKCr2bMssTewJTG9KEulkNaZ',
    'sid.sig': 'eYtbmHTMgZ-3T6II2Xh9iRz3AVQ'
}

def uploadPorblem():
    # 请求的URL
    url = 'http://xxx.com/d/usaco/problem/import/fps'       # TODO : 使用你的 url

    # 循环上传文件
    for i in range(1, 23 + 1):  # 从1.xml到23.xml
        filename = f'{i}.xml'  # 构建文件名
        files = {'file': (filename, open(filename, 'rb'), 'text/xml')}  # 准备文件信息
        response = requests.post(url, files=files, cookies=cookies)  # 发送带有cookie的POST请求
        print(f'上传文件 {filename} 的响应:', response.status_code)  # 打印每个文件的上传响应


def uploadData():
    global file_path
    for i in range(642,738 + 1):
        # 首先获取题目名称，然后到文件夹找到对应的题目
        problemUrl = 'https://xxx.com/d/usaco/p/' + str(i)       # TODO : 使用你的 url

        # 发送GET请求
        response = requests.get(problemUrl, cookies=cookies)
        # HTML内容
        html_content = response.text
        # print(html_content)
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html_content, 'lxml')
        # 从<title>标签中提取题目
        title_tag = soup.find('title')
        title_text = title_tag.get_text()
        # 从标题中提取特定部分
        problem_title = title_text.split(' - ')[1] if ' - ' in title_text else title_text
        problem_title = problem_title.replace(' ','').replace('[','').replace(']','').replace('/','').replace('?','').replace(':','')

        print(problem_title)
        # 文件夹路径
        folder_path = 'res/' + problem_title
        fileUrl = "https://xxx.com/d/usaco/p/" + str(i) + "/files"
        # 遍历文件夹中的文件
        for filename in os.listdir(folder_path):
            new_file = os.path.join(folder_path, filename)
            new_name = filename
            # 排除problem.md文件
            if filename == 'problem.md':
                continue
            match = re.match(r'.*\.(\d+)\.in$', filename)
            if match:
                # 提取数字部分，例如从'plumb.1.in'中提取'1'
                new_name = match.group(1) + '.in'
                # 构建原文件和新文件的完整路径
                old_file = os.path.join(folder_path, filename)
                new_file = os.path.join(folder_path, new_name)
                # 重命名文件
                if not os.path.exists(new_file):
                    os.rename(old_file, new_file)
                else:
                    print(f"文件 {new_file} 已存在，跳过重命名。")
                file_path = new_file

            match = re.match(r'.*\.(\d+)\.out$', filename)
            if match:
                # 提取数字部分，例如从'plumb.1.out'中提取'1'
                new_name = match.group(1) + '.out'
                # 构建原文件和新文件的完整路径
                old_file = os.path.join(folder_path, filename)
                new_file = os.path.join(folder_path, new_name)
                # 重命名文件
                if not os.path.exists(new_file):
                    os.rename(old_file, new_file)
                else:
                    print(f"文件 {new_file} 已存在，跳过重命名。注意这部分数据可能需要手动处理")

            file_path = new_file

            # 构建multipart/form-data的body内容
            multipart_form_data = {
                'filename': (new_name),
                'file': (new_name, open(file_path, 'rb'), 'application/octet-stream'),
                'type': ('', 'testdata'),
                'operation': ('', 'upload_file')
            }

            retry = 3  # 设置重试次数
            for _ in range(retry):
                try:
                    # 发送POST请求，需要在headers中设置正确的Content-Type
                    response = requests.post(fileUrl, files=multipart_form_data,cookies=cookies)
                    # 检查响应
                    if response.status_code == 200:
                        # print(f"文件 {new_name} 上传成功。")
                        break  # 成功后退出循环
                    elif response.status_code == 502:
                        sleep(3)
                        print("遇到502错误，正在重试...")
                        continue  # 遇到502错误时，继续下一次循环重试
                    else:
                        print(f"文件 {filename} 上传失败，状态码：{response.status_code}")
                        break  # 遇到其他错误，退出循环
                except Exception as e:
                    print(f"请求过程中发生异常：{e}")
                    break  # 发生异常，退出循环
