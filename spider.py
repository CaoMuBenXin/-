import requests
from bs4 import BeautifulSoup  # python解析html


def get_html(name):
    """
    返回问卷的信息（html）
    :return:
    """
    header = {
        'Cookie': 'browserid=2d031553-1fa1-47d9-8d05-6e878ce3322c; acw_tc=0a47329c17258988543052343e0120130b0d4cd139d3c62bd9f4234564bc0c; .ASPXANONYMOUS=zOA5FWY52wEkAAAAZTBkMWRmZmUtY2E2MC00OTU5LTljN2YtMjAwYmYwNjA1MzYzm2bUBGzG4Sd7TnHm2lUmRb3KlXI1; SERVERID=a3c22b3ae01a340de51e583138c7fc4c|1725898856|1725898854; querycond281180293=10000%7C%u5218%u6',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'

    }
    data = {
        '__VIEWSTATE': '/wEPDwUKLTkwNDc1MTkwOWRkneDfAyyOp+LH7m5xBE+MTvNb4ks=',
        '__VIEWSTATEGENERATOR': 'A51944F2',
        '__EVENTVALIDATION': '/wEdAATvNNUN3wEttQF3VjAPZTfUfxLSikTZqx6XzQUk71djD7A88eHGsukWIJIFOXmn8igR0tAd5ZA4PMHE5c0EdNu8wAYgZbyAmlKl/HlZup85JK6ik2w=',
        'hfPostType': '1',
        'hfQuery': '10000|' + name
    }
    content = requests.post('https://www.wjx.cn/resultquery.aspx?activity=281180293', headers=header, data=data).text
    return content


def get_questionnaire(name):
    soup = BeautifulSoup(
        get_html(name),
        'lxml')
    text = soup.get_text()
    with open('output.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(text)

    # 打开并读取原始文件
    with open("output.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    # 过滤掉空白行
    filtered_lines = [line for line in lines if line.strip()]
    # 将过滤后的行组合成一个字符串
    filtered_text = "".join(filtered_lines[9])
    # 将排序后的文本写入新的文件或覆盖原文件
    with open("questionnaire.txt", "w", encoding="utf-8") as file:
        i = 0
        while filtered_text[i] != '总':
            i += 1
        file.write("GHQ-20 心理问卷\n")  # 输入标题
        while i < len(filtered_text):
            if filtered_text[i] == '*':  # 遇*换行
                file.write('\n')
            file.write(filtered_text[i])
            i += 1


if __name__ == '__main__':
    get_questionnaire("刘毅")
