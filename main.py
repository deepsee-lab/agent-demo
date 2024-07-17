# 加载环境变量
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# 自研包导入
from AutoAgent.AutoGPT import AutoGPT
from Tools import *
from Tools.PythonTool import ExcelAnalyser

# 三方包导入
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)


def launch_agent(agent: AutoGPT):
    """执行 agent 函数"""
    human_icon = "\U0001F468"
    ai_icon = "\U0001F916"

    # 对话程序的主循环
    while True:
        task = input(f"{ai_icon}：有什么可以帮您？\n{human_icon}：")
        # 退出条件
        if task.strip().lower() == "quit":
            break
        reply = agent.run(task, verbose=True)
        print(f"{ai_icon}：{reply}\n")


def main():
    # 加载数据
    loader = DirectoryLoader('./data/')
    documents = loader.load()
    print(f'加载文档数量：{len(documents)}')

    # 切分成chunk
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    # 语言模型
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # 存储长时记忆的向量数据库
    db = Chroma.from_documents(docs, embedding_function)
    retriever = db.as_retriever(
        search_kwargs={"k": 1}
    )

    # 自定义工具集
    tools = [
        document_qa_tool,
        document_generation_tool,
        email_tool,
        excel_inspection_tool,
        directory_inspection_tool,
        finish_placeholder,
        ExcelAnalyser(
            prompts_path="./prompts/tools",
            prompt_file="excel_analyser.json",
            verbose=True
        ).as_tool()
    ]

    # 语言模型，agent 大脑
    llm = ChatOpenAI(
        model="gpt-4-1106-preview",
        temperature=0,
        model_kwargs={
            "seed": 42
        },
    )

    # 定义智能体
    agent = AutoGPT(
        # 大脑
        llm=llm,
        # 提示词的目录
        prompts_path="./prompts/main",
        # 可用的工具
        tools=tools,
        # 工作目录
        work_dir="./data",
        # 主要提示词
        main_prompt_file="main.json",
        # 任务结束的提示词
        final_prompt_file="final_step.json",
        # 最大的思考轮数
        max_thought_steps=20,
        # 长期记忆
        memery_retriever=retriever
    )

    # 运行智能体
    launch_agent(agent)


if __name__ == "__main__":
    main()
