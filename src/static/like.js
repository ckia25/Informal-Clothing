"use strict";

let request = null;

$(document).ready(() => {

    console.log("yoyuo")

    $("#like-submit").click((e) => {
        if (request != null) {
            request.abort();
        }

        // button color changes when liked/unliked
        $("#like-submit").classList.toggle("bi-suit-heart");
        $("#like-submit").classList.toggle("bi-suit-heart-fill");

        const listingid = $('input[name="listingid"]').val();
        const userid = $('input[name="userid"]').val();
        const csrf_token = $('input[name="csrf_token"]').val();

        request = $.ajax({
            type: "POST",
            url: "/likepost",
            data: {
                listingid: listingid,
                userid: userid,
            },
            headers: {
                "X-CSRFToken": csrf_token,
            }
        });
    });
});