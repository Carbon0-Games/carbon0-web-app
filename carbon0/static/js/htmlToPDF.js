
const getPDFData = pdfDataEndpoint => {
    // get the URL for the image needed on the tracking missions PDF
    $(document).ready(function () {
        // get the data on the carbon footprint from the API
        let endpoint = pdfDataEndpoint;
        $.ajax({
            method: "GET",
            url: endpoint,
            success: function (data) {
                // if it all works, then go on to create the PDF
                createPDF(
                    `${data.category}-Sign-${data.missionId}-image`,
                    data.missionTitle, 
                    data.imageURL
                );
            },
            error: function (error_data) {
                console.log(error_data)
            }
        })
    })
    
}

const createPDF = (pdfFileName, missionAction, categoryImgURL) => {
    // first validate we can create the PDF
    if (categoryImgURL !== "/static/No image") {
        // get the DOM elements needed to make the PDF
        const code = document.getElementById(pdfFileName);
        // Create and save a new PDF on the client machine
        let pdf = new jsPDF();
        // make an image in HTML from the image URL
        let categoryImg = document.createElement('img'); 
        categoryImg.setAttribute('src', categoryImgURL);
        // add the sign for the mission to the PDF
        pdf.addImage(categoryImg, x=0, y=0, width=285, height=150);
        // add the QR code for the specific mission to PDF
        pdf.addImage(code, format='PNG', x=170, y=0);
        // title and save the PDF
        pdf.save(pdfFileName);
    }
}
