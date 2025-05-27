<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>Plant Disease Diagnostics</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-4Q6Gf2aSP4eDXB8Miphtr37CMZZQ5oXLH2yaXMJ2w8e2ZtHTl7GptT4jmndRuHDT" crossorigin="anonymous">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ asset('build/assets/css/style.css') }}">

</head>

<body>
    <div class="floating-elements"></div>

    <div class="container py-5">
        <div class="hero-section">
            <h1 class="hero-title">Plant Disease Diagnostics</h1>
            <p class="hero-subtitle">AI-powered plant health analysis at your fingertips</p>
        </div>

        <div class="row g-4">
            <!-- Left Column: Upload & Analysis -->
            <div class="col-lg-6">
                <div class="glass-card upload-section">
                    <div id="image-preview"></div>

                    <div class="upload-zone" id="uploadZone">
                        <i class="fas fa-cloud-upload-alt upload-icon"></i>
                        <div class="upload-text">Drop your plant image here</div>
                        <div class="upload-subtext">or click to browse</div>
                        <input type="file" id="fileInput" name="image" accept="image/*" style="display: none;" required>
                    </div>

                    <form id="uploadForm" enctype="multipart/form-data">
                        @csrf
                        <button type="submit" class="modern-btn w-100" id="analyzeBtn">
                            <i class="fas fa-microscope me-2"></i>
                            Analyze Plant Health
                        </button>
                    </form>

                    <div id="result"></div>
                </div>
            </div>

            <!-- Right Column: Features & Info -->
            <div class="col-lg-6">
                <div class="glass-card info-section">
                    <h3 class="mb-4" style="color: var(--text-primary); font-weight: 600;">
                        <i class="fas fa-leaf me-2" style="color: #4facfe;"></i>
                        Advanced Plant Analysis
                    </h3>

                    <div class="feature-grid">
                        <div class="feature-item">
                            <i class="fas fa-brain feature-icon"></i>
                            <div class="feature-content">
                                <h4>AI-Powered Detection</h4>
                                <p>Advanced machine learning algorithms trained on thousands of plant disease images</p>
                            </div>
                        </div>

                        <div class="feature-item">
                            <i class="fas fa-clock feature-icon"></i>
                            <div class="feature-content">
                                <h4>Instant Results</h4>
                                <p>Get accurate plant health diagnostics in seconds, not hours</p>
                            </div>
                        </div>

                        <div class="feature-item">
                            <i class="fas fa-shield-alt feature-icon"></i>
                            <div class="feature-content">
                                <h4>High Accuracy</h4>
                                <p>State-of-the-art models with over 95% accuracy rate in disease detection</p>
                            </div>
                        </div>

                        <div class="feature-item">
                            <i class="fas fa-mobile-alt feature-icon"></i>
                            <div class="feature-content">
                                <h4>Mobile Friendly</h4>
                                <p>Works perfectly on all devices - desktop, tablet, and smartphone</p>
                            </div>
                        </div>
                    </div>

                    <div class="mt-4 p-3"
                        style="background: rgba(79, 172, 254, 0.1); border-radius: 10px; border-left: 4px solid #4facfe;">
                        <h5 style="color: #4facfe; margin-bottom: 0.5rem;">
                            <i class="fas fa-info-circle me-2"></i>How it works
                        </h5>
                        <p style="color: var(--text-secondary); margin: 0; font-size: 0.9rem;">
                            Simply upload a clear photo of your plant's affected area. Our AI will analyze the image and
                            provide detailed insights about potential diseases, health status, and recommendations.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer">
            <div class="footer-content">
                <p>&copy; 2025 Youssef Gamal Mohamed Mahmoud</p>
                <div class="footer-links">
                    <a href="https://github.com/Youssef-Mekkkawy" target="_blank">
                        <i class="fab fa-github me-1"></i>GitHub
                    </a>
                </div>
            </div>
        </div>
    </div>
    <!-- before closing </body> -->
    <script>
        // Emit the URL so upload.js can pick it up
        window.uploadUrl = @json(route('image.store'));
    </script>
    <script src="{{ asset('build/assets/js/javascript.js') }}"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-j1CDi7MgGQ12Z7Qab0qlWQ2ab0qlWQ/Qqz24Gc6BM0thvEMVjHnfYGF0rmFCozFSxQBxwHKO"
        crossorigin="anonymous"></script>
</body>

</html>