import pandas as pd

def get_column_names(
        filename : str
) -> str :

    """获取 Excel 文件的列名"""

    # 读取 Excel 文件的第一个工作表
    df = pd.read_excel(filename, sheet_name=0)  # sheet_name=0 表示第一个工作表
    column_names = '\t'.join(df.columns.tolist())
    # 打印列名
    return f"这是 '{filename}' 文件的列名：\n\n{column_names}"

def get_first_n_rows(
        filename : str,
        n : int = 3
) -> str :

    """获取 Excel 文件的前 n 行"""

    # 读取 Excel 文件的第一个工作表
    df = pd.read_excel(filename, sheet_name=0)  # sheet_name=0 表示第一个工作表

    n_lines = '\n'.join(
        df.head(n).to_string(index=False, header=True).split('\n')
    )

    return f"这是 '{filename}' 文件的前{n}行样例：\n\n{n_lines}"
