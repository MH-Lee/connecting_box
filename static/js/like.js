$(document).ready(function(event) {
    $(document).on('click', '#unlike', function(event) {
      event.preventDefault();
      var pk = $(this).attr('value');
      $.ajax({
        type: 'POST',
        url: '{% url "email_like" %}',
        data: {'id':pk, 'csrfmiddlewaretoken': '{{ csrftoken }}' },
        dataType: 'json',
        success: function(response){ 
          $('#like_section').html(response['form']) 
        },
        error: function(rs, e){
          console.log(rs.responseText);
        },
      });
    });
  });