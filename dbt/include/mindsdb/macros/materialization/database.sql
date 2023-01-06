{% materialization database, adapter='mindsdb' %}
  {%- set database = model['alias'] -%}
  {%- set engine = config.get('engine') -%}
  {%- set prefix = config.get('prefix') -%}
  {%- set parameters = config.get('parameters') -%}

  {% if prefix is none %}
    {%- set connector = database %}
  {% else %}
    {%- set connector =  prefix ~ "_" ~ database %}
  {% endif %}
  

  -- build model

  -- WA for https://github.com/mindsdb/mindsdb/issues/4152
  {%- call statement('tables', fetch_result = True) -%}
  SHOW DATABASES
  {%- endcall -%}
  {%- set tables = load_result('tables') -%}
  {%- set tables_data = tables['data'] -%}
  
  {%- set found_table = False -%}
  {% for item in tables_data %}
    {% if item[0] == connector %}
    {%- call statement('main') -%}
      DROP DATABASE IF EXISTS {{ connector }}
    {%- endcall -%}
    {% endif %}
  {% endfor %}

  -- end WA


  {%- call statement('main') -%}
    CREATE DATABASE {{ connector }} WITH ENGINE='{{engine}}',
    PARAMETERS={{parameters}}
  {%- endcall -%}

  {{ log("Create mindsdb database(integration) \"" ~ connector ~ "\" with engine \"" ~ engine ~ "\"", True) }}

  -- Return the relations created in this materialization
  {{ return({'relations': []}) }}
{%- endmaterialization -%}

