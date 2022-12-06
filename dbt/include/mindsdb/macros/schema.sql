{% macro mindsdb__create_schema(relation) -%}
  {%- call statement('create_schema') -%}
  SELECT 1
  {% endcall %}
{% endmacro %}


{% macro mindsdb__drop_schema(relation) -%}
  {%- call statement('drop_schema') -%}
    drop database if exists {{ relation.without_identifier() }}
  {% endcall %}
{% endmacro %}
