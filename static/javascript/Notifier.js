let Message = function ($container, text, type, timeout, callback) {
    let width = $container.outerWidth(true);
    let self = this;
    let $messageBox = $(`<span class="message-box alert alert-${type}">${text}</span>`);
    let timeoutID = 0;

    if(callback instanceof Function) {
        $messageBox.click(function() {
            clearTimeout(timeoutID);
            callback(self);
        });
    }
    else {
        $messageBox.click(function() {
            clearTimeout(timeoutID);
            self.hide(300, true);
        });
    }

    this.hide = function (duration = 0, remove = false) {
        $messageBox.animate({left: `+=${width}px`}, duration, function () {
            if(remove) {
                $messageBox.remove();
            }
        });
    }

    $container.prepend($messageBox);
    $messageBox.css({
        position: 'relative',
        right: 0,
        display: 'block',
        cursor: 'pointer',
        userSelect: 'none',
    });

    this.hide();

    $messageBox.animate({left: `-=${width}px`}, 300, function () {
        timeoutID = setTimeout(self.hide, timeout, 300, true);
    });
}

let Notifier = function (selector, timeout) {
    let $container = $(selector);

    this.addMessage = function (text, type, callback = null) {
        return new Message($container, text, type, timeout, callback);
    }
}