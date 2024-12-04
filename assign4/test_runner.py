import os
import subprocess

# Path to the test directory and the ToyLang interpreter
TEST_DIR = "tst"
INTERPRETER = "toylang2.py"

def run_test(file_path):
    try:
        print(f"Running test: {file_path}")
        result = subprocess.run(
            ["python", INTERPRETER],
            input=open(file_path).read(),
            text=True,
            capture_output=True
        )
        print(f"Output:\n{result.stdout}")
        if result.stderr:
            print(f"Errors:\n{result.stderr}")
    except Exception as e:
        print(f"Error while running test {file_path}: {e}")

def main():
    if not os.path.exists(TEST_DIR):
        print(f"Test directory {TEST_DIR} not found!")
        return
    
    for file_name in sorted(os.listdir(TEST_DIR)):
        if file_name.endswith(".toy2") or file_name.endswith(".toy"):
            file_path = os.path.join(TEST_DIR, file_name)
            run_test(file_path)

if __name__ == "__main__":
    main()
