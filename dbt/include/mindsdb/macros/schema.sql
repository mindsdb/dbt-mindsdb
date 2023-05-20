{% macro mindsdb__create_schema(relation) -%}

  -- WA for https://github.com/mindsdb/mindsdb/issues/4152
  {%- call statement('tables', fetch_result = True) -%}
  SHOW DATABASES
  {%- endcall -%}
  {%- set tables = load_result('tables') -%}
  {%- set tables_data = tables['data'] -%}

  {%- set found_table = {'result':False} -%}
  {% for item in tables_data %}
    {% if item[0] == relation.schema %}
      {% do found_table.update({'result': True}) %}
    {% endif %}
  {% endfor %}
  {% if not found_table['result'] %}
    {%- call statement('create_schema') -%}
      CREATE PROJECT {{ relation.schema }}
    {%- endcall -%}
  {% endif %}
  -- end WA
{% endmacro %}


{% macro mindsdb__drop_schema(relation) -%}
  {%- call statement('drop_schema') -%}
    drop database if exists {{ relation.project }}
  {% endcall %}
{% endmacro %}
