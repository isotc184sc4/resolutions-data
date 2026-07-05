import re

def block_scalar(text):
    lines = text.strip().split('\n')
    formatted_lines = []
    for line in lines:
        formatted_lines.append(f"      {line}" if line else "")
    return " |\n" + "\n".join(formatted_lines)

def write_yaml():
    pass
