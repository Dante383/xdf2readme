# {{ xdf.header.title }}

Authored by: {{ xdf.header.author }}
{{ xdf.header.description if xdf.header.description }}

## Categories
{% for index, category in xdf.header.categories.items() if category.elements|length > 0 %}
- {{ category.name }} ({{ category.elements|length }} items)
{% endfor %}

{% if xdf.elements[XdfElementType.PATCH] %}
## Patches
{% for patch in xdf.elements[XdfElementType.PATCH] %}
{% if patch.description %}
<details>
-	<summary>{{ patch.title }}</summary>

	{{ patch.description }}

</details>
{% else %}
- {{ patch.title }} {% for category_index in patch.category_indexes %}[{{ xdf.header.categories[category_index].name }}]{% endfor %}
{% endif %}
{% endfor %}
{% endif %}

## Constants
{% for constant in xdf.elements[XdfElementType.CONSTANT] %}
{% if constant.description %}
<details>
	<summary>{{ constant.title }}</summary>

	{{ constant.description }}

</details>
{% else %}
- {{ constant.title }} {% for category_index in constant.category_indexes %}[{{ xdf.header.categories[category_index].name }}]{% endfor %}
{% endif %}
{% endfor %}

## Tables
{% for table in xdf.elements[XdfElementType.TABLE] %}
{% if table.description %}
<details>
-	<summary>{{ table.title }}</summary>

	{{ table.description }}

</details>
{% else %}
- {{ table.title }} {% for category_index in table.category_indexes %}[{{ xdf.header.categories[category_index].name }}]{% endfor %}
{% endif %}
{% endfor %}

---
[OpenGK.org](https://opengk.org)