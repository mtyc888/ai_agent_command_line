from functions.run_python import run_python_file

def test():
    res1 = run_python_file("calculator", "main.py")
    res3 = run_python_file("calculator", "tests.py")
    res4 = run_python_file("calculator", "../main.py")  
    res2 = run_python_file("calculator", "nonexistent.py")
    print(res1)
    print(res3)
    print(res4)
    print(res2)

if __name__ == "__main__":
    test()
