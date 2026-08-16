/**
 * FaceSecure - Camera Utilities
 * Helper functions for camera operations
 */

class CameraUtils {
    constructor() {
        this.stream = null;
        this.videoElement = null;
        this.canvasElement = null;
    }

    /**
     * Initialize camera
     * @param {string} videoId - Video element ID
     * @param {string} canvasId - Canvas element ID
     */
    async initCamera(videoId = 'videoElement', canvasId = 'canvasElement') {
        this.videoElement = document.getElementById(videoId);
        this.canvasElement = document.getElementById(canvasId);
        
        if (!this.videoElement) {
            throw new Error('Video element not found');
        }
    }

    /**
     * Start camera stream
     * @param {Object} constraints - MediaStream constraints
     */
    async startCamera(constraints = { video: true }) {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia(constraints);
            this.videoElement.srcObject = this.stream;
            return true;
        } catch (error) {
            console.error('Camera access error:', error);
            throw error;
        }
    }

    /**
     * Stop camera stream
     */
    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
            this.videoElement.srcObject = null;
        }
    }

    /**
     * Capture frame from camera
     * @returns {string} Base64 encoded image
     */
    captureFrame() {
        if (!this.videoElement || !this.canvasElement) {
            throw new Error('Camera not initialized');
        }

        const canvas = this.canvasElement;
        const video = this.videoElement;
        
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);
        
        return canvas.toDataURL('image/jpeg');
    }

    /**
     * Capture multiple frames
     * @param {number} count - Number of frames to capture
     * @param {number} interval - Interval between captures in ms
     * @returns {Array<string>} Array of base64 encoded images
     */
    async captureFrames(count = 5, interval = 500) {
        const frames = [];
        
        for (let i = 0; i < count; i++) {
            frames.push(this.captureFrame());
            if (i < count - 1) {
                await new Promise(resolve => setTimeout(resolve, interval));
            }
        }
        
        return frames;
    }

    /**
     * Get camera capabilities
     * @returns {Object} Camera capabilities
     */
    async getCameraCapabilities() {
        if (!this.stream) {
            throw new Error('Camera not started');
        }

        const track = this.stream.getVideoTracks()[0];
        const capabilities = track.getCapabilities();
        
        return {
            width: capabilities.width?.max,
            height: capabilities.height?.max,
            frameRate: capabilities.frameRate?.max,
            facingMode: capabilities.facingMode
        };
    }

    /**
     * Check if camera is available
     * @returns {boolean} Camera availability
     */
    static async isCameraAvailable() {
        try {
            const devices = await navigator.mediaDevices.enumerateDevices();
            return devices.some(device => device.kind === 'videoinput');
        } catch (error) {
            console.error('Error checking camera availability:', error);
            return false;
        }
    }

    /**
     * Get available cameras
     * @returns {Array<Object>} List of available cameras
     */
    static async getAvailableCameras() {
        try {
            const devices = await navigator.mediaDevices.enumerateDevices();
            return devices
                .filter(device => device.kind === 'videoinput')
                .map(device => ({
                    id: device.deviceId,
                    label: device.label || `Camera ${device.deviceId.slice(0, 5)}`
                }));
        } catch (error) {
            console.error('Error getting cameras:', error);
            return [];
        }
    }

    /**
     * Request camera permission
     * @returns {boolean} Permission granted
     */
    static async requestCameraPermission() {
        try {
            await navigator.mediaDevices.getUserMedia({ video: true });
            return true;
        } catch (error) {
            console.error('Camera permission denied:', error);
            return false;
        }
    }

    /**
     * Cleanup
     */
    cleanup() {
        this.stopCamera();
        this.videoElement = null;
        this.canvasElement = null;
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CameraUtils;
}
