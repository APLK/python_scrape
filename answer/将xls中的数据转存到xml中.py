import xlrd
import json
from lxml import etree


def read_exl(file_name):
    exl = xlrd.open_workbook(file_name)
    exl_sheet = exl.sheet_by_name('student')
    data = {}
    for i in range(exl_sheet.nrows):
        # print(exl_sheet.row_values(i)[0])
        # print(exl_sheet.row_values(i)[1:])
        data[exl_sheet.row_values(i)[0]] = exl_sheet.row_values(i)[1:]
    return json.dumps(data,ensure_ascii=False) #转为json对象

def save_to_xml(data, new_file_name):
    root = etree.Element('root')
    students = etree.SubElement(root, 'students')
    # 注释
    students.append(etree.Comment(u"""学生信息表 "id" : [名字, 数学, 语文, 英文]"""))
    students.text = data

    student_xml = etree.ElementTree(root)#节点结束点
    student_xml.write(new_file_name, pretty_print=True, xml_declaration=True, encoding='utf-8')


if __name__ == '__main__':
    content = read_exl('E:/python_demo/hello/answer/student.xlsx')
    print(json.loads(content))
    save_to_xml(content, 'student.xml')
    # print(1--1)