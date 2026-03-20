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
        # 复制源文件到目标文件（实际项目中可能需要翻译，这里暂时复制）
        shutil.copy2(source_file, target_file)
        print(f"✓ 更新: {target_file}")
    else:
        print(f"✗ 源文件不存在: {source_file}")

def check_and_update_translations(base_dir, subfolders):
    """检查并更新翻译文件"""
    for folder in subfolders:
        folder_path = os.path.join(base_dir, folder)
        if not os.path.exists(folder_path):
            print(f"⚠ 文件夹不存在: {folder_path}")
            continue
        
        print(f"\n处理文件夹: {folder}")
        print("-" * 40)
        
        # 递归遍历文件夹
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file == "SKILL.md" or file == "README.md":
                    source_file = os.path.join(root, file)
                    target_file = os.path.join(root, file.replace(".md", "_CN.md"))
                    
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
    subfolders = [
        "anthropics-skills",
        "claude-scientific-skills",
        "composiohq-awesome-claude-skills",
        "huggingface-skills",
        "obsidian-skills",
        "openai-skills",
        "ui-ux-pro-max-skills",
        "vercel-labs-agent-skills",
        "vercel-labs-skills"
    ]
    
    check_and_update_translations(base_dir, subfolders)
    print("\n翻译文件检查完成！")

if __name__ == "__main__":
    main()
