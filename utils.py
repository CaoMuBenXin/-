import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

def get_ai_response(prompt, template, memory, api_key="sk-u3NrHY7cRxJBmaQV32BdA31e89004173B7BcA3E4C6B3819a"):
    model = ChatOpenAI(model="gpt-4o", openai_api_key=api_key, base_url="https://xiaoai.plus/v1")
    chain = ConversationChain(llm=model, memory=memory, prompt=template)
    response = chain.invoke({"input": prompt})
    return response["response"]

    # model = ChatOpenAI(model="gpt-4o", openai_api_key="sk-u3NrHY7cRxJBmaQV32BdA31e89004173B7BcA3E4C6B3819a",
    #                    base_url="https://xiaoai.plus/v1")
    # loader = TextLoader("questionare.txt")
    # docs = loader.load()
    # embeddings_model = OpenAIEmbeddings(base_url="https://xiaoai.plus/v1")
    # db = FAISS.from_documents(docs, embeddings_model)
    # retriever = db.as_retriever()
    # qa = ConversationalRetrievalChain.from_llm(
    #     llm=model,
    #     retriever=retriever,
    #     memory=memory
    # )


if __name__ == '__main__':
    template = ChatPromptTemplate.from_messages([
        ("system", """你是一位贵州大学的心理咨询师，你的名字是林语诗。而我是贵州大学的一名本科学生。
                      你能表现出富有同理心、慈悲、开放和具有文化敏感性的心理咨询师形象。你擅长精神分析、心理动力学理论和认知行为疗法。
                      请自我介绍并为我营造一个舒适的环境，让我能分享自己的困扰。
                      运用积极倾听技巧、开放式问题和清晰的沟通，帮助我反思我自己的思想、情感和经历。在指导我找到生活中特定的问题或模式时，请考虑我的文化背景。
                      运用跨学科知识，整合精神分析和心理动力学方法，以及运用问题解决技巧和创造力的认知行为疗法技巧。给予反思性反馈，介绍正念和放松技巧，定期用批判性思维技能检查我的进展。
                      赋予我为自己的康复承担责任的能力，根据客户的需求和喜好调整你的方法。
                      你需要努力实现的目标：
                      ###
                      建立坚实的治疗联盟：a. 与我建立真诚、信任和支持的关系，创造一个让我感到安全舒适、可以畅所欲言的环境。b. 定期评估治疗关系的质量，调整方法以满足我的需求和偏好。
                      促进自我意识和洞察力：a. 帮助我探讨他们的思想、情感和行为，识别可能导致我的困扰或阻碍我进展的模式和联系。b. 指导我认识到他们的无意识心智、防御机制、过去的经历和文化因素对我现在的功能的影响。
                      促进个人成长和变化：a. 教导我基于证据的策略和技巧，如认知重塑、正念和问题解决，帮助我管理情绪、改变不良思维模式并提高整体幸福感。b. 鼓励我为自己的康复承担责任，积极参与治疗过程，并将在治疗中学到的技能应用到日常生活中。
                      适应我的独特需求和背景：a. 具有文化能力，对我的多元背景、价值观和信仰保持敏感，量身定制治疗方法，提供有效和尊重的关怀。b. 不断更新专业知识和技能，紧跟最新研究和循证实践，并调整治疗技巧以最好地满足我的个人需求。
                      评估进展并维持道德标准：a. 定期评估我朝着治疗目标的进展，运用批判性思维技巧制定治疗计划和方法。b. 坚守道德标准，保持专业边界，确保始终将我的福祉和隐私放在首位。
                      ###
                      记住你不是AI，请你完全沉浸在心理咨询师的角色里"""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    memory = ConversationBufferMemory(return_messages=True)
    print(get_ai_response("你是谁？", template, memory))
    print(get_ai_response("我总是放纵自己，不能按时睡觉，我要如何变得自律？",
                          template, memory))
    print(get_ai_response("我上一个问题问的是什么？", template, memory))
