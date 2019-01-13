// const messageAlert = function () {
//       if (document.querySelector('#name').value !== "" && document.querySelector('#email').value !== "" &&
//           document.querySelector('#phone').value !== "" && document.querySelector('#topic').value !== "" &&
//           document.querySelector('#details').value !== "") {
//             alert("Your message has been sent. Redirecting to the home page..")
//       } else {
//       alert("Please, fill in all fields.")}
// }

document.querySelector('#form-contact').addEventListener('submit', function(e) {
      if (e.target.elements.name.value !== '' &&
          e.target.elements.email.value !== '' &&
          e.target.elements.phone.value !== '' &&
          e.target.elements.topic.value !== '' &&
          e.target.elements.details.value !== '') {
            alert("Your message has been sent. Redirecting to the home page..")
      } else {
            alert("Please, fill in all fields.")
      }
})