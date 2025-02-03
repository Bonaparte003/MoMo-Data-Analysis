document.addEventListener('DOMContentLoaded', function() {
    const logo = document.querySelector('.logo');
    const navLinks = document.querySelectorAll('.nav-link');
    const navLinkTexts = document.querySelectorAll('.nav-link p');
    const home = document.querySelector('.home-section');
    const addFile = document.querySelector('.Add-file-section');
    const print = document.querySelector('.print-section');
    const budget = document.querySelector('.budget-section');
    const bot = document.querySelector('.bot-section');
    const settings = document.querySelector('.settings-section');
    var file_content = '';

    function showSection(sectionToShow) {
        const sections = [home, addFile, print, budget, bot, settings];
        sections.forEach(section => section.style.display = 'none');
        sectionToShow.style.display = 'block';
    }

    function activateNavLink(navLinkToActivate) {
        navLinks.forEach(navLink => navLink.classList.remove('nav-link_activated'));
        navLinkToActivate.classList.add('nav-link_activated');
    }

    function hideInfo() {
        navLinkTexts.forEach(navLinkText => {
            if (navLinkText.style.display === 'none') {
                navLinkText.style.display = 'block';
            } else {
                navLinkText.style.display = 'none';
            }
        });
    }

    document.getElementById('file').addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) { // Define the onload event handler
                const fileContent = e.target.result; // Get the file content
                var file_content = fileContent; // Display the file content
                console.log(file_content); // Log the file content to the console
            };
            reader.readAsText(file); // Read the file as text
        }
    });

    logo.addEventListener('click', hideInfo);

    navLinks.forEach((navLink, index) => {
        navLink.addEventListener('click', () => {
            activateNavLink(navLink);
            switch (index) {
                case 0: showSection(home); break;
                case 1: showSection(addFile); break;
                case 2: showSection(print); break;
                case 3: showSection(budget); break;
                case 4: showSection(bot); break;
                case 5: showSection(settings); break;
            }
        });
    });

    showSection(addFile);
    activateNavLink(navLinks[1]);
});