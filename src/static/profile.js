"use strict";

let request = null;
let profileResultsRequest = null;
const username = JSON.parse($("#username_json").data("username"));
console.log(username)

// --------------------------------------------------------------------
// Loading Icon functions
function addSpinner() {
  let str = '<div class="spinner-border text-dark m-1" role="status"> <span class="sr-only"></span></div>';
  $("#loadingMyListings").html(str);
}

function removeSpinner() {
  $("#loadingMyListings").html('');
}
// --------------------------------------------------------------------
// profile results ajax function
function handleProfileResultsResponse(response) {
  $("#profileCards").html(response);
  removeSpinner();
}

function getProfileResults(queryBy) {
  queryBy = encodeURIComponent(queryBy);
  let url = "/profile/" + username + "/results?query=" + queryBy;

  if (profileResultsRequest != null) {
    profileResultsRequest.abort();
  }

  addSpinner();
  profileResultsRequest = $.ajax({
    type: "GET",
    url: url,
    success: handleProfileResultsResponse,
  });
}


// Document Ready
$("document").ready(function () {
  // only should be uncommented for debugging/admin view

  // const pointsModal = new bootstrap.Modal(
  //   document.getElementById("getting_points")
  // );

  // gets the listings for the profile page
  getProfileResults("My Listings"); // default run
  $("ul.nav-tabs > li").click(function(e) {
    e.preventDefault();
    var queryBy = $(this).text().trim();
    $('#listingsHeading').text(queryBy);
    getProfileResults(queryBy);
    $("ul.nav-tabs > li").removeClass("active");
    $(this).addClass("active");
    $(".navbar-toggler").click();
  });



  // GET POINTS FUNCTIONS
  $("#get_points").on("submit", function (e) {
    e.preventDefault();

    if (request != null) {
      request.abort();
    }

    const points = $("#points").val();
    const url = "/profile/getpoints";

    function handlePointsUpdate(response) {
      $("#balance").html(response);
    }

    const csrf_token = $('input[name="csrf_token"]').val();
    request = $.ajax({
      type: "POST",
      url: url,
      data: {
        points: points,
      },
      headers: {
        "X-CSRFToken": csrf_token,
      },
      success: handlePointsUpdate,
    });

    pointsModal.hide();


  });

  try{
    const listingformModal = new bootstrap.Modal("#successModel");
    listingformModal.show();
  } catch{

  }
  // load modal for invalid listing creation MUST BE AT THE BOTTOM
  // WE NEED TO FIGURE OUT HOW TO INCLUDE THIS WITHOUT IT FAILING
  try{
    const editListingModal = new bootstrap.Modal("#errorModel");
    editListingModal.show();
  } catch{
  }

});
