// show when this plant was last updated, and what the status was
export function displayHealthPreview(elemID, lastStatus, lastUpdated) {
    // get the HTML element we'll be making changes to
    let parentElem = document.getElementById(elemID);
        // add an element for the latest health check
    let health = document.createElement("p");
    const healthNode = document.createTextNode(lastStatus);
    health.appendChild(healthNode);
    // add Bootstrap classes to the time element
    let textColor = "";
    if (lastStatus === "Healthy") {
        textColor = "text-success";
    } else if (lastStatus === "Unhealthy") {
        textColor = "text-danger";
    } else if (lastStatus === "Unhealthy") {
        textColor = "text-warning";
    }
    healt.classList.add("card-text");
    health.classList.add(textColor);
    // add the health to the HTML document
    parentElem.appendChild(health);
    // show the last time the plant was updated on the DOM
    let time = document.createElement("p");
    const timeNode = document.createTextNode("Last Updated: " + lastUpdated);
    time.appendChild(timeNode);
    // add Bootstrap classes to the time element
    time.classList.add("card-text");
    time.classList.add("text-dark");
    // add the time to the HTML document
    parentElem.appendChild(time);
}
