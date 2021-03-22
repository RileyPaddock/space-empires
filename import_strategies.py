import urllib.request
import os

dirname = "imported_unit_strategies"
if not os.path.exists(dirname):
    os.makedirs(dirname)

to_fetch = [
    ("https://github.com/eurisko-us/space-empires-cohort-1/blob/main/unit_tests/movement_test_1/initial_state.py","initial_state.py"),
    ("https://github.com/eurisko-us/space-empires-cohort-1/blob/main/unit_tests/movement_test_1/initial_state.py","final_state.py"),

    ("https://github.com/eurisko-us/space-empires-cohort-1/blob/main/unit_tests/movement_test_1/strategies.py","strategies.py")
]

for url, file_name in to_fetch:
    with urllib.request.urlopen(url) as response:
        content = response.read()
        with open(os.path.join(dirname, file_name), "wb") as text_file:
            text_file.write(content)