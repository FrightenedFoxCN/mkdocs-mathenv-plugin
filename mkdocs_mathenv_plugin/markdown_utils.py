import re

def replace_standalone_words(word: str, target: str, string: str) -> str:
    return re.sub(f"\\b{word}\\b", target, string)

def replace_indented_block_start_with_options(target, handle, string):
    return re.sub(rf"({target}(\[(?P<options>.*)\])?.*\n(?P<contents>(((\t|(    )).*)|\n)*))", handle, string)

def get_indentation_level(str):
    return (len(str) - len(str.lstrip())) // 4

def _set_line_indentation_level(line, level):
    prev_level = get_indentation_level(line)
    return(" " * 4 * (prev_level + level)) + line.lstrip()

def return_to_indentation_level(str, level):
    lines = str.split("\n")
    return "\n".join([_set_line_indentation_level(line, level) for line in lines])

print(replace_standalone_words("1", "3", "1 12 1 10 7 8 1"))

def handle(matched):
    options = matched.group("options")
    contents = matched.group("contents")
    print("options:", options, "contents:", contents, sep="\n")

print("First test for indented block")

replace_indented_block_start_with_options("test", handle, """
test[option1, option2, option3]
    indented block
    another indented block

    also indented block
non-indented part
""")

replace_indented_block_start_with_options("test", handle, """
test
    indented block
    another indented block

    also indented block
non-indented part
""")

print(get_indentation_level("""    1 2 3 4   """))

print(return_to_indentation_level("""
    123
1234
        123
""", 1))