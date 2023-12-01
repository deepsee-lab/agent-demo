from colorama import init, Fore, Back, Style

THOUGHT_COLOR = Fore.GREEN
OBSERVATION_COLOR = Fore.YELLOW
ROUND_COLOR = Fore.BLUE

def color_print(text, color=None):
    if color is not None:
        print(color + text + Style.RESET_ALL)
    else:
        print(text)

def chinese_friendly(string) -> str:
    lines = string.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('{') and line.endswith('}'):
            try:
                lines[i] = json.dumps(json.loads(line), ensure_ascii=False)
            except:
                pass
    return '\n'.join(lines)