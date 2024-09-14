import os
import re
import pandas as pd

def extract_os_and_model(filename):
    """根据文件名提取OS和机型信息，并去掉.xlsx扩展名"""
    name_without_ext = filename.replace('.xlsx', '')
    
    # 使用正则表达式匹配文件名中的OS1, 机型, OS2
    match = re.match(r'^(.*?) (.*?)-(.*?) (.*?)$', name_without_ext)
    if match:
        os1 = match.group(1)
        model = match.group(2)
        os2 = match.group(3)
        model2 = match.group(4)
        os_info = f'{os1}/{os2}'  # 组合OS1和OS2
        return os_info, model
    else:
        raise ValueError(f"文件名格式不符合预期: {filename}")

def aggregate_data(base_dir):
    """聚合数据并保存到merged_data.xlsx"""
    # 创建一个Excel writer对象
    output_file = 'merged_data.xlsx'
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    
    # 遍历每个子文件夹
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)
        
        if os.path.isdir(folder_path):
            # 创建一个DataFrame来存放每个子文件夹的数据
            aggregated_df = pd.DataFrame()
            
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.xlsx'):
                    file_path = os.path.join(folder_path, file_name)
                    sheet_name = '合并'
                    
                    # 读取xlsx文件中的'合并' sheet
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                    
                    # 提取OS和机型信息
                    os_info, model_info = extract_os_and_model(file_name)
                    
                    # 添加OS和机型列
                    df['机型'] = model_info
                    df['OS'] = os_info
                    
                    # 将'对比'和'基线'列的数据统一到固定列中
                    df['对比'] = df.iloc[:, 4]  # E列
                    df['基线'] = df.iloc[:, 5]  # F列
                    df = df[['test_name', 'tool_name', 'results_key', 'metric', '对比', '基线', '百分比(单位%)', '机型', 'OS']]
                    
                    # 将当前文件的数据添加到聚合的DataFrame中
                    aggregated_df = pd.concat([aggregated_df, df], ignore_index=True)
            
            # 将聚合后的数据写入Excel中的一个sheet
            aggregated_df.to_excel(writer, sheet_name=folder_name, index=False)
            
            # 自动调整列宽
            worksheet = writer.sheets[folder_name]
            for idx, col in enumerate(aggregated_df.columns):
                series = aggregated_df[col]
                max_len = max(series.astype(str).map(len).max(), len(col))
                worksheet.set_column(idx, idx, max_len)
    
    # 保存Excel文件
    writer.save()
    print(f"数据已成功聚合并保存到 {output_file}")

# 运行脚本
base_directory = 'example_processed'
aggregate_data(base_directory)
