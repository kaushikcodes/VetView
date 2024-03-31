document.getElementById('stoolCheckerForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var image = document.getElementById('imageUpload').files[0];
    if (image) {
      // Create FormData object
      var formData = new FormData();
      // Append the file named 'stoolImage' to the form data
      formData.append('stoolImage', image);
      // Log to console or handle the file upload via AJAX
      console.log('Image file to upload:', image);
      // Add your AJAX upload code here
    }
  });
  