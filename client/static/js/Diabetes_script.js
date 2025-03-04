// var name;
var age;
var height;
var weight;
var BP;
var Pregnancies;
var Glucose;
var DBF;
var Skinthickness;
var insulin;
async function postInput() {
    const array = {"Pregnancies":Pregnancies,"Glucose":Glucose,	"BloodPressure":BP,	"SkinThickness":Skinthickness,"Insulin":insulin,"Height":height,"Weight":weight,"DiabetesPedigreeFunction":DBF	,"Age":age};

    try {
        const response = await fetch('/get_dprob', {
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

function Submit(){
    // name = document.getElementById("name").value;
    age  = parseInt(document.getElementById("age").value);
    height = parseFloat(document.getElementById("Height").value);
    weight = parseInt(document.getElementById("Weight").value);
    BP = parseInt(document.getElementById("BloodPressure").value);
    Pregnancies = parseInt(document.getElementById("Pregnancies").value);
    Glucose = parseInt(document.getElementById("Glucose").value);
    DBF = parseFloat(document.getElementById("DBF").value);
    Skinthickness = parseInt(document.getElementById("Skinthickness").value);
    insulin = parseInt(document.getElementById("insulin").value);
    postInput();
}