
{% materialization table, adapter='mindsdb' %}

  {% set target_relation = config.get('destination_table') %}
  {% set predictor_name = config.get('predictor_name') %}

  -- ... setup database ...
  -- ... run pre-hooks...

  -- build model
  {% call statement() -%}
    {{ apply_predictor_wrap(sql, predictor_name, target_relation) }}
  {%- endcall %}

  -- ... run post-hooks ...
  -- ... clean up the database...

  -- Return the relations created in this materialization
  {{ return({'relations': [target_relation]}) }}

{%- endmaterialization -%}



