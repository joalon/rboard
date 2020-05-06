import models
from jinja2 import Template

SCHOOL = {
  'EYE': {
    'COURSES': {
      'CLASS_0E',
      'CLASS_0F'
    },
    'EYE|MIT': {
      'COURSES': {
        'CLASS_1E',
        'CLASS_2F'
      },
      'EYE|MIT|NIT': {
        'COURSES': {
          'CLASS_1X',
          'CLASS_1D'
        },
        'EYE|MIT|NIT|XXX': {
          'COURSES': {
            'CLASS_4X'
          }
        }
      },
      'EYE|EDX': {
        'COURSES': {
          'CLASS_9A',
          'CLASS_9B'
        }
      }
    }
  }
}

template = Template("""
{%- macro recurse(n) %}
    {%- for key, value in n.items() %}
        {%- if key is not equalto 'COURSES' %}
            {{key}}
        {%- endif %}
        {%- if 'COURSES' in value and value is iterable %}
            COURSES
            {%- for item in value['COURSES'] %}
                {{item}}
            {%- endfor %}
        {%- endif %}
        {%- if value.items is defined %}
            {{recurse(value)}}
        {%- endif %}
    {%- endfor %}
{%- endmacro %}
{{ recurse(tree) }}
""")




my_tree = Post(text="asd", comments=[Comment(body="hej", comments=[Comment(body="igen")])])



my_template = Template("""
{%- macro recurse(comment) %}
        {%- if key is not equalto 'COURSES' %}
            {{key}}
        {%- endif %}
        {%- if 'COURSES' in value and value is iterable %}
            COURSES
            {%- for item in value['COURSES'] %}
            ┆   {{item}}
            {%- endfor %}
        {%- endif %}
        {%- if value.items is defined %}
            {{recurse(value)}}
        {%- endif %}
    {%- endfor %}
{%- endmacro %}
{{ recurse(tree) }}
""")

print(my_template.render(tree=post.comments[0]))

print(template.render(tree=SCHOOL))
