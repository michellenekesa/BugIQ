// Form validation functions
const validateForm = (formData) => {
    const errors = [];
    
    // Validate summary
    const summary = formData.get('summary');
    if (!summary || summary.trim().length < 10) {
        errors.push('Summary must be at least 10 characters long');
    }
    
    // Validate component
    const component = formData.get('component');
    if (!component || component.trim().length === 0) {
        errors.push('Component name is required');
    }
    
    return errors;
};

// Error display function
const showErrors = (errors) => {
    const alertContainer = document.getElementById('alert-container');
    if (alertContainer) {
        alertContainer.innerHTML = `
            <div class="alert alert-danger alert-dismissible fade show">
                <ul class="mb-0">
                    ${errors.map(error => `<li>${error}</li>`).join('')}
                </ul>
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
    }
};

// Form submission handler
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prediction-form');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const errors = validateForm(formData);
            
            if (errors.length > 0) {
                showErrors(errors);
                return;
            }
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Prediction failed');
                }
                
                if (data.severity) {
                    const alertContainer = document.getElementById('alert-container');
                    alertContainer.innerHTML = `
                        <div class="alert alert-success alert-dismissible fade show">
                            Prediction successful! Severity: ${data.severity}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    `;
                    
                    // Clear form
                    form.reset();
                    
                    // Reload after delay
                    setTimeout(() => window.location.reload(), 1500);
                }
            } catch (error) {
                showErrors([error.message]);
            }
        });
    }
});