/**
 * Main application Shortify
 */

class ShortifyApp {
    constructor() {
        this.init();
    }

    init() {
        this.cacheElements();
        this.attachEventListeners();
        this.loadHistory();
    }

    /**
     * Caching DOM elements
     */
    cacheElements() {
        this.form = document.getElementById('shortenForm');
        this.urlInput = document.getElementById('urlInput');
        this.urlError = document.getElementById('urlError');
        this.resultContainer = document.getElementById('resultContainer');
        this.originalUrlDisplay = document.getElementById('originalUrl');
        this.shortUrlDisplay = document.getElementById('shortUrl');
        this.shortCodeDisplay = document.getElementById('shortCode');
        this.copyBtn = document.getElementById('copyBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.historyContainer = document.getElementById('historyContainer');
        this.toast = document.getElementById('toast');
        this.submitBtn = this.form.querySelector('button[type="submit"]');
        this.btnText = this.submitBtn.querySelector('.btn-text');
        this.btnLoader = this.submitBtn.querySelector('.btn-loader');
    }

    /**
     * Connecting event handlers
     */
    attachEventListeners() {
        this.form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        this.copyBtn.addEventListener('click', () => this.copyToClipboard());
        this.resetBtn.addEventListener('click', () => this.resetForm());
        this.urlInput.addEventListener('input', () => this.clearError());
    }

    /**
     * Processing form submission
     */
    async handleFormSubmit(e) {
        e.preventDefault();

        const url = this.urlInput.value.trim();

        // Validation
        if (!this.validateURL(url)) {
            this.showError('Please enter a valid URL.');
            return;
        }

        await this.shortenURL(url);
    }

    /**
     * URL shortening
     */
    async shortenURL(url) {
        try {
            this.setLoading(true);

            const result = await api.shortenURL(url);

            // Display result
            this.displayResult(result);

            // Save to history
            this.saveToHistory(result);

            // Refresh history
            this.loadHistory();

            this.showToast('✅ Link successfully shortened!', 'success');
        } catch (error) {
            console.error(error);
            this.showError(error.message || 'Error when shortening a link');
            this.showToast('❌ ' + (error.message || 'Error when shortening a link'), 'error');
        } finally {
            this.setLoading(false);
        }
    }

    /**
     * Display result
     */
    displayResult(response) {
        // Handle nested data structure from backend
        const data = response.data || response;
        const shortUrl = `${window.location.origin}/${data.short_code}`;
        
        this.originalUrlDisplay.textContent = data.long_url || data.original_url;
        this.shortUrlDisplay.value = shortUrl;
        this.shortCodeDisplay.textContent = data.short_code;

        this.resultContainer.classList.remove('hidden');
    }

    /**
     * Copy to clipboard
     */
    async copyToClipboard() {
        const shortUrl = this.shortUrlDisplay.value;

        try {
            await navigator.clipboard.writeText(shortUrl);
            this.showToast('📋 Link copied!', 'success');

            // Визуальная обратная связь
            const originalText = this.copyBtn.textContent;
            this.copyBtn.textContent = '✅ Copied!';
            this.copyBtn.style.backgroundColor = 'var(--success-color)';

            setTimeout(() => {
                this.copyBtn.textContent = originalText;
                this.copyBtn.style.backgroundColor = '';
            }, 2000);
        } catch (error) {
            this.showToast('❌ Error while copying', 'error');
        }
    }

    /**
     * URL validation
     */
    validateURL(url) {
        try {
            new URL(url);
            return true;
        } catch (e) {
            return false;
        }
    }

    /**
     * Show error
     */
    showError(message) {
        this.urlError.textContent = message;
        this.urlError.classList.add('show');
    }

    /**
     * Clear error
     */
    clearError() {
        this.urlError.textContent = '';
        this.urlError.classList.remove('show');
    }

    /**
     * Set the download status
     */
    setLoading(isLoading) {
        this.submitBtn.disabled = isLoading;
        if (isLoading) {
            this.btnText.style.display = 'none';
            this.btnLoader.classList.remove('hidden');
        } else {
            this.btnText.style.display = 'inline';
            this.btnLoader.classList.add('hidden');
        }
    }

    /**
     * Reset form
     */
    resetForm() {
        this.form.reset();
        this.resultContainer.classList.add('hidden');
        this.clearError();
        this.urlInput.focus();
    }

    /**
     * Save to local history
     */
    saveToHistory(response) {
        // Handle nested data structure from backend
        const data = response.data || response;
        let history = this.getHistory();
        history.unshift({
            short_code: data.short_code,
            long_url: data.long_url || data.original_url,
            original_url: data.long_url || data.original_url,
            createdAt: new Date().toISOString()
        });
        // Limit history to the last 10 links
        history = history.slice(0, 10);
        localStorage.setItem('shortifyHistory', JSON.stringify(history));
    }

    /**
     * Get history from local storage
     */
    getHistory() {
        const history = localStorage.getItem('shortifyHistory');
        return history ? JSON.parse(history) : [];
    }

    /**
     * Download history
     */
    loadHistory() {
        const history = this.getHistory();

        if (history.length === 0) {
            this.historyContainer.innerHTML = `
                <div class="empty-state">
                    <p>📭 History is empty so far</p>
                </div>
            `;
            return;
        }

        this.historyContainer.innerHTML = history.map(item => `
            <div class="history-item">
                <div class="original" title="${item.original_url}">
                    ${this.truncateText(item.original_url, 50)}
                </div>
                <div class="short">${item.short_code}</div>
                <div class="date">${this.formatDate(item.createdAt)}</div>
                <button type="button" class="btn btn-secondary btn-small" onclick="app.copyHistoryItem('${this.escapeHtml(item.short_code)}')">
                    📋 Copy
                </button>
            </div>
        `).join('');
    }

    /**
     * Copy an item from history
     */
    copyHistoryItem(shortCode) {
        const shortUrl = `${window.location.origin}/${shortCode}`;
        navigator.clipboard.writeText(shortUrl);
        this.showToast('📋 Link copied!', 'success');
    }

    /**
     * Show toast notification
     */
    showToast(message, type = 'success') {
        this.toast.textContent = message;
        this.toast.className = `toast show ${type}`;

        setTimeout(() => {
            this.toast.classList.remove('show');
        }, 3000);
    }

    /**
     * Date formatting
     */
    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);

        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins} min ago`;
        if (diffHours < 24) return `${diffHours} hours ago`;
        if (diffDays < 7) return `${diffDays} days ago`;

        return date.toLocaleDateString('en-US', {
            day: '2-digit',
            month: '2-digit',
            year: '2-digit'
        });
    }

    /**
     * Trim text
     */
    truncateText(text, length) {
        return text.length > length ? text.substring(0, length) + '...' : text;
    }

    /**
     * HTML shielding
     */
    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }
}

// Initialize the application
const app = new ShortifyApp();
