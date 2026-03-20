import os
import hashlib
import shutil

def get_file_hash(filepath):
    """计算文件的MD5哈希值"""
    if not os.path.exists(filepath):
        return None
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def update_translation_file(source_file, target_file):
    """更新翻译文件"""
    if os.path.exists(source_file):
        # 确保目标目录存在
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        # 复制源文件到目标文件（实际项目中可能需要翻译，这里暂时复制）
        shutil.copy2(source_file, target_file)
        print(f"✓ 更新: {target_file}")
    else:
        print(f"✗ 源文件不存在: {source_file}")

def check_and_update_openclaw_translations(base_dir):
    """检查并更新awesome-openclaw-skills的翻译文件"""
    source_dir = os.path.join(base_dir, "awesome-openclaw-skills", "categories")
    target_dir = os.path.join(base_dir, "awesome-openclaw-skills", "categories_cn")
    
    if not os.path.exists(source_dir):
        print(f"⚠ 源目录不存在: {source_dir}")
        return
    
    print(f"处理目录: {source_dir}")
    print("-" * 40)
    
    # 遍历源目录中的文件
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".md"):
                source_file = os.path.join(root, file)
                # 计算相对路径
                rel_path = os.path.relpath(source_file, source_dir)
                target_file = os.path.join(target_dir, rel_path)
                
                # 检查文件是否需要更新
                source_hash = get_file_hash(source_file)
                target_hash = get_file_hash(target_file)
                
                if source_hash != target_hash:
                    print(f"需要更新: {source_file} → {target_file}")
                    update_translation_file(source_file, target_file)
                else:
                    print(f"✓ 已同步: {source_file}")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    check_and_update_openclaw_translations(base_dir)
    print("\nOpenClaw翻译文件检查完成！")

if __name__ == "__main__":
    main()
