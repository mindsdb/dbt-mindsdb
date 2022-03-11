
{% materialization table, adapter='mindsdb' %}

  {%- set identifier = model['alias'] -%}
  {%- set integration = config.get('integration') -%}
  {%- set predictor_name = config.get('predictor_name') -%}

  {% if integration is none %}
      {{ exceptions.raise_compiler_error('Integration is not set') }}
  {% endif %}

  {%- set target_relation = '`{}`.`{}`'.format(integration, identifier) -%}

  -- ... setup database ...
  -- ... run pre-hooks...

  -- build model
  {%- call statement() -%}
    {{ apply_predictor_wrap(sql, predictor_name, target_relation) }}
  {%- endcall -%}

  -- ... run post-hooks ...
  -- ... clean up the database...

  -- Return the relations created in this materialization
  {{ return({'relations': [target_relation]}) }}

{%- endmaterialization -%}



