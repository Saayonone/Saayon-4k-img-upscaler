const imageInput = document.getElementById("imageInput");
const uploadBtn = document.getElementById("uploadBtn");
const resultDiv = document.getElementById("result");
const upscaledImage = document.getElementById("upscaledImage");
const downloadBtn = document.getElementById("downloadBtn");

// Load TensorFlow.js model (Make sure you use a valid model here)
async function loadModel() {
  // Load the pre-trained model here (this is an example; change it according to your model's path)
  return await tf.loadGraphModel('https://example.com/path/to/your/model.json');
}

// Function to upscale image
async function upscaleImage(model, image) {
  const tensor = tf.browser.fromPixels(image).toFloat();
  const resized = tf.image.resizeBilinear(tensor, [tensor.shape[0] * 2, tensor.shape[1] * 2]); // Resize the image

  const output = model.predict(resized.expandDims(0));
  const upscaledTensor = output.squeeze().clipByValue(0, 255).toInt();

  return await tf.browser.toPixels(upscaledTensor);
}

uploadBtn.addEventListener("click", async function() {
  if (!imageInput.files.length) {
    alert("Please select an image first.");
    return;
  }

  const file = imageInput.files[0];
  const img = document.createElement("img");
  img.src = URL.createObjectURL(file);
  img.onload = async () => {
    const model = await loadModel();
    const upscaledPixels = await upscaleImage(model, img);
    const upscaledCanvas = document.createElement("canvas");
    upscaledCanvas.width = img.width * 2; // Double the size for upscaling
    upscaledCanvas.height = img.height * 2;
    const ctx = upscaledCanvas.getContext("2d");
    ctx.putImageData(new ImageData(upscaledPixels, upscaledCanvas.width, upscaledCanvas.height), 0, 0);

    // Show the upscaled image
    upscaledImage.src = upscaledCanvas.toDataURL();
    resultDiv.style.display = "block"; // Show result section
    downloadBtn.style.display = "inline-block"; // Show download button

    // Set up the download button
    downloadBtn.onclick = () => {
      const link = document.createElement('a');
      link.href = upscaledImage.src;
      link.download = 'upscaled_image.png'; // Change the file name if needed
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    };
  };
});
