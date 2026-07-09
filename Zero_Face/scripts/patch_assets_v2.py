import os

def patch_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Replace ALL occurrences of _next with next, including in assets paths
        if '_next' in content:
            new_content = content.replace('_next', 'next')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Patched: {file_path}")
    except Exception as e:
        print(f"Error patching {file_path}: {e}")

def main():
    # Patch BOTH frontend/out AND android assets
    targets = [r'K:\Zero_Face\frontend\out', r'K:\Zero_Face\android\app\src\main\assets']
    for target in targets:
        for root, dirs, files in os.walk(target):
            for file in files:
                if file.endswith(('.html', '.js', '.css', '.txt', '.webmanifest')):
                    patch_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
