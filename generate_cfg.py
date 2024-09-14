import pandas as pd
import os

# 定义Excel文件路径
file_path = 'merged_data.xlsx'

# 创建保存cfg文件的文件夹
output_dir = '重测cfg文件'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 读取Excel文件中的所有sheets
xls = pd.ExcelFile(file_path)

# 遍历所有sheets
for sheet_name in xls.sheet_names:
    # 读取每个sheet
    df = pd.read_excel(xls, sheet_name)
    
    # 按照机型/OS分组，并获取每个组中的唯一test_name
    grouped = df.groupby('机型/OS')['test_name'].unique()
    
    # 遍历每个机型/OS组合
    for os_name, test_names in grouped.items():
        # 创建cfg文件内容，并填入sheet名作为sold_type
        cfg_content = f"""# toml
[product]
name = "CVM"

[role]
area = ""  # 地域码（zone）缩写，如：gz、sh，腾讯云现网环境能自动获取
sold_type = "{sheet_name}"  # 实例类型（instance_type），填入sheet名
username = "root"  # centos/tlinux一般为root，ubuntu一般为ubuntu
port = 22
password = "Perf@host#2024"

[role.client]
ip = ""

[role.server]
ip = ""

[role.other]
ip = ""

[benchmark]
added_test = [
"""
        # 将test_names转换为字符串形式，并加上前缀"cvm.baseline."
        added_tests = [f'    "cvm.baseline.{test_name}",' for test_name in test_names]
        added_tests_str = '\n'.join(added_tests)  # 将列表转换为字符串，每项后跟换行符
        
        # 添加结束括号
        added_tests_str += '\n]'
        
        # 完成cfg_content字符串
        cfg_content += added_tests_str

        # 创建文件名
        file_name = f"{os_name}_default.cfg"
        file_path = os.path.join(output_dir, file_name)  # 将文件保存到指定的文件夹
        
        # 写入文件
        with open(file_path, 'w') as file:
            file.write(cfg_content)
        
        print(f"文件 {file_path} 已创建。")

# 关闭Excel文件
xls.close()
