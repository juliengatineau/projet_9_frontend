function highlightImage(index) {
    console.log('Highlighting image with index:', index);

    // Retirer la classe 'highlight' de toutes les images
    const images = document.querySelectorAll('.image li');
    images.forEach(image => {
        image.classList.remove('highlight');
        console.log('Removing highlight from image with index:', index);
    });

    // Ajouter la classe 'highlight' à l'image correspondante
    const imageElement = document.getElementById('image-' + index);
    if (imageElement) {
        console.log('Adding highlight to image with index:', index);
        imageElement.classList.add('highlight');
    } else {
        console.error('Image element not found for index:', index);
    }

    // Retirer la classe 'active' de tous les éléments de la liste
    const items = document.querySelectorAll('.num_id li');
    items.forEach(item => {
        item.classList.remove('active');
    });

    // Ajouter la classe 'active' à l'élément de la liste correspondant
    const itemElement = document.getElementById('num-' + index);
    if (itemElement) {
        itemElement.classList.add('active');
    } else {
        console.error('Item element not found for index:', index);
    }
}


// Activer le premier élément au lancement de la page
document.addEventListener('DOMContentLoaded', () => {
    highlightImage(1);
});



function submitForm(index) {
    const imageElement = document.getElementById('image-' + index).querySelector('img');
    const imageUrl = imageElement.src;

    // Remplir le champ caché avec l'URL de l'image
    document.getElementById('image-url').value = imageUrl;

    // Soumettre le formulaire
    document.getElementById('prediction-form').submit();
}