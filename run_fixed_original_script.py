def run_fixed_original_script():
    """运行修复后的原始脚本"""

    print("运行修复后的原始make_jsons_fb.py...")
    print("=" * 50)

    try:
        # 直接导入并运行修复后的脚本
        import subprocess
        import sys

        result = subprocess.run([
            sys.executable,
            "C:/Users/lunor/Desktop/yan1/HatePostDetection/make_jsons_fb.py"
        ], capture_output=True, text=True)

        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        print(f"返回码: {result.returncode}")

    except Exception as e:
        print(f"运行出错: {e}")


# 运行修复后的原始脚本
run_fixed_original_script()