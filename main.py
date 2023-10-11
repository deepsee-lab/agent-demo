from dotenv import load_dotenv

load_dotenv("api_keys.env")  # 从环境变量中加载 API keys，必须在所有 import 之前

from AutoAgent.AutoGPT import AutoGPT
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from Tools import *
from Tools.PythonTool import ExcelAnalyser
from langchain.agents.agent_toolkits import FileManagementToolkit


def launch_agent(agent: AutoGPT):
    human_icon = "\U0001F468"
    ai_icon = "\U0001F916"

    while True:
        task = input(f"{ai_icon}：有什么可以帮您？\n{human_icon}：")
        if task.strip().lower() == "quit":
            break
        reply = agent.run(task, verbose=True)
        print(f"{ai_icon}：{reply}\n")


def main():

    prompts_path = "./prompts"

    # 语言模型
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,
        model_kwargs={"top_p": 1 / 100255},
    )

    # 存储长时记忆的向量数据库
    db = Chroma.from_documents([Document(page_content="")], OpenAIEmbeddings(model="text-embedding-ada-002"))
    retriever = db.as_retriever(search_kwargs=dict(k=1))

    # 自定义工具集
    tools = [
        calculator_tool,
        calendar_tool,
        document_qa_tool,
        document_generation_tool,
        email_tool,
        excel_inspection_tool,
    ]

    # 添加文件管理工具
    tools += FileManagementToolkit(
        root_dir="."
    ).get_tools()

    # 添加Excel分析工具
    tools += [ExcelAnalyser(
        prompts_path=prompts_path
    ).as_tool()]

    # 定义智能体
    agent = AutoGPT(
        llm=llm,
        prompts_path=prompts_path,
        tools=tools,
        work_dir="./data",
        main_prompt_file="main.templ",
        final_prompt_file="final.templ",
        max_thought_steps=20,
        memery_retriever=retriever
    )

    # 运行智能体
    launch_agent(agent)


if __name__ == "__main__":
    main()
