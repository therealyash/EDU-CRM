document.addEventListener('DOMContentLoaded', function() {
    const contactList = document.querySelector('.contact-list');
    const form = document.getElementById('contactForm');
    const addContactBtn = document.querySelector('.add-contact-btn');

    // Contact form functionality
    addContactBtn.addEventListener('click', function() {
        const wrapper = document.createElement('div');
        wrapper.className = 'contact-row-wrapper';
        
        const row = document.createElement('div');
        row.className = 'contact-row';
        row.innerHTML = `
            <input type="email" placeholder="Contact Email" class="contact-email" required>
            <input type="text" placeholder="First Name" class="contact-firstname" required>
            <input type="text" placeholder="Last Name" class="contact-lastname" required>
            <input type="tel" placeholder="Phone Number" class="contact-phone" pattern="[0-9]{10}" title="Please enter a valid 10-digit phone number">
        `;

        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.className = 'remove-contact-btn';
        removeBtn.setAttribute('aria-label', 'Remove contact');
        removeBtn.textContent = '×';
        
        wrapper.appendChild(row);
        wrapper.appendChild(removeBtn);
        contactList.appendChild(wrapper);

        // Add event listener to remove button
        removeBtn.addEventListener('click', function() {
            if (contactList.children.length > 1) {
                wrapper.remove();
            }
        });

        // Add phone number formatting
        const phoneInput = row.querySelector('.contact-phone');
        phoneInput.addEventListener('input', function(e) {
            // Remove any non-digit characters
            let value = e.target.value.replace(/\D/g, '');
            
            // Truncate to 10 digits if longer
            if (value.length > 10) {
                value = value.slice(0, 10);
            }
            
            e.target.value = value;
        });
    });

    // Handle form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Collect all contact data
        const contacts = [];
        const contactRows = contactList.querySelectorAll('.contact-row');
        
        contactRows.forEach(row => {
            const inputs = row.querySelectorAll('input');
            contacts.push({
                email: inputs[0].value,
                firstName: inputs[1].value,
                lastName: inputs[2].value,
                phoneNumber: inputs[3].value
            });
        });

        const formData = {
            contacts: contacts,
            subscriptionType: document.querySelector('select[name="subscription_type"]').value
        };

        // Log the collected data (replace with your actual submission logic)
        console.log('Form Data:', formData);
        
        // Here you would typically send the data to your server
        // For now, we'll just show an alert
        alert('Form submitted successfully!');
    });

    // Add event listener to the initial remove button
    const initialRemoveBtn = document.querySelector('.remove-contact-btn');
    if (initialRemoveBtn) {
        initialRemoveBtn.addEventListener('click', function() {
            if (contactList.children.length > 1) {
                this.closest('.contact-row-wrapper').remove();
            }
        });
    }

    // Add phone number formatting to initial phone input
    const initialPhoneInput = document.querySelector('.contact-phone');
    if (initialPhoneInput) {
        initialPhoneInput.addEventListener('input', function(e) {
            // Remove any non-digit characters
            let value = e.target.value.replace(/\D/g, '');
            
            // Truncate to 10 digits if longer
            if (value.length > 10) {
                value = value.slice(0, 10);
            }
            
            e.target.value = value;
        });
    }
});
