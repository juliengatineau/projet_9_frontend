function highlightImage(index) {
    console.log('Highlighting image with index:', index);

    // Retirer la classe 'highlight' de toutes les images
    const images = document.querySelectorAll('.image li');
    images.forEach(image => {
        image.classList.remove('highlight');
        console.log('Removing highlight from image with ID:', image.id);
    });

    // Ajouter la classe 'highlight' à l'image correspondante
    const imageElement = document.getElementById('image-' + index);
    if (imageElement) {
        console.log('Adding highlight to image with index:', index);
        setTimeout(() => {
            imageElement.classList.add('highlight');
            console.log('Highlight class added to image with index:', index);
        }, 0);
    } else {
        console.error('Image element not found for index:', index);
    }

    // Retirer la classe 'active' de tous les éléments de la liste
    const items = document.querySelectorAll('.num_id li');
    items.forEach(item => {
        item.classList.remove('active');
        console.log('Removing active from item with ID:', item.id);
    });

    // Ajouter la classe 'active' à l'élément de la liste correspondant
    const itemElement = document.getElementById('num-' + index);
    if (itemElement) {
        itemElement.classList.add('active');
        console.log('Active class added to item with index:', index);
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