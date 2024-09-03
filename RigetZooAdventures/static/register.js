function termsSubmit() {
    document.getElementById("submit").disabled = true;
}
function activateSubmit(element) {
    var email = document.getElementById('email');
    var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if (element.checked) {
        if (!filter.test(email.value)) {
            alert('Please provide a valid email address');
            email.focus;
        }
        else {
            document.getElementById("submit").disabled = false;
            document.getElementById("terms").value = "true";
        }
    }

document.getElementById("show-password").addEventListener("click", myFunction);

function myFunction() {
    var x = document.getElementById("show-password"); // Only Works on Microsoft Edge
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }
}