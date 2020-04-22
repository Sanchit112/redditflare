<!doctype html>
<html>

<head>
    <meta charset="UTF-8">
    <title>Reddit Flair Detector</title>
</head>
<div class="formbox">
<form action="{{ url_for('main') }}" method="POST">
    <fieldset>
        <legend>Reddit Flair Detector:</legend>
        Enter a Reddit Post URL from <a href="https://reddit.com/r/india" style="color: black">here</a>:
        <input name="url" type="text" required>
        <br>
        <br>
        <input type="submit" class="btn btn-primary btn-block btn-large">
        
    
    
</fieldset>

</form>

</div>

<br>
<div class="result" align="center">
    {% if result %}
        {% for variable, value in original_input.items() %}
            <b>{{ variable }}</b> : {{ value }}
        {% endfor %}
        <br>
        <br> Predicted flair:
           <p style="font-size:50px">{{ result }}</p>
    {% endif %}
</div>
</html>
