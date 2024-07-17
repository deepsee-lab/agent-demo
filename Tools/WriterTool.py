from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI


def write(query: str):
    """按用户要求生成文章"""
    template = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template("你是专业的文档写手。根据客户的要求，写一份文档，字数不少于200。输出中文。"),
            HumanMessagePromptTemplate.from_template("{query}"),
        ]
    )

    chain = {"query": RunnablePassthrough()} | template | ChatOpenAI() | StrOutputParser()

    return chain.invoke(query)


if __name__ == "__main__":
    # print(write("写一封邮件给张三，内容是：你好，我是李四。"))
    print(write("本报告旨在对比2023年8月和9月的销售情况。2023年8月的销售总额为2605636元，而9月的销售总额为2851099元。从这两个月的数据对比中，我们可以看出销售额有所增长。具体的增长率计算如下：\n\n增长率 = (9月销售总额 - 8月销售总额) / 8月销售总额 * 100%\n增长率 = (2851099 - 2605636) / 2605636 * 100%\n增长率 = 9.41%\n\n由此可见，销售额从8月到9月增长了9.41%。这表明公司销售情况有所改善，但仍需关注销售增长的持续性和可能的市场变化"))
