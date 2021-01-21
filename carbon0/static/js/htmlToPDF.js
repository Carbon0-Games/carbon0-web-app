const createPDF = (qrCodeImage, missionAction, missionCategory) => {
    // get the DOM elements needed to make the PDF
    const code = document.getElementById(qrCodeImage);
    // Create and save a new PDF on the client machine
    let pdf = new jsPDF();
    // find the sign for trackers in this Mission's category
    const categorySign = {
        "R": "{% static 'images/Sticker_Recycling.png' %}",
        "D": "{% static 'images/Sticker_Diet.png' %}",
        "T": url('../images/Sticker_Transport.png'),
        "U": url('images/Sticker_Utilities.png')
    };
    // make an image in HTML from the image URL
    const categoryImgURL = categorySign[missionCategory];
    const categoryImg = document.createElement('img'); 
    categoryImg.src =  categoryImgURL;
    // add the sign for the mission to the PDF
    pdf.addImage(categoryImg, format='PNG', x=0, y=0);
    // add the QR code for the specific mission to PDF
    pdf.addImage(code, format='PNG', x=0, y=0);
    // title and save the PDF
    pdf.text(missionAction, x=3, y=45);
    pdf.save(qrCodeImage);
}