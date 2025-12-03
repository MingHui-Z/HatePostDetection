import os

# 创建符号链接，让fb指向FB
if not os.path.exists("datasets/fb"):
    os.symlink("FB", "datasets/fb")
    print("✓ 已创建符号链接: datasets/fb -> datasets/FB")