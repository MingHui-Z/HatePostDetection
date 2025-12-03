def verify_fix():
    """验证修复是否成功"""

    # 检查处理后的文件
    output_file = "C:/Users/lunor/Desktop/yan1/HatePostDetection/datasets/FB/files/processed_test.json"

    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            processed_data = json.load(f)

        print(f"处理后的文件包含 {len(processed_data)} 条记录")
        print("前3条处理后的数据:")
        for i, item in enumerate(processed_data[:3]):
            print(f"{i + 1}: {item}")

        # 检查关键字段是否存在
        if processed_data:
            first_item = processed_data[0]
            required_fields = ['img', 'text', 'label', 'id']
            missing_fields = [field for field in required_fields if field not in first_item]

            if not missing_fields:
                print("✓ 所有必需字段都存在")
            else:
                print(f"✗ 缺少字段: {missing_fields}")
    else:
        print("处理后的文件尚未生成")


verify_fix()