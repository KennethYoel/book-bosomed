$(document).ready(function () {
    const editor = document.getElementById('editor');
    const hiddenInput = document.getElementById('myHtml');
    const form = document.forms.mainform;
    var option = {
        placeholder: 'Compose an epic...',
        theme: 'snow',
        bounds: '#parent'
    };
    var quill = new Quill('#editor', option);
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        console.log(editor.firstChild.innerHTML);
        hiddenInput.value = editor.firstChild.innerHtml;
        this.submit();
    });
});
// Many thanks to James Hibbard-SitePoint Editor for these lines of code.
//# sourceMappingURL=quill.js.map