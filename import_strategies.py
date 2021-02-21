import urllib.request
import os

dirname = "imported_strategies"
if not os.path.exists(dirname):
    os.makedirs(dirname)

to_fetch = [
    ("https://github.com/eurisko-us/eurisko-us.github.io/tree/master/files/strategies/cohort-1/level-2/david_strategy_level_2.py","david_strategy_level_2.py"),
    ("https://github.com/eurisko-us/eurisko-us.github.io/blob/master/files/strategies/cohort-1/level-2/elijah_strategy_level_2.py","elijah_strategy_level_2.py"),
    ("https://github.com/eurisko-us/eurisko-us.github.io/blob/master/files/strategies/cohort-1/level-2/george_strategy_level_2.py","george_strategy_level_2.py"),
    ("https://github.com/eurisko-us/eurisko-us.github.io/blob/master/files/strategies/cohort-1/level-2/justin_strategy_level_2.py","justin_strategy_level_2.py")
]

# basic_strategy.py is part of Colby's strategies

# strategy_util.py is used by Elijah's strategies

for url, file_name in to_fetch:
    with urllib.request.urlopen(url) as response:
        content = response.read()
        with open(os.path.join(dirname, file_name), "wb") as text_file:
            text_file.write(content)