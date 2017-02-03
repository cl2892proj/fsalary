$(function () {
    // Remove Search if user Resets Form or hits Escape!
    $('#main-search-form button[type="reset"]').on('click keyup', function(event) {
        console.log(event.currentTarget);
        if (event.which == 27 && $('#main-search-form').hasClass('active') ||
                $(event.currentTarget).attr('type') == 'reset') {
            closeSearch();
        }
    });

    function closeSearch() {
        var $form = $('#main-search-form.active')
        $form.find('input').val('');
        $('#content').css({"opacity": "1"});
        $form.removeClass('active');
    }

    // Show Search if form is not active // event.preventDefault() is important, this prevents the form from submitting
    $(document).on('click', '#main-search-trigger', function(event) {
        event.preventDefault();
        var $form = $('#main-search-form'),
            $input = $form.find('input');
        $form.addClass('active');
        $('#content').css({"opacity": "0.2"});
        $input.focus();

    });
});
