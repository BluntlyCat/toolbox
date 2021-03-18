let Ajax = function (callbackOnError)
{
    let self = this;
    let data = new FormData();

    let resetData = function ()
    {
        data = new FormData();
    };

    this.ajaxForm = $('#ajaxForm');

    this.addAllData = function (form)
    {
        data = new FormData(form[0]);
    };

    this.appendObject = function (obj)
    {
        for (let key in obj)
        {
            if (obj.hasOwnProperty(key))
            {
                let d = data.get(key);

                if(!d) {
                    data.append(key, obj[key]);
                }
            }
        }
    };

    this.request = function (url, callback)
    {
        data.append('ajaxCall', 'true');

        if(!data.get('csrfmiddlewaretoken'))
        {
            let token = self.ajaxForm.find('input').first().val();
            data.append('csrfmiddlewaretoken', token);
        }

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: false,
            dataType: 'json',
            processData: false, // Don't process the files
            contentType: false, // Set content type to false as jQuery will tell the server its a query string request
            success: function (response)
            {
                if (response['loggedOut'] === true)
                {
                    callbackOnError(response);
                }
                else
                {
                    if (response)
                    {
                        data.response = response;

                        if (callback instanceof Function)
                            callback(data);
                    }
                }

                resetData();
            },
            error: function (xhr)
            {
                callbackOnError(xhr);
                resetData();
            }
        });
    };
};