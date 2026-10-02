{# Round a number to 2 decimal places. #}
{% macro money(column) -%}
    round({{ column }}, 2)
{%- endmacro %}
