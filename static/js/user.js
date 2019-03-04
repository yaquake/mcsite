
document.querySelector('#form-contact').addEventListener('submit', function(e) {
    if (e.target.elements.name.value !== '' &&
        e.target.elements.email.value.match(/^\S{3,20}@\S{3,20}\.\S{2,10}$/) &&
        e.target.elements.phone.value.match(/^[0-9]{4,13}$/) &&
        e.target.elements.topic.value !== '' &&
        e.target.elements.details.value !== '') {
    } else {
        e.preventDefault()
        alert("Please, fill in all fields correctly.")
    }
});

document.querySelector('#email').addEventListener('input', function (e) {
    const emailRegExp = /^\S{3,20}@\S{3,20}\.\S{2,10}$/;
    if (e.target.value.match(emailRegExp)) {
        document.querySelector('#emailValidation').innerHTML =
            "<span style='color: green; font-size: .7em;'>Valid email!</span>"
    }
    else {
        document.querySelector('#emailValidation').innerHTML =
            "<span style='color: red; font-size: .7em;'>Invalid email!</span>"
    }
});

document.querySelector('#phone').addEventListener('input', function (e) {
    const phoneRegExp = /^[0-9]{4,13}$/;
    if (e.target.value.match(phoneRegExp)) {
        document.querySelector('#phoneValidation').innerHTML =
            "<span style='color: green; font-size: .7em;'>Valid phone number!</span>"
    }
    else {
        document.querySelector('#phoneValidation').innerHTML =
            "<span style='color: red; font-size: .7em;'>Invalid phone number!</span>"
    }
});


