# 🏗️ Chains
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Combine prompts, LLMs, and parsers into chains.

## LLMChain (Legacy)

```python
from langchain.chains import LLMChain

chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(text="Hello")
```

## Modern Chain (LCEL)

```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | llm | StrOutputParser()
result = chain.invoke({"text": "Hello", "language": "French"})
```

## Sequential Chains

```python
chain1 = prompt1 | llm1 | parser
chain2 = prompt2 | llm2 | parser
full_chain = chain1 | chain2
# Output of chain1 becomes input to chain2
```

<!-- 🤔 Use LCEL (LangChain Expression Language) with `|` operator. It's the modern way. -->

## Run the Code

```bash
python code/04-chains.py
```
