const createPDF = (qrCodeImage, missionAction) => {
    // get the DOM elements needed to make the PDF
    const image = document.getElementById(qrCodeImage);
    // Create and save a new PDF on the client machine
    let pdf = new jsPDF();
    pdf.addImage(image, format='PNG', x=0, y=0);
    pdf.text(missionAction, x=3, y=45);
    pdf.save(qrCodeImage);
}