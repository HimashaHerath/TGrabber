const timestamp = new Date().getTime();
fetch(`/static/images/images.txt?t=${timestamp}`)
  .then(response => response.text())
  .then(text => {
    const imageLinks = text.split("\n");
    const imageContainer = document.getElementById("image-container");
    imageLinks.forEach(link => {
      const image = document.createElement("img");
      image.src = link;
      imageContainer.appendChild(image);
    });
  });
