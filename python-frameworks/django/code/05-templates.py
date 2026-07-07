"""Template rendering — pure Python simulation."""
import re

def render_template(template: str, context: dict) -> str:
    result = template

    for key, value in context.items():
        result = result.replace(f'{{{{ {key} }}}}', str(value))

    def replace_for(match):
        loop_var = match.group(2)
        collection_name = match.group(3)
        items = context.get(collection_name, [])
        body = match.group(4)
        output = []
        for item in items:
            item_context = {**context, loop_var: item}
            output.append(render_template(body, item_context))
        return '\n'.join(output)

    result = re.sub(r'({% for (\w+) in (\w+) %})(.*?)({% endfor %})', replace_for, result, flags=re.DOTALL)

    def replace_var(match):
        var_name = match.group(1)
        return context.get(var_name, '')

    result = re.sub(r'{{ (\w+)\|upper }}', lambda m: context.get(m.group(1), '').upper(), result)
    result = re.sub(r'{{ (\w+)\|lower }}', lambda m: context.get(m.group(1), '').lower(), result)

    return result


template = """
<html>
<body>
  <h1>{{ title }}</h1>
  <ul>
  {% for item in posts %}
    <li>{{ item|upper }}</li>
  {% endfor %}
  </ul>
</body>
</html>
"""

context = {
    'title': 'My Blog',
    'posts': ['Hello Django', 'Django Models', 'Django Views'],
}

print(render_template(template, context))
