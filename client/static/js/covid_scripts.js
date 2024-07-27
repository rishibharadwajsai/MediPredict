async function uploadImage() {
            const imageInput = document.getElementById('image');
            const file = imageInput.files[0];
            const formData = new FormData();
            formData.append('file', file);
            try{
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            document.getElementById('Output').innerText ="Output : "+ JSON.stringify(result.Prediction);
        }catch (error) {
                console.error('Error:', error);
                document.getElementById("Output").innerText = 'Error: ' + error.message;
            }
        }