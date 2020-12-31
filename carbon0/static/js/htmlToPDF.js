const createPDF = qrCodeID => {
    // get the DOM element needed to make the PDF
    const element = document.getElementById(qrCodeID);

    // convert the HTML to a PDF in the browser
   let pdf = new jsPDF();
   pdf.addImage(element, format='PNG', x=0, y=0);
   pdf.save(qrCodeID);
}