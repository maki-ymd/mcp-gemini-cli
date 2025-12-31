#!/usr/bin/env python3
"""Windows環境でのmcp-gemini-cliビルドエラー修正パッチ"""
import json
import subprocess
import sys
from pathlib import Path

def main():
    print("修正中...")
    
    # package.json修正
    pkg_path = Path("package.json")
    with open(pkg_path, "r", encoding="utf-8") as f:
        pkg = json.load(f)
    
    pkg["scripts"]["build"] = "rm -rf dist && bun build --target=node --outdir=dist --sourcemap index.ts"
    
    with open(pkg_path, "w", encoding="utf-8") as f:
        json.dump(pkg, f, indent=2, ensure_ascii=False)
    
    print("package.json 修正完了")
    
    # ビルド実行
    print("ビルド中...")
    result = subprocess.run(["bun", "run", "build"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ビルド失敗:\n{result.stderr}")
        sys.exit(1)
    
    print("ビルド成功")
    
    # shebang追加
    dist_index = Path("dist/index.js")
    content = dist_index.read_text(encoding="utf-8")
    if not content.startswith("#!/usr/bin/env node"):
        content = "#!/usr/bin/env node\n" + content
        dist_index.write_text(content, encoding="utf-8")
        print("shebang追加完了")
    
    print("パッチ適用完了！")

if __name__ == "__main__":
    main()
