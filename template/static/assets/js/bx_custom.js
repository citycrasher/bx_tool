// toaster function
function updateToast(toastClass, toastMessage, delay = 2000) {
        var toastElement = $('.bs-toast.toast');
        toastElement.find('.toast-body').text(toastMessage);
        toastElement.removeClass('bg-success bg-danger bg-warning bg-info hide').addClass(toastClass).addClass('show');
        // Initialize the toast with the specified delay

        setTimeout(function() {
            toastElement.toast('hide');
        }, delay);
    }

// file accept check
document.getElementById('inputFile').addEventListener('change', function(event) {
        const fileList = event.target.files;
        const output = document.getElementById('inputFile');
        output.innerHTML = '';  // Clear previous output

        for (let i = 0; i < fileList.length; i++) {
            const file = fileList[i];
            if (file.name.endsWith('.txt')) {
                const listItem = document.createElement('div');
                listItem.textContent = `Selected file: ${file.name}`;
                output.appendChild(listItem);
            } else {
                alert('Hey User, Only .txt files are allowed.....!!!');
                event.target.value = '';  // Clear the selected files
                break;
            }
        }
    });

// get movie list
$(document).ready(function() {
    $('#client').change(function() {
        var clientId = $(this).val();
        console.log("get movie", "ajaxGetMoviesListUrl");
        if (clientId) {
            $.ajax({
                url: ajaxGetMoviesListUrl,
                data: {
                    'client_id': clientId
                },
                success: function(data) {
                    $('#movie').empty();
                    $('#movie').append('<option value="">Select Movie</option>');
                    $.each(data, function(key, value) {
                        $('#movie').append('<option value="' + value.id + '">' + value.movie_name + '</option>');
                    });
                }
            });
        } else {
            $('#movie').empty();
            $('#movie').append('<option value="">Select movie</option>');
        }
    });
});


// form submit
$(document).ready(function() {
    $('#send-button').click(function() {
        var client = $('#client').val();
        var movie = $('#movie').val();
        var original_type = $('#original_type').val();
        var fileInput = $('#inputFile')[0];
        var urlInput = $('#url_input').val();
        var formData = new FormData();
        formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
        formData.append('client', client);
        formData.append('movie', movie);
        formData.append('original_type', original_type);

        // Check if at least one of the fields is filled
        if ((!urlInput || urlInput.trim() === '') && fileInput.files.length === 0) {
            alert('Please provide either a URL or select a file.');
            return;
        }

        if (urlInput && urlInput.trim() !== '') {
                    formData.append('url', urlInput.trim());
               }

        if (fileInput.files.length > 0) {
                    formData.append('file', fileInput.files[0]);
                }

        $.ajax({
            type: 'POST',
            url: ajaxPostFormIpReportUrl,
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function() {
                //$('#response').text('Sending...');
                //updateToast('bg-primary', 'before', 2000);
                $('#inputFile').val('');
                $('#url_input').val('');
            },
            success: function(response) {
                updateToast('bg-success', response.data, 2000);
            },
            error: function(xhr, status, error) {
                $('#response').text('An error occurred: ' + error);
                updateToast('bg-danger', 'error occurred while reporting' + error, 2000);
            },
            complete: function(response) {
                 // execute after complete

            }
        });
    });
});
