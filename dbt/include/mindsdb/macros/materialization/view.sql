
{% materialization view, adapter='mindsdb' %}

    {{ exceptions.raise_compiler_error('View materialization is not supported') }}

{%- endmaterialization -%}




