import xml.etree.ElementTree as ET
import os
import re
from xmlEditor import editXML
from uploader import uploadPorblem
from uploader import uploadData

def clean_folder_name(folder_name):
    # 定义Windows文件系统中不允许的字符
    invalid_chars = r'[\\/*?:"<>|]'
    # 使用正则表达式替换不合法字符为空字符串
    clean_name = re.sub(invalid_chars, '', folder_name)
    return clean_name

def clean_text(text):
    """移除CDATA等标记，只保留文本内容。"""
    return text.replace('<![CDATA[', '').replace(']]>', '').strip() if text else ''

def parseXML(xml_file_path):
    # 解析XML文件
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # 遍历所有题目
    for idx, item in enumerate(root.findall('item'), start=1):
        title = item.find('title').text
        # 生成一个安全的文件夹名称，移除不合法字符
        folder_name = f"{title.replace('[', '').replace(']', '').replace(':', '').replace(' ', '').replace('_','')}"
        folder_name = clean_folder_name(folder_name)
        folder_name = r"res/" + folder_name
        # 在当前目录下创建题目文件夹
        os.makedirs(folder_name, exist_ok=True)

        # 创建Markdown文件并写入题目描述和样例
        with open(os.path.join(folder_name, 'problem.md'), 'w', encoding='utf-8') as md_file:
            # 写入题目描述
            description = clean_text(item.find('description').text)
            description = description.replace("<p>", "").replace("</p>", "\n")
            md_file.write(f"# {title}\n\n## Description\n\n{description}\n\n")

            # 写入样例输入和输出
            sample_inputs = item.findall('sample_input')
            sample_outputs = item.findall('sample_output')
            for i, (inp, out) in enumerate(zip(sample_inputs, sample_outputs), start=1):
                sample_input_content = clean_text(inp.text)
                sample_output_content = clean_text(out.text)
                md_file.write(f"## Sample Input {i}\n\n```\n{sample_input_content}\n```\n\n")
                md_file.write(f"## Sample Output {i}\n\n```\n{sample_output_content}\n```\n\n")

        # 解析并保存测试输入和输出
        for test_input in item.findall('test_input'):
            file_name = test_input.get('filename')
            content = clean_text(test_input.text)
            with open(os.path.join(folder_name, file_name), 'w', encoding='utf-8') as f:
                f.write(content)

        for test_output in item.findall('test_output'):
            file_name = test_output.get('filename')
            content = clean_text(test_output.text)
            with open(os.path.join(folder_name, file_name), 'w', encoding='utf-8') as f:
                f.write(content)

        print(f"题目 '{title}' 的描述和测试用例已保存在 '{folder_name}' 文件夹中。")

def parse():
    data_dir = 'data'  # 请确保这是你的XML文件所在的目录
    file_list = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            full_path = os.path.join(root, file)
            file_list.append(full_path)

    cnt = 0
    for file in file_list:
        parseXML(file)
        # 加载XML文件
        tree = ET.parse(file)
        root = tree.getroot()

        # 遍历所有元素并删除名为test_output和test_input的元素
        for elem in root.findall(".//test_output"):
            elem.clear()  # 清除元素内容但保留元素本身
            # 如果想要完全删除元素，可以使用 parent.remove(elem)
        for elem in root.findall(".//test_input"):
            elem.clear()  # 清除元素内容但保留元素本身
            # 如果想要完全删除元素，可以使用 parent.remove(elem)
        # 保存修改后的XML到一个新文件
        cnt += 1
        tree.write(str(cnt) + ".xml")
        print(str(cnt) + ".xml" + " saved")

if __name__ == '__main__':
    parse()
    uploadPorblem()
    uploadData()
