def main(chk_str: str) -> str:
    if not chk_str:
        return "no text provided"
    if isinstance(chk_str, tuple):
        " ".join(chk_str)
    replace_index = {
            '\n': ' ',
            '.': '-',
            ',': '-',
            '_': '-',
            '---': '-',
            '--': '-',
            '  ': ' ',
            }
    for x, y in replace_index.items():
        chk_str = chk_str.replace(x, y)
    return chk_str.strip()
