import os
import pandas as pd
import py7zr

#脚本放到数据文件夹的目录下
root_directory = os.path.dirname(os.path.abspath(__file__))
output_base_dir = os.path.join(root_directory, 'example_processed')

def process_files_in_dir(directory, output_directory):

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    file_count = 0
    total_files = len([f for f in os.listdir(directory) if f.endswith('.xlsx')])
    print(f"Processing files in {directory}, total {total_files} files...")

    # 遍历目录下的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.xlsx'):
            filepath = os.path.join(directory, filename)
            
            try:
                df = pd.read_excel(filepath)

                #去除空数据
                df.dropna(inplace=True)

                # '百分比(单位%)' 列转换为浮点数
                if '百分比(单位%)' in df.columns:
                    df['百分比(单位%)'] = df['百分比(单位%)'].str.rstrip('%').astype('float') / 100
                    df = df[(df['百分比(单位%)'] < -0.05) | (df['百分比(单位%)'] > 0.05)]
                    df['百分比(单位%)'] = df['百分比(单位%)'].apply(lambda x: f'{x*100}%')

                # 小优
                small_advantage_df = df[df['metric'].str.contains('单位: ns|单位: second|单位: N/A|单位: μs|单位: ms')]
                small_advantage_df = small_advantage_df[small_advantage_df['百分比(单位%)'].str.rstrip('%').astype('float') <= 0]

                # 大优
                large_advantage_df = df[~df['metric'].str.contains('单位: ns|单位: second|单位: N/A|单位: μs|单位: ms')]
                large_advantage_df = large_advantage_df[large_advantage_df['百分比(单位%)'].str.rstrip('%').astype('float') >= 0]

                #合并
                combined_df = pd.concat([small_advantage_df, large_advantage_df], ignore_index=True)

                # 写入
                with pd.ExcelWriter(os.path.join(output_directory, filename)) as writer:
                    small_advantage_df.to_excel(writer, sheet_name='小优', index=False)
                    large_advantage_df.to_excel(writer, sheet_name='大优', index=False)
                    combined_df.to_excel(writer, sheet_name='合并', index=False)  

                file_count += 1
                print(f"Processed: {filename} ({file_count}/{total_files})")

            except Exception as e:
                error_message = f"Error processing file {filename}:\n{str(e)}"
                print(error_message)
                with open(os.path.join(output_base_dir, "error_log.txt"), 'a') as log_file: 
                    log_file.write(f"{filename}: {error_message}\n")
                continue

def process_directories_in_root(root_dir):
    for dir_name in os.listdir(root_dir):
        dir_path = os.path.join(root_dir, dir_name)
        
        if os.path.isdir(dir_path):  
            output_directory = os.path.join(output_base_dir, dir_name)
            process_files_in_dir(dir_path, output_directory)

def compress_directory_to_7z(directory, output_filename):
    with py7zr.SevenZipFile(output_filename, 'w') as archive:
        archive.writeall(directory, 'example_processed')


if __name__ == "__main__":
    process_directories_in_root(root_directory)

    #output_7z_file = os.path.join(root_directory, 'example_processed.7z')
    #compress_directory_to_7z(output_base_dir, output_7z_file)
    #print(f"Compression complete: {output_7z_file}")