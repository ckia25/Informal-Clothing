"use strict";

/* ----------------------------------------------------------------- */

window.onload = () => {
  // load modal for invalid listing creation
  if (!($('#listingPageModel').length)) return;
  const newListingPageModal = new bootstrap.Modal("#listingPageModel");
  newListingPageModal.show();
};

