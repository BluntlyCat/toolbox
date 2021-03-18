let Modal = function () {
    let self = this;

    let modal = $('<div class="modal" tabindex="-1"></div>');
    let modalDialog = $('<div class="modal-dialog"></div>').appendTo(modal);
    let modalContent = $('<div class="modal-content"></div>').appendTo(modalDialog);

    let header = $('<div class="modal-header"></div>').appendTo(modalContent);
    let body = $('<div class="modal-body"></div>').appendTo(modalContent);
    let footer = $('<div class="modal-footer"></div>').appendTo(modalContent);
    let btnGroup = $('<div class="btn-group"></div>').appendTo(footer);


    let modalTitle = $('<h5 class="modal-title"></h5>').appendTo(header);
    let close = $('<button class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>').appendTo(header);

    const init = function () {
        modal.css({'background': 'rgba(0, 0, 0, .85)'});

        modal.click(function (e) {
            if (e.target === modal[0])
                self.closeModal()
        });

        close.click(function () {
            self.closeModal();
        });

        modal.appendTo($('body'));
    }

    this.setTitle = function (title) {
        modalTitle.html(title);
    }

    this.setBody = function (content) {
        body.html('');

        if (content)
            content.appendTo(body);
        else
            footer.css('border', 'none');
    };

    this.addButton = function (button) {
        button.appendTo(btnGroup);
    };

    this.openModal = function (callback) {
        modal.slideDown(function () {
            if (callback instanceof Function)
                callback();
        });
    };

    this.closeModal = function (callback) {
        modal.slideUp(function () {
            modalTitle.html('');
            body.html('');
            btnGroup.html('');

            if (callback instanceof Function)
                callback();
        });
    };

    init();
};