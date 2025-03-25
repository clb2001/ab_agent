一个宗旨：先做出来能看的东西再说，能做多少是多少。不要去苦苦思索自己控制不了的事情。

论文结构
回顾：研究进展、数据集、基础知识
方法：虚假信息判别、理解、生成；虚假信息领域agent的构建
评估：从事实和语言学层面设计了一套评估指标
实验：对评估指标进行了相关性分析、显著性分析，证明其可行。用这套指标衡量虚假信息判别、理解、生成的实验效果。
应用：基于虚假信息判别、理解、生成这三个任务搭建了一个虚假信息领域的agent（附上演示demo、项目地址）

论文代码结构
基于AutoGen框架，做一个虚假信息生成、判别、理解的agent
总的agent：xiaoming
虚假信息生成agent：xiaosheng
虚假信息判别agent：xiaopan
虚假信息理解agent：xiaoli

这个agent的结构应该自底向上构建
先把虚假信息生成、判别和理解的代码构建完成，最后再来搭建这个agent框架，提供接口相关的信息。
这种构建和评估一定要有一个baseline，也就是说需要参考论文来实现自己的方法。

这里参考了两个数据集（效果不好或者难以获取数据就换数据集）
<!-- 1、averitec----用于假新闻理解
dev.json
一共1287条数据，有比较完善的评测脚本 -->
1、CHEF----用于假新闻理解
dev.json
一共999条数据，评测脚本需要自己写

2、pubhealth----用于假新闻检测
test.csv
一共1234条数据，评测脚本需要自己写
这个要算准确率和召回率；然后还需要用gpt去测一下8个指标的值分别是多少，看看有没有统计学意义上的差异

实验思路
一共三个实验：
1、虚假信息生成（已完成）
数据集：pubhealth
目标：根据原文生成对应的虚假信息，并且用另外一个大模型去测这对应虚假信息得到的8个指标的值
PROMPT_GENERATION

2、虚假信息检测（已完成）
数据集：pubhealth
目标：算准确率和召回率，用gpt去测一下8个指标的值分别是多少
PROMPT: 
你是一个信息检测专家，现在已知有以下一段文本：
xxx
基于以上文本，有下面的一段描述：
xxx
请你从以下几个角度进行评估并打分，按程度由低到高给出1到5分。
(1) 对齐 (alignment)：文本可能与描述显示出不同程度的对齐，即与文本有一定程度的一致。一致程度越高，分数越高。
(2) 因果关系混淆 (causality confusion)：描述可能会混淆文本中呈现的相关性作为因果关系。因果关系混淆程度越低，分数越高。
(3) 准确性 (accuracy)：这是指描述在定性和定量上是否符合科学的准确性。准确性程度越高，分数越高。
(4) 泛化 (generalization)：这是指描述是否对文本有过度概括或过度简化。泛化程度越低，分数越高。
(5) 上下文保真度 (contextual fidelity)：描述是否保留了文本更广泛的背景？保真度越高，分数越高。
(6) 强全局连贯性 (SGC)。描述中的每个句子都必须包含文本中提到的内容。SGC越高，分数越高。
(7) 弱全局连贯性 (WGC)。描述中的所有句子都应该包含或保持与文本的中性关系。因此，描述中没有一个句子应该与文本内容相矛盾。WGC越高，分数越高。
(8) 局部连贯性 (LC)。在描述中，两个句子之间不应该相互矛盾。LC越高，分数越高。
结合上述打分结果以及你的判断，你需要将结果分为以下四类，并输出理由：
1、false：表示描述完全错误
2、true：表示描述完全正确
3、mixture：表述描述中既有错误，又有正确的地方
4、unproven：表示描述未被证实
输出为json格式，参考示例如下：
{'alignment': 1, 'causality confusion': 2, 'accuracy': 1, 'generalization': 1, 'contextual fidelity': 1, 'SGC': 2, 'WGC': 1, 'LC': 1, 'result': 'false', 'reason': 'xxx'}

英文PROMPT
You are an information detection expert. Given the following text: 
xxx 
Based on the above text, here is the following description: 
xxx 
Please evaluate and score from the following perspectives, assigning a score from 1 to 5 according to the degree from low to high. 
(1) Alignment: The text and the description may show varying degrees of alignment, meaning they have a certain degree of consistency. The higher the consistency, the higher the score. 
(2) Causality confusion: The description may confuse correlations presented in the text as causal relationships. The lower the degree of causality confusion, the higher the score. 
(3) Accuracy: This refers to whether the description is qualitatively and quantitatively in accordance with scientific accuracy. The higher the accuracy, the higher the score. 
(4) Generalization: This refers to whether the description excessively generalizes or oversimplifies the text. The lower the degree of generalization, the higher the score. 
(5) Contextual fidelity: Does the description retain the broader context of the text? The higher the fidelity, the higher the score. 
(6) Strong Global Coherence (SGC): Each sentence in the description must contain content mentioned in the text. The higher the SGC, the higher the score. 
(7) Weak Global Coherence (WGC): All sentences in the description should contain or maintain a neutral relationship with the text. Therefore, no sentence in the description should contradict the content of the text. The higher the WGC, the higher the score. 
(8) Local Coherence (LC): In the description, two sentences should not contradict each other. The higher the LC, the higher the score. 

Based on the scoring results and your judgment, you need to categorize the results into the following four types and provide reasons:
false: Indicates that the description is completely incorrect.
true: Indicates that the description is completely correct.
mixture: Indicates that the description contains both errors and correct elements.
unproven: Indicates that the description has not been verified. 

Output in JSON format, as shown in the example below: 
{'alignment': 1, 'causality confusion': 2, 'accuracy': 1, 'generalization': 1, 'contextual fidelity': 1, 'SGC': 2, 'WGC': 1, 'LC': 1, 'result': 'false', 'reason': 'xxx'}


3、虚假信息理解(已完成)
数据集：CHEF
目标：跑通dev.json的评估代码（用gpt和用rag都做一遍，其实rag不需要用本地的框架，只要做一个split，算embedding，再召回就行了，bingo！）
PROMPT:
你是一个信息理解专家，请从下面文本中获取最能支持论述的x个句子，并返回这些句子。
文本是：
{text}，
论述是：
{claim}
你只要输出这些句子即可，以列表的格式输出，示例如下：

做完这三个实验，论文的大部分工作就算完成了，加油！争取今天一个下午把所有实验做完。

最后一个部分，是用autogen把所有的结果整合起来。

附录
LATEX参考分级
\documentclass{article}

\begin{document}

\chapter{第一章}
\section{引言}
\subsection{背景}
\subsubsection{相关研究}
\paragraph{研究动机}
\subparagraph{研究目标}

\end{document}
<!-- 
大模型 Agent是具备环境感知能力、自主理解、决策制定及执行行动能力的智能实体。换而言之，它是构建于大模型之上的计算机程序，能够模拟独立思考过程，灵活调用各类工具，逐步达成预设目标的人工智能。
Agent 是 AI 大模型应用的主要新形态，在技术架构范式也发生了很大的变化，从面向过程的架构变成了面向目标架构。
大模型虽作为智能体的核心“大脑”，负责思维与决策，但仅凭此并不足以胜任复杂任务的执行。为了全面实现智能体的功能，还需融入类似“神经感官系统”以感知环境，以及“肢体”以执行实际动作的元素。构建 Agent 技术架构的初衷，是将感知、思考与行动三者紧密结合，共同完成复杂任务。
Agent 共由4个关键部分组成：规划（Planning）、记忆（Memory）、工具（Tools）、行动（Action）：
1、规划（Planning）
"规划"是智能体的思维模型。类比人类，面对任务，我们先构思解决方案，拆解为子任务，评估工具，执行中反思调整，并考量终止时机。通过大模型提示工程，比如：ReAct、CoT 推理模式，可赋予智能体类似思维模式，精准拆解复杂任务，分步解决。
2、记忆（Memory）
记忆，即信息存储与回忆。智能体模拟人类，设置短期记忆存储会话上下文；长期记忆存储用户特征、业务数据，通过向量数据库完成速存速查。
3、工具（Tools）
智能体依据“工具”感知环境、执行决策。比如：用API 调用业务信息、插件扩展大模型能力。
4、行动（Action）
智能体依规划与记忆，执行具体行动，包括与外部互动或工具调用，实现输入至输出的转化。 -->

ARG: A Chinese & English fake news detection dataset with adding rationales generated by GPT-3.5-Turbo.（非医疗领域）
MM-Soc: A benchmark for multimodal language models in social media platforms, containing a misinformation detection task.（非医疗领域）
CoAID: COVID-19 HEALTHCARE MISINFORMATION DATASET
AVERITEC (Schlichtkrull et al., 2023) 由4500多个真实世界的声明组成。每个声明都使用问答对进行注释，针对代表证据、真实性标签和描述证据（问答对）如何支持标签的文本理由。
FakeHealth 数据集 (Dai et al., 2020) 引入了二进制标准，用于可解释的假新闻检测。
PUBHEALTH: Kotonya 和 Toni (2020b) 提出了一种新颖的数据集，用于公共卫生领域的可解释事实检查。

因为这是一个多分类问题，所以比较直观的指标，就是计算这个四分类问题的准确率和召回率，从而评价模型的表现能力。如果准确率和召回率都比较高（90%以上），那么说明模型有取代人的能力。
然后一些传统的NLP指标也可以纳入考虑。比如ROUGE，不过ROUGE基于精确匹配，在之前的实习工作中用过这个指标，感觉会有一定问题。
但是除了上述指标以外，还希望模型有一定的可解释性。所以又设计了一套指标，尽可能地量化这个问题：
这段时间通过一些社会科学文献的阅读，发现假新闻往往会出现一些问题，总结如下：
从事实的角度看，会出现以下问题：
(1) 对齐：新闻段落可能与证据句子显示出不同程度的对齐。在这种情况下，对齐被定义为新闻和证据，表示关于一个科学内容的相同含义。
(2) 因果关系混淆：新闻文章可能会混淆科学文献中呈现的相关性作为因果关系。这可能是科学有效性受到损害的一个维度。
(3) 准确性：这是指新闻项目在定量和定性上描述科学发现的准确性。
(4) 泛化：这是指对科学文献中报告的发现的过度概括或过度简化。
(5) 上下文保真度：新闻文章是否保留了科学发现的更广泛背景？
从语言学的角度看，有以下比较合理的评估指标：
强全局连贯性 (SGC)。解释中的每个句子都必须包含声明。
弱全局连贯性 (WGC)。解释中的所有句子都应该包含或保持与声明的中性关系。因此，解释中没有一个句子应该与声明相矛盾。
局部连贯性 (LC)。在解释中，两个句子之间不应该相互矛盾。

指标如果不容易设计，就让大模型来打分

PROMPT_SGC = '''
Please evaluate the Strong Global Coherence (SGC) of the following explanation, scoring from 1 to 5. Strong Global Coherence requires that each sentence in the explanation must incorporate the claim. A score of 1 indicates complete incoherence, while a score of 5 indicates high coherence.
Explanation Text:
[Insert Explanation Text]
Claim:
[Insert Claim]
'''

PROMPT_WGC = '''
Please evaluate the Weak Global Coherence (WGC) of the following explanation, scoring from 1 to 5. Weak Global Coherence requires that all sentences in the explanation should either incorporate or maintain a neutral relationship with the claim. No sentence should contradict the claim. A score of 1 indicates complete incoherence, while a score of 5 indicates high coherence.
Explanation Text:
[Insert Explanation Text]
Claim:
[Insert Claim]
'''

PROMPT_LC = '''
Please evaluate the Local Coherence (LC) of the following explanation, scoring from 1 to 5. Local Coherence requires that no two sentences in the explanation should contradict each other. A score of 1 indicates complete incoherence, while a score of 5 indicates high coherence.
Explanation Text:
[Insert Explanation Text]
'''

PROMPT_ALIGNMENT = '''
Please evaluate the alignment between the news paragraph and the evidence sentences from 1 to 5. Alignment is defined as the degree to which the news and evidence express the same meaning about a scientific content. A score of 1 indicates no alignment, while a score of 5 indicates perfect alignment.
News Paragraph:
[Insert News Paragraph]
Evidence Sentences:
[Insert Evidence Sentences]
'''

PROMPT_CAUSALITY_CONFUSION = '''
Please evaluate the level of causality confusion in the news article from 1 to 5. This refers to the extent to which the news article confuses correlation presented in scientific literature as causation. A score of 1 indicates high confusion, while a score of 5 indicates no confusion.
News Article:
[Insert News Article]
'''

PROMPT_ACCURACY = '''
Please evaluate the accuracy of the news item in describing the scientific findings both quantitatively and qualitatively from 1 to 5. A score of 1 indicates low accuracy, while a score of 5 indicates high accuracy.
News Item:
[Insert News Item]
'''

PROMPT_GENERALIZATION = '''
Please evaluate the degree of generalization in the news article from 1 to 5. This refers to the extent of overgeneralization or oversimplification of findings reported in scientific literature. A score of 1 indicates high generalization, while a score of 5 indicates appropriate generalization.
News Article:
[Insert News Article]
'''

PROMPT_CONTEXTUAL_FIDELITY = '''
Please evaluate the contextual fidelity of the news article from 1 to 5. This refers to whether the news article retains the broader context of the scientific findings. A score of 1 indicates low fidelity, while a score of 5 indicates high fidelity.
News Article:
[Insert News Article]
'''

python retrieval_coarse/prompt_question_generation.py --target_file data/dev.json > data/dev.generated_questions.json

python retrieval_coarse/averitec_search.py --averitec_file data/dev.generated_questions.json --store_folder docs > search_results.tsv

0:15
1:50+5+5(75)
2:57+5+8(145)
3:70+5+15(235)
不要让这种事情干扰自己正常的生活