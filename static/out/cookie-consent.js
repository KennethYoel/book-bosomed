window.cookieconsent.initialise({
    container: document.getElementById('cookieconsent'),
    palette: {
        popup: { background: '#d1ecf1' },
        button: { background: '#ccc' }
    },
    revokable: true,
    onStatusChange: function (status) {
        console.log(this.hasConsented() ? 'enable cookies' : 'disable cookies');
    },
    theme: 'edgeless'
});
//# sourceMappingURL=cookie-consent.js.map