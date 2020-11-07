// static/main.js

// Get Stripe publishable key
fetch("/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);
  
  // new
  // Event handler
  document.getElementById("pay").addEventListener("click", () => {
    // Get Checkout Session ID
    fetch(`/create-checkout-session/?slug=${slug}&quantity=${quantity_value}`)
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId, })
    })
    .then((res) => {
      console.log(res);
    });
  });
});