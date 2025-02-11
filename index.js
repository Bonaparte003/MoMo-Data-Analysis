document.addEventListener('DOMContentLoaded', function () {
    const logo = document.querySelector('.logo');
    const navLinks = document.querySelectorAll('.nav-link');
    const navLinkTexts = document.querySelectorAll('.nav-link p');
    const home = document.querySelector('.home-section');
    const addFile = document.querySelector('.Add-file-section');
    const print = document.querySelector('.print-section');
    const budget = document.querySelector('.budget-section');
    const bot = document.querySelector('.bot-section');
    const settings = document.querySelector('.settings-section');
    const fileInput = document.getElementById('file');
    let file_content = '';

    // Function to show loading overlay
    function showLoading(message) {
        let loadingDiv = document.getElementById('loading-overlay');
        if (!loadingDiv) {
            loadingDiv = document.createElement('div');
            loadingDiv.id = 'loading-overlay';
            loadingDiv.innerHTML = `<div class="loading-message">${message}</div>`;
            document.body.appendChild(loadingDiv);
        }
        loadingDiv.style.display = 'flex';
    }

    // Function to hide loading overlay
    function hideLoading() {
        const loadingDiv = document.getElementById('loading-overlay');
        if (loadingDiv) {
            loadingDiv.style.display = 'none';
        }
    }

    // Function to show a section
    function showSection(sectionToShow) {
        const sections = [home, addFile, print, budget, bot, settings];
        sections.forEach(section => section.style.display = 'none');
        sectionToShow.style.display = 'flex';
    }

    // Function to activate navigation link
    function activateNavLink(navLinkToActivate) {
        navLinks.forEach(navLink => navLink.classList.remove('nav-link_activated'));
        navLinkToActivate.classList.add('nav-link_activated');
    }

    // Function to hide/show text
    function hideInfo() {
        navLinkTexts.forEach(navLinkText => {
            navLinkText.style.display = navLinkText.style.display === 'none' ? 'flex' : 'none';
        });
    }

    // Function to show alert messages
    function showAlert(message, isError = false) {
        const alertBox = document.createElement('div');
        alertBox.className = `custom-alert ${isError ? 'error' : ''}`;
        alertBox.textContent = message;
        document.body.appendChild(alertBox);
        alertBox.classList.add('show');
        setTimeout(() => {
            alertBox.classList.remove('show');
            document.body.removeChild(alertBox);
        }, 3000);
    }

    // Handle file upload and database fetch
    fileInput.addEventListener('change', async function (event) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = async function (e) {
            file_content = e.target.result;

            if (file_content) {
                showLoading('Uploading file...');
                try {
                    const response = await fetch('http://127.0.0.1:8000/file', {
                        method: 'POST',
                        headers: { 'Content-Type': 'text/plain' },
                        body: file_content,
                    });

                    if (!response.ok) throw new Error('File upload failed.');
                    
                    const responseData = await response.json();
                    hideLoading();
                    showAlert('File uploaded successfully!');

                    if (responseData.status === 'success') {
                        showLoading('Fetching database results...');
                        try {
                            const databaseResponse = await fetch('c');
                            if (!databaseResponse.ok) throw new Error('Database fetch failed.');

                            const databaseData = await databaseResponse.json();
                            hideLoading();
                            console.log('Database data:', databaseData);
                        } catch (error) {
                            hideLoading();
                            showAlert(`Error fetching database: ${error.message}`, true);
                        }
                    }
                } catch (error) {
                    hideLoading();
                    showAlert(`Error: ${error.message}`, true);
                }
            }
        };
        reader.readAsText(file);
    });

    // Handle navigation clicks
    logo.addEventListener('click', hideInfo);
    navLinks.forEach((navLink, index) => {
        navLink.addEventListener('click', () => {
            activateNavLink(navLink);
            const sections = [home, addFile, print, budget, bot, settings];
            showSection(sections[index]);
        });
    });

    // Set initial section
    showSection(addFile);
    activateNavLink(navLinks[1]);
});
