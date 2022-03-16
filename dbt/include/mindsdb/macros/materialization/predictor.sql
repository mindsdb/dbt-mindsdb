
{% materialization predictor, adapter='mindsdb' %}

  {%- set predictor = model['alias'] -%}
  {%- set integration = config.get('integration') -%}
  {%- set predict = config.get('predict') -%}
  {%- set predict_alias = config.get('predict_alias') -%}
  {%- set using = config.get('using') -%}

  {% if integration is none %}
      {{ exceptions.raise_compiler_error('Integration is not set') }}
  {% endif %}

  {% if predict is none %}
      {{ exceptions.raise_compiler_error('Predict target is not set') }}
  {% endif %}

  -- ... setup database ...
  -- ... run pre-hooks...

  -- ... using to string ...
  {%- set using_str = None  -%}
   {% if using is not none %}
      {%- set using_list = []  -%}
      {% for key, value in using.items() -%}
         {{ using_list.append('{} = "{}"'.format(key, value))  }}
      {%- endfor %}

      {% set using_str = using_list | join(',\n') %}

  {% endif %}


  -- build model
  {%- call statement('main') -%}
    {{ drop_predictor_wrap(predictor)}}
  {%- endcall -%}


  {%- call statement('main') -%}
    {{ create_predictor_wrap(
                             sql,
                             predictor,
                             integration,
                             predict,
                             predict_alias,
                             using_str )}}
  {%- endcall -%}


  -- ... run post-hooks ...
  -- ... clean up the database...

  -- Return the relations created in this materialization
  {{ return({'relations': []}) }}

{%- endmaterialization -%}


