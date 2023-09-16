"use strict";

let request = null;

$(document).ready(() => {
  let rating = 0;

  // initialize the star rating system
  $(".bi-star").hover(function () {
    $(this).addClass("bi-star-fill").removeClass("bi-star");
    $(this).prevAll().addClass("bi-star-fill").removeClass("bi-star");
    $(this).nextAll().addClass("bi-star").removeClass("bi-star-fill");

    rating = $(this).index() + 1;
  });

  $("#rating-submit").click((e) => {
    if (request != null) {
      request.abort();
    }

    $("#rating-submit").prop('disabled', true);
    $("#rating-submit").addClass("disabled");

    const borrowOrLend = $("#rating-submit").attr("name");
    let url = "/rateuser/" + borrowOrLend + "submit";

    let today = new Date();
    const offset = today.getTimezoneOffset();
    today = new Date(today.getTime() - offset * 60 * 1000);
    today = today.toISOString().split("T")[0];

    const csrf_token = $('input[name="csrf_token"]').val();
    request = $.ajax({
      type: "POST",
      url: url,
      data: {
        rating: rating,
        msg: $("#rating-comments").val(),
        date_rated: today
      },
      headers: {
        "X-CSRFToken": csrf_token,
      },
      success: window.location.href = "/listings"
    });
  });
});

function disableBtn(id) {
  const element = document.getElementById(id);
  element.disabled = true;
  element.classList.add("disabled");
}
