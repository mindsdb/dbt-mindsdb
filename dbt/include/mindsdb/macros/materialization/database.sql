{% materialization database, adapter='mindsdb' %}
  {%- set database = model['alias'] -%}
  {%- set engine = config.get('engine') -%}
  {%- set parameters = config.get('parameters') -%}

  -- build model
  {%- call statement('main') -%}
    CREATE DATABASE {{ database }}
  {%- endcall -%}
  {%- call statement('main') -%}
    DROP DATABASE IF EXISTS {{ database }}
  {%- endcall -%}


  {%- call statement('main') -%}
    CREATE DATABASE {{ database }} WITH ENGINE='{{engine}}',
    PARAMETERS={{parameters}}
  {%- endcall -%}


  -- Return the relations created in this materialization
  {{ return({'relations': []}) }}
{%- endmaterialization -%}

