//
// document.querySelector('#form-contact').addEventListener('submit', function(e) {
//       if (e.target.elements.name.value !== '' &&
//           e.target.elements.email.value !== '' &&
//           e.target.elements.phone.value !== '' &&
//           e.target.elements.topic.value !== '' &&
//           e.target.elements.details.value !== '') {
//             alert("Your message has been sent. Redirecting to the home page..")
//       } else {
//             alert("Please, fill in all fields.")
//       }
// });

document.querySelector('#email').addEventListener('input', function (e) {
      const emailRegExp = /^\S{3,20}@\S{3,20}\.\S{2,10}$/;
      if (e.target.value.match(emailRegExp)) {
            document.querySelector('#emailValidation').innerHTML = "<span style='color: green; font-size: .7em;'>Good email!</span>"
      }
      else {
            document.querySelector('#emailValidation').innerHTML = "<span style='color: red; font-size: .7em;'>Wrong email format!</span>"
      }
});

document.querySelector('#phone').addEventListener('input', function (e) {
      const phoneRegExp = /^[0-9]{4,13}$/;
      if (e.target.value.match(phoneRegExp)) {
            document.querySelector('#phoneValidation').innerHTML = "<span style='color: green; font-size: .7em;'>Good phone number!</span>"
      }
      else {
            document.querySelector('#phoneValidation').innerHTML = "<span style='color: red; font-size: .7em;'>Not valid phone number!</span>"
      }
});