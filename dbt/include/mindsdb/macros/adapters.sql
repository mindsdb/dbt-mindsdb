{% macro mindsdb__list_schemas(database) %}
    {% call statement('list_schemas', fetch_result=True, auto_begin=False) -%}
        select distinct schema_name
        from information_schema.schemata
    {%- endcall %}

    {{ return(load_result('list_schemas').table) }}
{% endmacro %}


{% macro mindsdb__list_relations_without_caching(schema_relation) %}
  {% call statement('list_relations_without_caching', fetch_result=True) -%}
    select
      null as "database",
      table_name as name,
      table_schema as "schema",
      'table' as table_type
    from information_schema.tables
    where table_schema = '{{ schema_relation.schema }}'
  {% endcall %}
  {{ return(load_result('list_relations_without_caching').table) }}
{% endmacro %}


{% macro apply_predictor_wrap(sql, predictor_name, destination_table) -%}

  create or replace table {{ destination_table }}
    select * from (
       {{ sql }}
    )
    join {{ predictor_name }}

{% endmacro %}


{% macro drop_predictor_wrap(predictor) -%}

    DROP PREDICTOR IF EXISTS {{ predictor }};

{% endmacro %}

{% macro create_predictor_wrap(sql, predictor, integration, predict, predict_alias, using) -%}

    CREATE PREDICTOR {{ predictor }}
    FROM {{ integration }}  (
        {{ sql }}
    ) PREDICT {{ predict }} {% if predict_alias is not none %} as {{predict_alias}} {% endif %}
     {% if using is not none %}
     USING
       {{using}}
     {% endif %}

{% endmacro %}