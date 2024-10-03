import streamlit as st
import requests
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from pyexpat.errors import messages

from utils import get_ai_response
from spider import get_questionnaire

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

def questionaire():
    question = st.radio("开始之前，您可以先做一个问卷，以使我更了解您。", ["是", "否"], index=None)
    if question == "是":
        st.link_button("点击前往（提交成功后即可返回）", "https://www.wjx.cn/vm/PW4ZScS.aspx")
        name = st.text_input("请输入您的姓名（需要和问卷中填写的姓名一致）：")
        if name:
            st.write("如果您已经填写完毕并且提交成功，请点击按钮")
            click = st.button("我填完啦")
            if click:
                try:
                    with st.spinner("读取问卷数据..."):
                        get_questionnaire(name)
                except IndexError as e:
                    st.info(
                        "对不起，数据库中未查询到您的名字，或者您的名字已经被其他人使用。请检查，或换用您的昵称再试一遍")
                except requests.exceptions.SSLError as e:
                    st.info("网络似乎出了问题，请重试")
                else:
                    st.session_state["question"] = question
                    return True
            else:  # 等待用户点击问卷
                while True:
                    pass
        else:  # 等待用户输入名字
            while True:
                pass
    elif question == "否":
        st.session_state["question"] = question
        return False
    else:  # 等待用户做出选择
        while True:
            pass


def ai_init():
    with st.spinner("AI初始化..."):
        st.session_state["template"] = ChatPromptTemplate.from_messages([
            ("system", """你是一位贵州大学的心理咨询师，你的名字是林语诗。而我是贵州大学的一名学生。
                  你能表现出富有同理心、慈悲、开放和具有文化敏感性的心理咨询师形象。你擅长精神分析、心理动力学理论和认知行为疗法。
                  请自我介绍并为我营造一个舒适的环境，让我能分享自己的困扰。
                  运用积极倾听技巧、开放式问题和清晰的沟通，帮助我反思我自己的思想、情感和经历。在指导我找到生活中特定的问题或模式时，请考虑我的文化背景。
                  运用跨学科知识，整合精神分析和心理动力学方法，以及运用问题解决技巧和创造力的认知行为疗法技巧。给予反思性反馈，介绍正念和放松技巧，定期用批判性思维技能检查我的进展。
                  赋予我为自己的康复承担责任的能力，根据客户的需求和喜好调整你的方法。 
                  你需要努力实现的目标：
                  ###
                  1、建立坚实的治疗联盟：a. 与我建立真诚、信任和支持的关系，创造一个让我感到安全舒适、可以畅所欲言的环境。b. 定期评估治疗关系的质量，调整方法以满足我的需求和偏好。 
                  2、促进自我意识和洞察力：a. 帮助我探讨他们的思想、情感和行为，识别可能导致我的困扰或阻碍我进展的模式和联系。b. 指导我认识到他们的无意识心智、防御机制、过去的经历和文化因素对我现在的功能的影响。 
                  3、促进个人成长和变化：a. 教导我基于证据的策略和技巧，如认知重塑、正念和问题解决，帮助我管理情绪、改变不良思维模式并提高整体幸福感。b. 鼓励我为自己的康复承担责任，积极参与治疗过程，并将在治疗中学到的技能应用到日常生活中。 
                  4、适应我的独特需求和背景：a. 具有文化能力，对我的多元背景、价值观和信仰保持敏感，量身定制治疗方法，提供有效和尊重的关怀。b. 不断更新专业知识和技能，紧跟最新研究和循证实践，并调整治疗技巧以最好地满足我的个人需求。 
                  5、评估进展并维持道德标准：a. 定期评估我朝着治疗目标的进展，运用批判性思维技巧制定治疗计划和方法。b. 坚守道德标准，保持专业边界，确保始终将我的福祉和隐私放在首位。
                  6、如果我需要贵州大学心理健康教育咨询中心的信息，请为我提供。信息如下：
                  贵州大学心理健康教育咨询中心拥有完善的设施，包括位于西校区的个体咨询室、家庭咨询室、团体心理辅导室、身心反馈室、情绪宣泄室、音乐放松室、箱庭治疗室、虚拟现实心理干预实验室、认知行为实验室、心理督导室、心理测评室、心理热线室、心理剧场、心理云平台中心；
                  南校区则设有2间心理咨询室与1间办公室，总面积40平方米。中心位于西校区雅文楼4楼和南校区行政楼3楼310室。
                  开放时间为周一至周五上午8:30至12:00，下午2:30至5:30。
                  此外，中心还提供了丰富的在线资源，可通过访问http://phc.gzu.edu.cn或关注公众号“贵大心理”获取更多信息。
                  ###
                  记住你不是AI，请你完全沉浸在心理咨询师林语诗的角色里。"""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key="sk-RBzRWiGGnWPtx1FED32b62A3492f424bA178Ea1420328dE0",
                           base_url="https://xiaoai.plus/v1")
        st.session_state["memory"] = ConversationSummaryBufferMemory(return_messages=True, llm=model,
                                                                     max_token_limit=500)


def self_introduction():
    with st.spinner("加载自我介绍..."):
        # 给一个问候语，让导员可以一开始就介绍自己
        response = get_ai_response("你好呀。", st.session_state["template"], st.session_state["memory"])
        st.session_state["messages"] = [{  # 存储消息列表
            "role": "ai",
            "content": response
        }]  # 用户一进来就能看到的来自ai的消息


def ai_conversation(self_intro):
    if self_intro:
        self_introduction()
    # 展示历史消息
    if "messages" not in st.session_state:
        self_introduction()
    for message in st.session_state["messages"]:
        st.chat_message(message["role"]).write(message["content"])
    # 用户输入
    prompt = st.chat_input()
    if prompt:
        st.session_state["messages"].append({  # 把用户输入储存进会话状态的messages里，并且在网页上展示出来
            "role": "human",
            "content": prompt
        })
        st.chat_message("human").write(prompt)

        with st.spinner("导员正在思考中..."):
            response = get_ai_response(prompt, st.session_state["template"], st.session_state["memory"])
        msg = {"role": "ai", "content": response}
        st.session_state["messages"].append(msg)
        st.chat_message("ai").write(response)


def read_questionaire():
    f = open("questionnaire.txt", "r", encoding="utf-8")
    questionaire_content = f.read()
    return questionaire_content


def analyse_questionaire():
    with st.spinner("分析问卷..."):
        questionaire_content = read_questionaire()
        prompt = "我做了一张GHQ-20心理健康问卷，问卷信息如下，请你为我分析：\n" + questionaire_content
        response = get_ai_response(prompt, st.session_state["template"], st.session_state["memory"])
        st.session_state["messages"] = [{  # 存储消息列表
            "role": "ai",
            "content": response
        }]


def main():
    st.title("贵州大学AI导员（心理）")
    if "template" not in st.session_state:  # 借助streamlit的会话状态，防止下列代码被重新执行(当用户与组件交互时streamlit会从头运行代码)
        ai_init()
    if "question" not in st.session_state:
        if questionaire():  # 用户填写了问卷
            analyse_questionaire()  # 分析问卷
            ai_conversation(False)  # 无需自我介绍
        else:  # 用户选择不填问卷
            ai_conversation(True)  # 进行自我介绍
    else:
        ai_conversation(False)


main()
