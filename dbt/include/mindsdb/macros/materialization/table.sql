
{% materialization table, adapter='mindsdb' %}

  {%- set identifier = model['alias'] -%}
  {%- set integration = config.get('integration') -%}

  {% if integration is none %}
      {{ exceptions.raise_compiler_error('Integration is not set') }}
  {% endif %}

  -- first element
  {%- set target_relation_list = ['`{}`'.format(integration)]  -%}

  -- path
  {% for item in identifier.split('.') -%}
    {{ target_relation_list.append('`{}`'.format(item))  }}
  {%- endfor %}

  -- final
  {%- set target_relation = api.Relation.create(identifier=target_relation_list[1],
                                                schema=target_relation_list[0],
                                                type='table') -%}

  -- ... setup database ...
  -- ... run pre-hooks...
  {{ run_hooks(pre_hooks) }}

  -- build model
  {% call statement('main') %}
       {{ save_to_table_wrap(sql, target_relation) }}
  {% endcall %}

  -- ... run post-hooks ...
  {{ run_hooks(post_hooks) }}
  -- ... clean up the database...

  -- Return the relations created in this materialization
  {{ return({'relations': [target_relation]}) }}

{%- endmaterialization -%}
