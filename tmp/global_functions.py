import xml.etree.ElementTree


def parse_xml_str(file_name, xml_str):
    # 将response生成xml文件
    file_name = 'GlobalSpecies.xml'
    f = open(file_name, 'w')
    f.truncate()
    f.write(xml_str)
    f.write('\n')
    f.close()

    # 读取xml
    root = xml.etree.ElementTree.parse(file_name)
    return root