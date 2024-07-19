var name;
var age;
var height;
var weight;
var glucose;
var ap_hi;
var ap_lo;
var cholesterol;

async function postInput() {
    const array = [age, height, weight, ap_hi, ap_lo, cholesterol, glucose];

    try {
        const response = await fetch('/get_probab', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ array: array }),
        });

        if (!response.ok) {
            const errorMessage = await response.text();
            throw new Error(errorMessage || 'Something went wrong');
        }

        const data = await response.json();
        const imgSrc = `data:image/png;base64,${data.image}`;   
        document.getElementById("Output").innerText = 'Severity: ' + data.predicate;
        // document.getElementById("Image").scr = imgsrc;
        img = document.createElement('img');
        img.src = imgSrc;
        img.alt = 'ResultImage';
        img.width = 650;
        img.height = 250;
        var container = document.getElementById("Image");
        container.innerHTML = '';
        container.append(img);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById("Output").innerText = 'Error: ' + error.message;
    }
}

function submitForm() {
    name = document.getElementById("name").value;
    age = parseInt(document.getElementById("age").value);
    height = parseInt(document.getElementById("height").value);
    weight = parseInt(document.getElementById("weight").value);
    glucose = parseInt(document.getElementById("glucose").value);
    ap_hi = parseInt(document.getElementById("ap_hi").value);
    ap_lo = parseInt(document.getElementById("ap_lo").value);
    cholesterol = parseInt(document.getElementById("cholesterol").value);
    postInput();
}
