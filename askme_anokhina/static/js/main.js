$(".rating-btn").click(function (ev) {
    $.ajax({
        method: "POST",
        url: "/likeQuestion",
        data: {'question_id': $(this).data('id'), 'action': $(this).data('action')},
        dataType: "json",
        headers: {'X-CSRFToken': csrftoken,
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    }).always(function (data) {
        const $rating = $("#rating-" + $(this).data('id'))
        $rating.text(data.new_rating);

    });
})

$(".rating-btn").click(function (ev) {
    $.ajax({
        method: "POST",
        url: "/likeAnswer",
        data: {'answer_id': $(this).data('id'), 'action': $(this).data('action')},
        dataType: "json",
        headers: {'X-CSRFToken': csrftoken,
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    }).always(function (data) {
        const $rating = $("#rating-" + $(this).data('id'))
        $rating.text(data.new_rating);

    });
})


$(".answer-correct").click(function (ev) {
    ev.preventDefault();
    $.ajax({
        method: "POST",
        url: "/correctAnswer",
        data: {'answer_id': $(this).data('id')},
        dataType: "json",
        headers: {'X-CSRFToken': csrftoken}
    }).always(function (data) {
        $(this).checked ^= true;
    });
})