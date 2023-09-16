'use strict'
let count = 0;

function addSpinner() {
  let str = '<div class="clearfix"><div class="spinner-border float-end" role="status"><span class="sr-only"></span></div></div>';
  $("#spinner").html(str);
}

function setup(){
  // handle the date stuff
  let today = new Date();
  const offset = today.getTimezoneOffset();
  today = new Date(today.getTime() - offset * 60 * 1000);
  today = today.toISOString().split("T")[0];
  $("#listingDateCreated").val(today);


  // Disabling form submissions if there are invalid fields
  const form = document.getElementById("listing-form");
    if (!form) return;
    form.addEventListener("submit", (event) => {
      // setAllAdditionalFiles();
      const btn = document.getElementById("submitButton");
      if (!form.checkValidity() | count != 0) {
        event.preventDefault();
        event.stopPropagation();
      } else {
        count++;
        btn.disabled=true;
        btn.classList.add("disabled");
        addSpinner();
      }
      form.classList.add("was-validated");
    }, false);

}

$('document').ready(setup);
