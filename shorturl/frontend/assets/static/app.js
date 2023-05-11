(function () {
  "use strict";

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll(".needs-validation");

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener(
      "submit",
      function (event) {
        event.preventDefault();

        if (!form.checkValidity()) {
          event.stopPropagation();
        } else {
          try {
            let fd = new FormData(form);
            let success_alert_box = document.getElementById("success_alert");
            let error_alert_box = document.getElementById("error_alert");

            fetch("/post/", {
              method: "POST",
              body: JSON.stringify({ long_url: fd.get("long_url") }),
              headers: {
                "Content-Type": "application/json",
              },
            })
              .then((response) => response.json())
              .then((json_response) => {
                error_alert_box.classList.add("d-none");
                success_alert_box.classList.add("d-none");

                if (json_response.success == true) {
                  let a = document.getElementById("success_message");
                  a.href = "/" + json_response.message.short_url;
                  success_alert_box.classList.remove("d-none");
                } else {
                  let span = document.getElementById("error_message");
                  span.innerText = json_response.message;
                  error_alert_box.classList.remove("d-none");
                }
              })
              .catch((error) => {
                let span = document.getElementById("error_message");
                error_alert_box.classList.add("d-none");
                success_alert_box.classList.add("d-none");
                span.innerText = "Unexpected error contacting backend.";
                error_alert_box.classList.remove("d-none");
              });
          } catch (e) {
            event.preventDefault();
            event.stopPropagation();
            let span = document.getElementById("error_message");
            error_alert_box.classList.add("d-none");
            success_alert_box.classList.add("d-none");
            span.innerText = "Unexpected error contacting backend.";
            error_alert_box.classList.remove("d-none");
          }
        }

        form.classList.add("was-validated");
      },
      false
    );
  });
})();
