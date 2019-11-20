{% extends "index.html" %}
{% block header %}
<h1>Nýskráning:</h1>
{% endblock %}

{% block content %}
<form class="Form" method="POST">
    <div>
        <p>Username:</p>
        <input type="text" name="username" required placeholder="Someone26" size="35">
        {% if errors[0] %}
            <p class="loginError">Username already taken</p>
        {% endif %}
    </div>

    <div>
        <p>Netfang:</p>
        <input type="text" name="email" required placeholder="someone@yahoo.com">
        {% if errors[1] %}
            <p class="loginError">Email already registered on this site</p>
        {% endif %}
    </div>

    <div>
        <p>Lykilorð:</p>
        <input type="password" name="password" required placeholder="************">
    </div>


    <div>
        <input type="submit" value="Submit">
    </div>
</form>
{% endblock %}