/*!
* Start Bootstrap - Creative v7.0.7 (https://startbootstrap.com/theme/creative)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-creative/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {
    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }
    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    // Activate SimpleLightbox plugin for portfolio items
    new SimpleLightbox({
        elements: '#portfolio a.portfolio-box'
    });

    // Pie Chart
    const ctx = document.getElementById('pie-chart').getContext('2d');

    // Initial data for the pie chart
    const initialData = {
        labels: ['Male', 'Female', 'Neutral'],
        datasets: [{
            label: 'Gender Distribution',
            data: [30, 40, 30], // Initial dummy values
            backgroundColor: [
                'rgba(90, 172, 216)', // Blue for Male
                'rgba(231, 75, 75)', // Red for Female
                'rgba(255, 207, 86)' // Yellow for Neutral
            ],
            borderColor: [
                'rgba(7, 161, 244)',
                'rgba(243, 20, 20)',
                'rgba(246, 178, 7)'
            ],
            borderWidth: 1
        }]
    };

    // Create the initial pie chart
    let pieChart = new Chart(ctx, {
        type: 'pie',
        data: initialData,
        options: {
            title: {
                display: true,
                text: 'Gender Distribution'
            }
        }
    });

    // Input and button elements
    const inputText = document.getElementById('input-text');
    const outputText = document.getElementById('output-text');
    const detectBtn = document.getElementById('detect-btn');
    const convertBtn1 = document.getElementById('convert-btn1');
    const convertBtn2 = document.getElementById('convert-btn2');
    const convertBtn3 = document.getElementById('convert-btn3');

    // Detect button
    detectBtn.addEventListener('click', () => {
        fetch('/detect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: inputText.value })
        })
        .then(response => response.json())
        .then(data => {
            // Update the pie chart with the returned percentages
            updatePieChart(data.labels, data.datasets[0].data);
        })
        .catch(error => console.error('Error:', error)); // Handle errors
    });

    // Convert button function
    const convertText = (gender) => {
        fetch(`/convert/${gender}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: inputText.value })
        })
        .then(response => response.json())
        .then(data => {
            outputText.value = data.converted_text;  // Update the output text box with the converted text
        })
        .catch(error => console.error('Error:', error)); // Handle errors
    };

    // Event listeners for convert buttons
    convertBtn1.addEventListener('click', () => convertText('Male'));
    convertBtn2.addEventListener('click', () => convertText('Female'));
    convertBtn3.addEventListener('click', () => convertText('Neutral'));

    // Update pie chart
    const updatePieChart = (labels, data) => {
        if (pieChart) pieChart.destroy();
        pieChart = new Chart(ctx, { 
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: ['#5AACD8', '#E74B4B', '#FFCF56'],
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'top' },
                }
            }
        });
    };

    // Feedback form submission
    window.submitFeedback = function(event) {
        event.preventDefault(); // Prevent the default form submission

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;

        // Send feedback data to the server
        fetch('/submit-feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, message })
        })
        .then(response => {
            return response.json().then(data => {
                if (response.ok) {
                    document.getElementById('submitSuccessMessage').classList.remove('d-none');
                    document.getElementById('contactForm').reset(); // Reset the form
                } else {
                    console.error('Error response:', data); // Log the error response
                    document.getElementById('submitErrorMessage').classList.remove('d-none');
                }
            });
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('submitErrorMessage').classList.remove('d-none');
        });
    };
});