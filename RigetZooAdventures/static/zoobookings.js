// Get the current date and time
var currentDate = new Date();
var currentDateString = currentDate.toISOString().slice(0, 16); // The Format is YYYY-MM-DD

// Set the min attribute of the input field to the current date and time
document.querySelector('.checkin-datetime').setAttribute('min', currentDateString); // Min is removing the previous dates

  // Function to calculate total ticket price
        function calculateTotal() {
            var numAdults = parseInt(document.getElementById("numAdults").value);
            var numChildren = parseInt(document.getElementById("numChildren").value);

            var adultPrice = 18.35;
            var childPrice = 12.75;

            var total = (numAdults * adultPrice) + (numChildren * childPrice);

            alert('Total ticket price: £' + total.toFixed(2));

            return false; // Prevent form submission
        }
