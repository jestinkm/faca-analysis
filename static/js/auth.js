/**
 * FaceSecure - Authentication Utilities
 * Helper functions for authentication operations
 */

class AuthUtils {
    /**
     * Make authenticated API request
     * @param {string} url - API endpoint
     * @param {Object} options - Fetch options
     * @returns {Promise<Object>} Response data
     */
    static async authRequest(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            credentials: 'include'
        };

        const response = await fetch(url, { ...defaultOptions, ...options });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Request failed');
        }

        return data;
    }

    /**
     * Show alert message
     * @param {string} message - Alert message
     * @param {string} type - Alert type (success, danger, warning, info)
     * @param {string} containerId - Container element ID
     * @param {number} duration - Duration in ms
     */
    static showAlert(message, type = 'info', containerId = 'alertContainer', duration = 5000) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `<div class="alert alert-${type}">${message}</div>`;

        if (duration > 0) {
            setTimeout(() => {
                container.innerHTML = '';
            }, duration);
        }
    }

    /**
     * Show loading state
     * @param {HTMLElement} element - Element to show loading on
     * @param {boolean} loading - Loading state
     * @param {string} originalText - Original button text
     */
    static setLoading(element, loading, originalText) {
        if (!element) return;

        if (loading) {
            element.disabled = true;
            element.dataset.originalText = element.textContent;
            element.innerHTML = `
                <span class="loading-spinner me-2"></span>
                ${originalText || 'Loading...'}
            `;
        } else {
            element.disabled = false;
            element.textContent = element.dataset.originalText || originalText;
        }
    }

    /**
     * Format date
     * @param {Date|string} date - Date to format
     * @param {string} format - Format string
     * @returns {string} Formatted date
     */
    static formatDate(date, format = 'YYYY-MM-DD HH:mm:ss') {
        const d = new Date(date);
        
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        const hours = String(d.getHours()).padStart(2, '0');
        const minutes = String(d.getMinutes()).padStart(2, '0');
        const seconds = String(d.getSeconds()).padStart(2, '0');
        
        return format
            .replace('YYYY', year)
            .replace('MM', month)
            .replace('DD', day)
            .replace('HH', hours)
            .replace('mm', minutes)
            .replace('ss', seconds);
    }

    /**
     * Format duration
     * @param {number} seconds - Duration in seconds
     * @returns {string} Formatted duration
     */
    static formatDuration(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;

        if (hours > 0) {
            return `${hours}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
        }
        return `${minutes}:${String(secs).padStart(2, '0')}`;
    }

    /**
     * Debounce function
     * @param {Function} func - Function to debounce
     * @param {number} wait - Wait time in ms
     * @returns {Function} Debounced function
     */
    static debounce(func, wait = 300) {
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

    /**
     * Validate email
     * @param {string} email - Email to validate
     * @returns {boolean} Valid email
     */
    static validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    /**
     * Validate password strength
     * @param {string} password - Password to validate
     * @returns {Object} Validation result
     */
    static validatePassword(password) {
        const result = {
            valid: true,
            errors: []
        };

        if (password.length < 8) {
            result.valid = false;
            result.errors.push('Password must be at least 8 characters');
        }

        if (!/[A-Z]/.test(password)) {
            result.valid = false;
            result.errors.push('Password must contain at least one uppercase letter');
        }

        if (!/[a-z]/.test(password)) {
            result.valid = false;
            result.errors.push('Password must contain at least one lowercase letter');
        }

        if (!/[0-9]/.test(password)) {
            result.valid = false;
            result.errors.push('Password must contain at least one number');
        }

        return result;
    }

    /**
     * Get session info
     * @returns {Promise<Object>} Session information
     */
    static async getSessionInfo() {
        try {
            const response = await this.authRequest('/api/auth_status');
            return response;
        } catch (error) {
            console.error('Error getting session info:', error);
            return null;
        }
    }

    /**
     * Check if user is authenticated
     * @returns {boolean} Authentication status
     */
    static isAuthenticated() {
        // Check if session exists (you may need to adjust this based on your session handling)
        return document.cookie.includes('session');
    }

    /**
     * Redirect to login if not authenticated
     */
    static requireAuth() {
        if (!this.isAuthenticated()) {
            window.location.href = '/login';
        }
    }

    /**
     * Logout
     * @returns {Promise<boolean>} Logout success
     */
    static async logout() {
        try {
            await this.authRequest('/logout', { method: 'POST' });
            window.location.href = '/login';
            return true;
        } catch (error) {
            console.error('Logout error:', error);
            return false;
        }
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AuthUtils;
}
