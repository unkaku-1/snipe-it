/*!
 * Snipe-IT Liquid Glass Effects
 * JavaScript enhancements for the Liquid Glass Theme
 * Version: 1.0.0
 */

(function() {
    'use strict';

    // Wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', function() {
        initLiquidGlassEffects();
    });

    /**
     * Initialize all liquid glass effects
     */
    function initLiquidGlassEffects() {
        console.log('🌊 Initializing Liquid Glass Effects...');
        
        // Initialize effects
        initMouseTrackingEffects();
        initScrollAnimations();
        initHoverEnhancements();
        initLoadingAnimations();
        initParallaxEffects();
        
        console.log('✨ Liquid Glass Effects initialized successfully!');
    }

    /**
     * Mouse tracking effects for glass elements
     */
    function initMouseTrackingEffects() {
        const glassElements = document.querySelectorAll('.box, .panel, .card, .btn');
        
        glassElements.forEach(element => {
            element.addEventListener('mousemove', function(e) {
                const rect = element.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;
                
                element.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
            });
            
            element.addEventListener('mouseleave', function() {
                element.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)';
            });
        });
    }

    /**
     * Scroll-based animations
     */
    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    
                    // Add staggered animation for child elements
                    const children = entry.target.querySelectorAll('.box, .panel, .card, .btn');
                    children.forEach((child, index) => {
                        setTimeout(() => {
                            child.classList.add('animate-in');
                        }, index * 100);
                    });
                }
            });
        }, observerOptions);

        // Observe all main content sections
        const sections = document.querySelectorAll('.content-wrapper .content > *');
        sections.forEach(section => {
            observer.observe(section);
        });

        // Add CSS for animations
        addScrollAnimationStyles();
    }

    /**
     * Enhanced hover effects
     */
    function initHoverEnhancements() {
        // Enhanced button hover effects
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(button => {
            button.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px) scale(1.02)';
                this.style.boxShadow = '0 12px 24px rgba(0, 0, 0, 0.15)';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
                this.style.boxShadow = '';
            });
        });

        // Enhanced card hover effects
        const cards = document.querySelectorAll('.box, .panel, .card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-8px)';
                this.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.15)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = '';
            });
        });
    }

    /**
     * Loading animations for dynamic content
     */
    function initLoadingAnimations() {
        // Add shimmer effect to loading elements
        const loadingElements = document.querySelectorAll('.loading, [data-loading="true"]');
        loadingElements.forEach(element => {
            element.classList.add('liquid-glass-loading');
        });

        // Animate new content when it's added
        const contentObserver = new MutationObserver(function(mutations) {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1) { // Element node
                        const newElements = node.querySelectorAll('.box, .panel, .card');
                        newElements.forEach((element, index) => {
                            element.style.opacity = '0';
                            element.style.transform = 'translateY(20px)';
                            
                            setTimeout(() => {
                                element.style.transition = 'all 0.6s cubic-bezier(0.175, 0.885, 0.32, 2.2)';
                                element.style.opacity = '1';
                                element.style.transform = 'translateY(0)';
                            }, index * 100);
                        });
                    }
                });
            });
        });

        contentObserver.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    /**
     * Parallax effects for background elements
     */
    function initParallaxEffects() {
        let ticking = false;

        function updateParallax() {
            const scrolled = window.pageYOffset;
            const parallaxElements = document.querySelectorAll('.main-header, .main-sidebar');
            
            parallaxElements.forEach(element => {
                const speed = element.dataset.speed || 0.5;
                const yPos = -(scrolled * speed);
                element.style.transform = `translateY(${yPos}px)`;
            });
            
            ticking = false;
        }

        function requestTick() {
            if (!ticking) {
                requestAnimationFrame(updateParallax);
                ticking = true;
            }
        }

        window.addEventListener('scroll', requestTick);
    }

    /**
     * Add CSS styles for scroll animations
     */
    function addScrollAnimationStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .animate-in {
                animation: slideInUp 0.6s cubic-bezier(0.175, 0.885, 0.32, 2.2) forwards;
            }

            @keyframes slideInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .liquid-glass-loading {
                position: relative;
                overflow: hidden;
            }

            .liquid-glass-loading::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(
                    90deg,
                    transparent,
                    rgba(255, 255, 255, 0.3),
                    transparent
                );
                animation: shimmer 2s infinite;
            }

            @keyframes shimmer {
                0% {
                    left: -100%;
                }
                100% {
                    left: 100%;
                }
            }

            /* Smooth transitions for all glass elements */
            .box, .panel, .card, .btn, .form-control {
                transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 2.2) !important;
            }

            /* Enhanced focus states */
            .form-control:focus {
                transform: scale(1.02) !important;
            }

            .btn:focus {
                outline: none !important;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3) !important;
            }

            /* Ripple effect for buttons */
            .btn {
                position: relative;
                overflow: hidden;
            }

            .btn::before {
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                width: 0;
                height: 0;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.3);
                transform: translate(-50%, -50%);
                transition: width 0.6s, height 0.6s;
            }

            .btn:active::before {
                width: 300px;
                height: 300px;
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Utility function to add glass effect to new elements
     */
    window.addGlassEffect = function(element) {
        if (!element) return;
        
        element.classList.add('glass-medium');
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            element.style.transition = 'all 0.6s cubic-bezier(0.175, 0.885, 0.32, 2.2)';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 100);
    };

    /**
     * Theme toggle functionality (if needed)
     */
    window.toggleGlassTheme = function() {
        const body = document.body;
        body.classList.toggle('glass-theme-dark');
        
        // Save preference
        localStorage.setItem('glassTheme', body.classList.contains('glass-theme-dark') ? 'dark' : 'light');
    };

    // Load saved theme preference
    const savedTheme = localStorage.getItem('glassTheme');
    if (savedTheme === 'dark') {
        document.body.classList.add('glass-theme-dark');
    }

    /**
     * Performance optimization: Reduce animations on low-end devices
     */
    function optimizeForPerformance() {
        // Detect if device prefers reduced motion
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            const style = document.createElement('style');
            style.textContent = `
                *, *::before, *::after {
                    animation-duration: 0.01ms !important;
                    animation-iteration-count: 1 !important;
                    transition-duration: 0.01ms !important;
                }
            `;
            document.head.appendChild(style);
        }

        // Reduce effects on mobile devices
        if (window.innerWidth < 768) {
            const mobileStyle = document.createElement('style');
            mobileStyle.textContent = `
                .box:hover, .panel:hover, .card:hover {
                    transform: none !important;
                }
                
                .btn:hover {
                    transform: none !important;
                }
            `;
            document.head.appendChild(mobileStyle);
        }
    }

    // Initialize performance optimizations
    optimizeForPerformance();

})();

