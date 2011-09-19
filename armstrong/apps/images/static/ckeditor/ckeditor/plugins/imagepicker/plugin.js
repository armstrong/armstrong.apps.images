(function() {
    var plugin = {
        exec: function(editor) {
            var media = window.showModalDialog("/images/admin/browse/",null,"dialogWidth:750px;dialogHeight:500px;center:yes; resizable: yes; help: no");
            if (media != false && media != null) {
                editor.insertHtml(media);
            }
        }
    },
    plugin_name='imagepicker';
    CKEDITOR.plugins.add(plugin_name, {
        init: function(editor) {
            editor.addCommand(plugin_name, plugin);
            editor.ui.addButton('ImagePicker', {
                label: 'Insert Image',
                icon: this.path + 'toolBarButton.png',
                command: plugin
            });
        }
    });
})();
