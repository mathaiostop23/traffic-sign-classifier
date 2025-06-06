// Modern Traffic Sign Classifier JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeThemeToggle();
    initializeFileUpload();
    initializeFormHandling();
    initializeAnimations();
    initializeNavigation();
});

// Theme Toggle Functionality
function initializeThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    
    // Check for saved theme preference or default to light mode
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    if (currentTheme === 'dark') {
        body.classList.add('dark-mode');
        updateThemeIcon(true);
    }
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            body.classList.toggle('dark-mode');
            const isDark = body.classList.contains('dark-mode');
            
            // Save theme preference
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            updateThemeIcon(isDark);
        });
    }
}

function updateThemeIcon(isDark) {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        const icon = themeToggle.querySelector('i');
        if (icon) {
            icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
        }
    }
}

// File Upload with Drag & Drop
function initializeFileUpload() {
    const fileInput = document.getElementById('file');
    const fileLabel = document.getElementById('file-label');
    const selectedFile = document.getElementById('selected-file');
    const removeFileBtn = document.getElementById('remove-file');
    
    if (!fileInput || !fileLabel) return;
    
    // File input change handler
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop handlers
    fileLabel.addEventListener('dragover', handleDragOver);
    fileLabel.addEventListener('dragenter', handleDragEnter);
    fileLabel.addEventListener('dragleave', handleDragLeave);
    fileLabel.addEventListener('drop', handleDrop);
    
    // Remove file handler
    if (removeFileBtn) {
        removeFileBtn.addEventListener('click', clearFileSelection);
    }
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        displaySelectedFile(file);
    }
}

function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
}

function handleDragEnter(event) {
    event.preventDefault();
    event.stopPropagation();
    event.currentTarget.classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    event.stopPropagation();
    event.currentTarget.classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    event.currentTarget.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        
        // Validate file type
        if (isValidFileType(file)) {
            const fileInput = document.getElementById('file');
            fileInput.files = files;
            displaySelectedFile(file);
        } else {
            showNotification('Please select a valid image file (JPG, PNG, WEBP)', 'error');
        }
    }
}

function isValidFileType(file) {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    return allowedTypes.includes(file.type);
}

function displaySelectedFile(file) {
    const selectedFileDiv = document.getElementById('selected-file');
    const fileNameSpan = document.getElementById('file-name');
    const fileSizeSpan = document.getElementById('file-size');
    
    if (selectedFileDiv && fileNameSpan && fileSizeSpan) {
        fileNameSpan.textContent = file.name;
        fileSizeSpan.textContent = formatFileSize(file.size);
        selectedFileDiv.classList.add('show');
        
        // Update upload label
        const fileLabel = document.getElementById('file-label');
        if (fileLabel) {
            const uploadText = fileLabel.querySelector('.upload-text');
            const uploadSubtext = fileLabel.querySelector('.upload-subtext');
            if (uploadText) uploadText.textContent = 'File selected successfully!';
            if (uploadSubtext) uploadSubtext.textContent = 'Click "Analyze Traffic Sign" to continue';
        }
    }
}

function clearFileSelection() {
    const fileInput = document.getElementById('file');
    const selectedFileDiv = document.getElementById('selected-file');
    const fileLabel = document.getElementById('file-label');
    
    if (fileInput) fileInput.value = '';
    if (selectedFileDiv) selectedFileDiv.classList.remove('show');
    
    // Reset upload label
    if (fileLabel) {
        const uploadText = fileLabel.querySelector('.upload-text');
        const uploadSubtext = fileLabel.querySelector('.upload-subtext');
        if (uploadText) uploadText.textContent = 'Choose a file or drag and drop';
        if (uploadSubtext) uploadSubtext.textContent = 'Supports JPG, PNG, WEBP (Max 10MB)';
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Form Handling
function initializeFormHandling() {
    const form = document.getElementById('prediction-form');
    const predictBtn = document.getElementById('predict-btn');
    const loading = document.getElementById('loading');
    
    if (form) {
        form.addEventListener('submit', function(event) {
            const fileInput = document.getElementById('file');
            
            if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
                event.preventDefault();
                showNotification('Please select an image file first', 'warning');
                return;
            }
            
            const file = fileInput.files[0];
            
            // Validate file size (10MB limit)
            if (file.size > 10 * 1024 * 1024) {
                event.preventDefault();
                showNotification('File size must be less than 10MB', 'error');
                return;
            }
            
            // Show loading state
            if (loading && predictBtn) {
                loading.classList.add('show');
                predictBtn.disabled = true;
                predictBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
            }
        });
    }
}

// Animations
function initializeAnimations() {
    // Add entrance animations to elements
    const animatedElements = document.querySelectorAll('.fade-in, .slide-up');
    
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animationDelay = '0s';
                    entry.target.style.animationFillMode = 'forwards';
                }
            });
        }, { threshold: 0.1 });
        
        animatedElements.forEach(el => {
            observer.observe(el);
        });
    }
    
    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Navigation
function initializeNavigation() {
    // Mobile menu toggle (if needed in future)
    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;
    
    // Hide/show navbar on scroll
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    });
    
    // Add active class to current page navigation
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// Notification System
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notif => notif.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${getNotificationIcon(type)}"></i>
            <span>${message}</span>
            <button class="notification-close">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 400px;
    `;
    
    // Add to DOM
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        hideNotification(notification);
    }, 5000);
    
    // Close button handler
    const closeBtn = notification.querySelector('.notification-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => hideNotification(notification));
    }
}

function hideNotification(notification) {
    notification.style.transform = 'translateX(100%)';
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 300);
}

function getNotificationIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function getNotificationColor(type) {
    const colors = {
        'success': '#10B981',
        'error': '#EF4444',
        'warning': '#F59E0B',
        'info': '#3B82F6'
    };
    return colors[type] || '#3B82F6';
}

// Example interaction handlers
function handleExampleClick(signType) {
    showNotification(`Click "Choose a file" to upload a ${signType} image`, 'info');
    
    // Scroll to upload section
    const uploadSection = document.querySelector('.upload-section');
    if (uploadSection) {
        uploadSection.scrollIntoView({ behavior: 'smooth' });
    }
}

// Add example click handlers
document.addEventListener('DOMContentLoaded', function() {
    const exampleItems = document.querySelectorAll('.example-item');
    exampleItems.forEach(item => {
        item.addEventListener('click', function() {
            const signType = this.getAttribute('data-sign');
            if (signType) {
                handleExampleClick(signType);
            }
        });
    });
});

// Performance optimizations
// Debounce function for scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Lazy loading for images
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[loading="lazy"]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.add('loaded');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
}

// Initialize lazy loading
document.addEventListener('DOMContentLoaded', initializeLazyLoading);

// Error handling for images
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('error', function() {
            this.style.display = 'none';
            console.warn('Failed to load image:', this.src);
        });
    });
});

// Export functions for external use
window.TrafficSignClassifier = {
    showNotification,
    clearFileSelection,
    handleExampleClick
}; 