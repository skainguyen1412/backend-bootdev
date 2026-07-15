from functions.get_files_info import get_files_info

current_directory = get_files_info("calculator", ".")

print(f"Result for current directory: \n{current_directory}")

pkg = get_files_info("calculator", "pkg")

print(f"Result for 'pkg' directory: \n{pkg}")

bin = get_files_info("calculator", "/bin")

print(f"Result for '/bin' directory: \n{bin}")

ddot = get_files_info("calculator", "../")

print(f"Result for '../' directory: \n{ddot}")
