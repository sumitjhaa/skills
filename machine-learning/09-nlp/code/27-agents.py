"""
09.27 Agents — ReAct Agent with Tool Execution Loop
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


class Tool:
    def __init__(self, name, func, description=""):
        self.name = name
        self.func = func
        self.description = description

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class ReActAgent:
    """
    Reasoning + Acting loop agent.
    Thought -> Action -> Observation -> Thought -> ...
    """

    def __init__(self, tools=None):
        self.tools = {t.name: t for t in (tools or [])}
        self.history = []

    def think(self, query):
        """Simulate reasoning step."""
        thoughts = [
            f"Thought: I need to answer '{query}'.",
            "Thought: I should look up relevant information.",
            "Thought: Let me use a tool to find the answer.",
        ]
        return thoughts[np.random.randint(len(thoughts))]

    def act(self, thought):
        """Decide which tool to use based on thought."""
        if "look up" in thought.lower() or "search" in thought.lower():
            return "search"
        if "calculate" in thought.lower() or "compute" in thought.lower():
            return "calculator"
        return "search"

    def observe(self, action, result):
        return f"Observation ({action}): {result}"

    def run(self, query, max_steps=5):
        self.history = []
        step = 0
        result = None

        while step < max_steps:
            thought = self.think(query)
            self.history.append(thought)

            action = self.act(thought)
            if action in self.tools:
                result = self.tools[action](query)
            else:
                result = f"No tool named {action}"

            observation = self.observe(action, result)
            self.history.append(observation)

            # Simple check: if we have a result, stop
            if result and "not found" not in result.lower():
                thought_final = f"Thought: I have the answer: {result}"
                self.history.append(thought_final)
                break
            step += 1

        return self.history


if __name__ == "__main__":
    def search_func(query):
        data = {
            "capital of france": "Paris",
            "population of india": "1.4 billion",
            "python gui framework": "Tkinter, PyQt, wxPython",
        }
        for key, val in data.items():
            if key in query.lower():
                return val
        return f"No results for: {query}"

    tools = [
        Tool("search", search_func, "General knowledge search"),
        Tool("calculator", lambda q: f"Calculated: {hash(q) % 1000}", "Basic computation"),
    ]
    agent = ReActAgent(tools)

    query = "What is the capital of France?"
    history = agent.run(query)
    for entry in history:
        print(entry)
