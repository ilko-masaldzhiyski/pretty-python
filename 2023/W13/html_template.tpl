{% extends "html_table.tpl" %}
{% block table %}
<div style="padding-left: 20px">
    <br><br><br>
    <h1 style="display: inline; font-family: Archivo;">TECH &nbsp;INDUSTRY &nbsp;EMPLOYMENT &nbsp;TRENDS</h1>
    <p style="color: #A2A2A2; font-family: 'Archivo'; font-size: 16px; margin-top: 15px; margin-bottom:5px;">Employee growth and decline in the largest tech companies, 2009 - 2022</p>
    <p style="color: #A2A2A2; font-family: 'Archivo'; font-size: 16px; margin-top: 0px;">IBM consistently shrinking over time. Amazon downsizing in the last year.</p>
</div>
<div style="padding-left: 20px">
{{ super() }}
</div>
<br><br><br>
{% endblock table %}
