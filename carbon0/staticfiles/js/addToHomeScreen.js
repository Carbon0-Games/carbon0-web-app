// JS function to make a new button
const createBtn = (text) => {
    // detect if the user is on Android or iOS
    if (
        (navigator.userAgent.indexOf("Android") != -1) ||
        (navigator.userAgent.indexOf("like Mac") != -1)
    ) {
        // grab the div we want to add the button to
        buttonDiv = document.getElementById("add-2-home-screen");
        // make the button
        const btn = document.createElement("button");
        btn.innerText = text;
        // add CSS classes
        btn.classList.add("btn");
        btn.classList.add("btn-info");
        // add it to our HTML document
        buttonDiv.appendChild(btn);
        return btn;
    }
}
// call the function
let addBtn = createBtn("Add to Home Screen!");
/*
 * Code to handle the install to the user's home screen.
 * Credit to the MDN PWA Examples Repo on GitHub: 
 * https://github.com/mdn/pwa-examples/blob/master/a2hs/index.js
 */
window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent Chrome 67 and earlier from automatically showing the prompt
    e.preventDefault();
    // Stash the event so it can be triggered later.
    deferredPrompt = e;
    // Update UI to notify the user they can add to home screen
    addBtn.style.display = 'block';

    addBtn.addEventListener('click', (e) => {
        // hide our user interface that shows our A2HS button
        addBtn.style.display = 'none';
        // Show the prompt
        deferredPrompt.prompt();
        // Wait for the user to respond to the prompt
        deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                console.log('User accepted the A2HS prompt');
            } else {
                console.log('User dismissed the A2HS prompt');
            }
            deferredPrompt = null;
        });
    });
});
