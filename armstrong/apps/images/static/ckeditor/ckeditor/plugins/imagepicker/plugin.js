(function() {
    var a = {
        exec: function(editor) {
            var media = window.showModalDialog("/images/admin/browse/",null,"dialogWidth:750px;dialogHeight:500px;center:yes; resizable: yes; help: no");
            if (media != false && media != null) {
                editor.insertHtml(media);
            }
        }
    },
    b='imagepicker';
    CKEDITOR.plugins.add(b, {
        init: function(editor) {
            editor.addCommand(b, a);
            editor.ui.addButton('ImagePicker', {
                label: 'Insert Image',
                icon: this.path + 'toolBarButton.png',
                command: b
            });
        }
    });
})();
