document.addEventListener('DOMContentLoaded', function() {
    const navItems = document.querySelectorAll('.nav-item');
    const contentSections = document.querySelectorAll('.content-section');

    // Helpers to manage active section and URL/localStorage state
    const STORAGE_KEY = 'dashboard:lastSection';

    function getSectionFromUrl() {
        const params = new URLSearchParams(window.location.search);
        return params.get('section');
    }

    function setSectionInUrl(sectionId) {
        const url = new URL(window.location.href);
        if (sectionId) {
            url.searchParams.set('section', sectionId);
        } else {
            url.searchParams.delete('section');
        }
        window.history.replaceState({}, '', url);
    }

    function activateSectionById(sectionId) {
        if (!sectionId) return;
        // Toggle nav active
        navItems.forEach(nav => nav.classList.remove('active'));
        const matchingNav = document.querySelector(`.nav-item[data-section="${sectionId}"]`);
        if (matchingNav) matchingNav.classList.add('active');

        // Toggle section visibility
        contentSections.forEach(section => section.classList.remove('active'));
        const targetElement = document.getElementById(sectionId);
        if (targetElement) {
            targetElement.classList.add('active');
        }
    }

    function getCurrentActiveSectionId() {
        const active = document.querySelector('.content-section.active');
        return active ? active.id : null;
    }
    
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            if (this.hasAttribute('data-section')) {
                e.preventDefault();

                const targetSection = this.getAttribute('data-section');

                // Update UI
                navItems.forEach(nav => nav.classList.remove('active'));
                this.classList.add('active');
                contentSections.forEach(section => section.classList.remove('active'));
                const targetElement = document.getElementById(targetSection);
                if (targetElement) targetElement.classList.add('active');

                // Persist state
                localStorage.setItem(STORAGE_KEY, targetSection);
                setSectionInUrl(targetSection);
            }
        });
    });

    // On load, restore last viewed section from URL ?section=... or localStorage
    (function restoreSectionOnLoad() {
        const urlSection = getSectionFromUrl();
        const storedSection = localStorage.getItem(STORAGE_KEY);
        const initialSection = urlSection || storedSection;
        if (initialSection) {
            activateSectionById(initialSection);
            setSectionInUrl(initialSection);
        } else {
            // Ensure the initially active section is stored
            const current = getCurrentActiveSectionId();
            if (current) {
                localStorage.setItem(STORAGE_KEY, current);
                setSectionInUrl(current);
            }
        }
    })();

    // Preserve section across filter submissions inside dashboard content
    document.addEventListener('submit', function(e) {
        const form = e.target;
        if (!(form instanceof HTMLFormElement)) return;
        const withinSection = form.closest('.content-section');
        if (!withinSection) return;

        const activeSectionId = getCurrentActiveSectionId() || withinSection.id;

        // Ensure hidden input 'section' exists and is up-to-date
        let hidden = form.querySelector('input[name="section"][type="hidden"]');
        if (!hidden) {
            hidden = document.createElement('input');
            hidden.type = 'hidden';
            hidden.name = 'section';
            form.appendChild(hidden);
        }
        hidden.value = activeSectionId;

        // Also reflect in action/query for idempotent GET links
        try {
            const actionUrl = new URL(form.getAttribute('action') || window.location.href, window.location.origin);
            actionUrl.searchParams.set('section', activeSectionId);
            form.setAttribute('action', actionUrl.pathname + '?' + actionUrl.searchParams.toString());
        } catch (_) {
            // no-op if URL parsing fails
        }
    }, true);

    // Preserve section when clicking internal links within content sections (e.g., pagination, filters)
    document.addEventListener('click', function(e) {
        const anchor = e.target instanceof Element ? e.target.closest('a[href]') : null;
        if (!anchor) return;
        const withinSection = anchor.closest('.content-section');
        if (!withinSection) return;

        // Ignore pure hash links handled below
        const href = anchor.getAttribute('href');
        if (!href || href.startsWith('#')) return;

        const activeSectionId = getCurrentActiveSectionId() || withinSection.id;
        try {
            const url = new URL(href, window.location.origin);
            // Same-origin only
            if (url.origin === window.location.origin) {
                url.searchParams.set('section', activeSectionId);
                anchor.setAttribute('href', url.pathname + '?' + url.searchParams.toString());
            }
        } catch (_) {
            // If not a valid URL, skip
        }
    }, true);

    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    setInterval(function() {
        console.log('Auto-refresh triggered');
    }, 300000);
});