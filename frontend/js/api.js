/**
 * API Service for interacting with Shortify backend
 */

class ShortifyAPI {
    constructor() {
        // Please provide the address of your backend server.
        this.baseURL = 'http://localhost:8000/api/v1';
        this.timeout = 10000; // 10 секунд
    }

    /**
     * Shorten URL
     * @param {string} originalUrl - Original URL
     * @returns {Promise<Object>} Shorten result
     */
    async shortenURL(originalUrl) {
        try {
            const response = await this.fetchWithTimeout(`${this.baseURL}/short_url`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    long_url: originalUrl
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error when shortening URL');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Get information about a shortened link
     * @param {string} shortCode - Shortened link code
     * @returns {Promise<Object>} Link information
     */
    async getURLInfo(shortCode) {
        try {
            const response = await this.fetchWithTimeout(`${this.baseURL}/urls/${shortCode}`);

            if (!response.ok) {
                throw new Error('Link not found');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Get all links
     * @returns {Promise<Array>} Array of all links
     */
    async getAllURLs() {
        try {
            const response = await this.fetchWithTimeout(`${this.baseURL}/urls`);

            if (!response.ok) {
                throw new Error('Error retrieving list of links');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Remove link
     * @param {string} shortCode - Short link code
     * @returns {Promise<void>}
     */
    async deleteURL(shortCode) {
        try {
            const response = await this.fetchWithTimeout(`${this.baseURL}/urls/${shortCode}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Error deleting link');
            }
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Update link
     * @param {string} shortCode - Short link code
     * @param {Object} data - Data to update
     * @returns {Promise<Object>} Updated link
     */
    async updateURL(shortCode, data) {
        try {
            const response = await this.fetchWithTimeout(`${this.baseURL}/urls/${shortCode}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error updating link');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Fetch with a timeout
     * @private
     */
    fetchWithTimeout(url, options = {}) {
        return Promise.race([
            fetch(url, options),
            new Promise((_, reject) =>
                setTimeout(() => reject(new Error('Request timeout')), this.timeout)
            )
        ]);
    }
}

// Creating a global instance of the API
const api = new ShortifyAPI();
