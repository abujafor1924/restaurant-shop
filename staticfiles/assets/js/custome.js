let autocomplete;

function initAutoComplete() {
    const inputElement = document.getElementById("id_address");

    if (!inputElement) {
        console.error("Error: Address input field not found!");
        return;
    }

    autocomplete = new google.maps.places.Autocomplete(inputElement, {
        types: ["geocode", "establishment"],
        componentRestrictions: { country: ["bd"] },
    });

    autocomplete.addListener("place_changed", onPlaceChanged);
}

function onPlaceChanged() {
    if (!autocomplete) {
        console.error("Error: Autocomplete is not initialized.");
        return;
    }

    const place = autocomplete.getPlace();
    if (!place.geometry) {
        console.warn("Warning: No geometry found for the selected place.");
        return;
    }

    const latitude = place.geometry.location.lat();
    const longitude = place.geometry.location.lng();

    console.log("Latitude:", latitude);
    console.log("Longitude:", longitude);
   


    document.getElementById("id_latitude").value = latitude;
    document.getElementById("id_longitude").value = longitude;

    let country = "";
    let state = "";
    let city = "";
    let pincode = "";

    for (let i = 0; i < place.address_components.length; i++) {
        const component = place.address_components[i];
        const types = component.types;

        if (types.includes("country")) {
            country = component.long_name;
        }
        if (types.includes("administrative_area_level_1")) {
            state = component.long_name;
        }
        if (types.includes("locality") || types.includes("administrative_area_level_2")) {
            city = component.long_name;
        }
        if (types.includes("postal_code")) {
            pincode = component.long_name;
        }
    }

    if (country) document.getElementById("id_country").value = country;
    if (state) document.getElementById("id_state").value = state;
    if (city) document.getElementById("id_city").value = city;
    if (pincode) document.getElementById("id_pin_code").value = pincode;
}

document.addEventListener("DOMContentLoaded", function () {
    if (typeof google === "undefined" || !google.maps || !google.maps.places) {
        console.error("Error: Google Maps API is not loaded.");
        return;
    }
    initAutoComplete();
});


