import xml.etree.ElementTree as ET

def remove_elements(tree, tag):
    root = tree.getroot()
    for element in tree.findall(".//{}".format(tag)):
        if element == root:
            parent = None
        else :
            parent = element.getparent()
        if parent is not None:
            parent.remove(element)

def remove_test_elements(xml_file):
    # 解析XML数据
    root = ET.fromstring(xml_data)

    # 查找所有test_input和test_output元素并删除它们
    for test_case in root.findall('test_case'):
        for elem in test_case:
            if elem.tag in ['test_input', 'test_output']:
                test_case.remove(elem)

    # 将修改后的XML数据转换回字符串
    updated_xml_data = ET.tostring(root, encoding='unicode')

    updated_xml_data

def editXML(file):
    remove_test_elements(file)
