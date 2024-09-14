import subprocess

def run_script(script_path):
    """运行一个Python脚本"""
    try:
        # 使用subprocess.run来执行脚本，check=True会在子进程退出时引发CalledProcessError异常
        result = subprocess.run(['python', script_path], check=True)
        print(f"Script {script_path} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute {script_path}: {e}")

def main():
    script1 = 'unit_bank.py'
    script2 = 'pack_up.py'
    # script3 = 'E:\\CVMstorage\\showcase\\api_answer_single.py'
    script4 = 'generate_cfg.py'

    print("开始筛选问题数据...")
    run_script(script1)

    print("筛选完成！数据打包中...")
    run_script(script2)

    #print("打包完成，请查看压缩包；问题数据正在向AI提单...")
    #run_script(script3)

    #print("数据打包完成！开始生成cfg文件...")
    #run_script(script4)
    #print("cfg文件生成完成！请查看文件夹。")

if __name__ == '__main__':
    main()