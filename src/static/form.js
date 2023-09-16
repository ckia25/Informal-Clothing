'use strict'

let count = 0

/* ----------------------------------------------------------------- */
// let fileArray = [];
// THIS IS A POTENTIAL SOLUTION TO ADDING ONLY FIVE EXTRA FILES
// function showFiles() {
//   if (fileArray.length > 5) {
//     $('#maxFiles').html('<div>' + 'Max 5 additional images' + '</div>');
//     alert("You are only allowed to upload 5 additional images");
//   } else {
//     $('#maxFiles').html('');
//     for(var i = 0 ; i < this.files.length ; i++){
//       if (fileArray.length >= 5) {
//         alert('You are only allowed to upload 5 additional images');
//         break;
//       }
//       var fileName = this.files[i].name;
//       fileArray.push(this.files[i]);
//       $('#filenames').append('<div class="name">' + fileName + '</div>');
//     }
//   }

// }

// function setAllAdditionalFiles() {
//   try{
//     for (var i = 0; i < fileArray.length; i++) {
//       var id = '#file'+String(i+1);
//       $(id).val(fileArray[i]);
//     }
//   }
//   catch{
//     alert('error');
//   }


// }
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
        btn.disabled = true;
        btn.classList.add("disabled");
        addSpinner()
      }
      form.classList.add("was-validated");
    }, false);





  // $('#additionalImages').change(showFiles);

  // load modal for invalid listing creation MUST BE AT THE BOTTOM
  // WE NEED TO FIGURE OUT HOW TO INCLUDE THIS WITHOUT IT FAILING
  try{
    const listingformModal = new bootstrap.Modal("#errorModel");
    listingformModal.show();
  } catch{

  }

}

$('document').ready(setup);
