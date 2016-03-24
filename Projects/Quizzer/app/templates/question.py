{% extends "base.html" %}

{% block content %}
            <form class="form-inline" action="" method="post" name="post">
                {{form.hidden_tag()}}
                <div class="form-group {% if form.topic.errors %}error{% endif %}">
                    <label for="topic">New topic name:</label>
                        {{ form.topic(size = 30, maxlength = 255) }}
                    <button type="submit" class="btn btn-default">New Topic</button>
                </div>
                {% for error in form.topic.errors %}
                    <span class="help-inline">{{error}}</span>
                {% endfor %}
            </form>
{% endblock %}