"use strict";

function handleResponse(response) {
  $("#listingcardsID").html(response);
  // remove spinner
  $("#loadingListings").html('');
}

function addSpinner() {
  let str = '<div class="spinner-border text-dark mb-3" role="status"> <span class="sr-only"></span></div>';
  $("#loadingListings").html(str);
}

let search = "";

function encodeURIList(list) {
  let url = "";
  for (var i = 0; i < list.length; i++) {
    if (i > 0) {
      url += ",";
    }
    url += encodeURIComponent(list[i]);
  }
  return url;
}

let request = null;

// handles all of the filtering
function getFilteredResults() {
  let category = $("input[name='categoryfilter']:checked").val();
  let subcategories = $("input[name='subcategoryfilter']:checked")
    .map(function () {
      return $(this).val();
    })
    .get();
  let sizes = $("input[name='sizefilter']:checked")
    .map(function () {
      return $(this).val();
    })
    .get();
  let minprice = $("#minPrice").val();
  let maxprice = $("#maxPrice").val();
  let sort = $("input[name='sortfilter']:checked").val();

  category = encodeURIComponent(category);

  let url = "/listings/results?category=" + category;
  url += "&subcategories=" + encodeURIList(subcategories);
  url += "&sizes=" + encodeURIList(sizes);
  url += "&minprice=" + encodeURIComponent(String(minprice));
  url += "&maxprice=" + encodeURIComponent(String(maxprice));
  url += "&sort=" + encodeURIComponent(sort);
  url += "&search=" + encodeURIComponent(search);

  if (request != null) {
    request.abort();
  }


  // Before add the spinner
  addSpinner();
  request = $.ajax({
    type: "GET",
    url: url,
    success: handleResponse,
  });
}

// Allows this sticky element to stay at the top
function stickyFunction() {
  const stickyElement = document.querySelector(".sticky-element");
  const initialPosition = stickyElement.getBoundingClientRect().top;

  window.addEventListener("scroll", () => {
    const scrollPosition = window.scrollY;

    if (scrollPosition >= initialPosition) {
      stickyElement.classList.add("sticky");
    } else {
      stickyElement.classList.remove("sticky");
    }
  });
}

function setup() {
  getFilteredResults();
  $("input[name='categoryfilter']").on("input", getFilteredResults);
  $("input[name='subcategoryfilter']").on("input", getFilteredResults);
  $("input[name='sizefilter']").on("input", getFilteredResults);
  $("#priceRangeSubmit").click(function (e) {
    e.preventDefault();
    getFilteredResults();
  });
  $("#searchSubmit").click(function (e) {
    e.preventDefault();
    search = $("#searchBar").val();
    getFilteredResults();
  });
  $("input[name='sortfilter']").on("input", getFilteredResults);

  stickyFunction();
}

$("document").ready(setup);
