
{% materialization predictor, adapter='mindsdb' %}

  {%- set project = model.schema -%}
  {%- set predictor = model['alias'] -%}
  {%- set integration = config.get('integration') -%}
  {%- set predict = config.get('predict') -%}
  {%- set predict_alias = config.get('predict_alias') -%}
  {%- set order_by = config.get('order_by', none) -%}
  {%- set group_by = config.get('group_by', none) -%}
  {%- set window = config.get('window', none) -%}
  {%- set horizon = config.get('horizon', none) -%}
  {%- set using = config.get('using') -%}

  {% if predict is none %}
      {{ exceptions.raise_compiler_error('Predict target is not set') }}
  {% endif %}

  -- ... setup database ...
  -- ... run pre-hooks...

  -- ... using to string ...
  {%- set using_str = None  -%}
   {% if using is not none %}
      {%- set using_list = []  -%}
      {%- set keys = using.keys() -%}

      {% for key in keys|sort -%}
         {{ using_list.append('{} = {}'.format(key, using[key] | tojson) )  }}
      {%- endfor %}

      {% set using_str = using_list | join(',\n') %}

  {% endif %}


  -- build model
  -- even if project does not exists, mindsdb returns no error
  {%- call statement('main') -%}
    {{ drop_predictor_wrap(project, predictor)}}
  {%- endcall -%}


  {%- call statement('main') -%}
    {{ create_predictor_wrap(
                             sql,
                             project,
                             predictor,
                             integration,
                             predict,
                             predict_alias,
                             using_str,
                             order_by, group_by, window, horizon )}}
  {%- endcall -%}


  -- ... run post-hooks ...
  -- ... clean up the database...

  -- Return the relations created in this materialization
  {{ return({'relations': []}) }}

{%- endmaterialization -%}


