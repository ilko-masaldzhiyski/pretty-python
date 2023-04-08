{% extends "html_table.tpl" %}
{% block table %}
<div style="text-align: center;">
    <br><br><br>
    <h1 style="display: inline; font-family: Archivo;">MONTHLY &nbsp;WEATHER &nbsp;FORECAST</h1>
    <p style="color: #A2A2A2; font-family: 'Archivo'; font-size: 16px; margin-top: 15px; margin-bottom:5px;">The 30-day forecast lets you know the anticipated weather day by day.</p>
    <p style="color: #A2A2A2; font-family: 'Archivo'; font-size: 16px; margin-top: 0px;">These trends can be helpful when planning trips or preparing for the weather in advance.</p>
</div>
<div style="padding-left: 20px">
{{ super() }}
</div>
<br><br><br>
{% endblock table %}
