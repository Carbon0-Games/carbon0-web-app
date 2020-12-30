const createPDF = qrCodeID => {
    // get the DOM element needed to make the PDF
    const element = document.getElementById(qrCodeID);

    // convert the HTML to a PDF in the browser
    const worker = html2pdf();
    worker.from(element).save(qrCodeID);
}