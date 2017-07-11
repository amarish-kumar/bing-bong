$(document).ready(function() {
   $('#explore').click(function() {
        $.get('/results', { query: $('#query').val()}, function(data) {
            $('#results').html("");
            $('#results').append('<ul>');
            var results = data.results;
            for(var i=0;i<results.length;i++) {
                $('#results').append('<li>' + results[i].url + ' -> ' + results[i].rank + '</li>')
            }
            $('#results').append('</ul>');
        });
    });
});