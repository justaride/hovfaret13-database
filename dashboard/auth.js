// Hovfaret 13 Dashboard Authentication
// Version 2.76

(function() {
    const AUTH_KEY = 'h13_auth';
    const AUTH_PASSWORD = 'h13-skøyen-2025';
    const SESSION_HOURS = 24;

    function isAuthenticated() {
        const session = localStorage.getItem(AUTH_KEY);
        if (!session) return false;

        try {
            const data = JSON.parse(session);
            const expires = new Date(data.expires);
            if (expires > new Date() && data.authenticated) {
                return true;
            }
        } catch (e) {
            return false;
        }
        return false;
    }

    function authenticate(password) {
        if (password === AUTH_PASSWORD) {
            const expires = new Date();
            expires.setHours(expires.getHours() + SESSION_HOURS);
            localStorage.setItem(AUTH_KEY, JSON.stringify({
                authenticated: true,
                expires: expires.toISOString()
            }));
            return true;
        }
        return false;
    }

    function showLoginDialog() {
        // Create overlay
        const overlay = document.createElement('div');
        overlay.id = 'auth-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 99999;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        `;

        overlay.innerHTML = `
            <div style="
                background: white;
                padding: 3rem;
                border-radius: 1rem;
                box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
                max-width: 400px;
                width: 90%;
                text-align: center;
            ">
                <div style="
                    width: 60px;
                    height: 60px;
                    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
                    border-radius: 12px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto 1.5rem;
                ">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                        <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                    </svg>
                </div>
                <h2 style="margin: 0 0 0.5rem; color: #0f172a; font-size: 1.5rem; font-weight: 600;">
                    Hovfaret 13
                </h2>
                <p style="margin: 0 0 1.5rem; color: #64748b; font-size: 0.875rem;">
                    Prosjektdatabase — Begrenset tilgang
                </p>
                <form id="auth-form">
                    <input
                        type="password"
                        id="auth-password"
                        placeholder="Skriv inn passord"
                        autocomplete="current-password"
                        style="
                            width: 100%;
                            padding: 0.875rem 1rem;
                            border: 2px solid #e2e8f0;
                            border-radius: 0.5rem;
                            font-size: 1rem;
                            margin-bottom: 1rem;
                            box-sizing: border-box;
                            transition: border-color 0.2s;
                        "
                    />
                    <button
                        type="submit"
                        style="
                            width: 100%;
                            padding: 0.875rem;
                            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
                            color: white;
                            border: none;
                            border-radius: 0.5rem;
                            font-size: 1rem;
                            font-weight: 500;
                            cursor: pointer;
                            transition: transform 0.2s, box-shadow 0.2s;
                        "
                    >
                        Logg inn
                    </button>
                    <p id="auth-error" style="
                        color: #ef4444;
                        margin: 1rem 0 0;
                        font-size: 0.875rem;
                        display: none;
                    ">
                        Feil passord. Prøv igjen.
                    </p>
                </form>
                <p style="margin: 1.5rem 0 0; color: #94a3b8; font-size: 0.75rem;">
                    Kontakt prosjektleder for tilgang
                </p>
            </div>
        `;

        document.body.appendChild(overlay);
        document.body.style.overflow = 'hidden';

        const form = document.getElementById('auth-form');
        const input = document.getElementById('auth-password');
        const error = document.getElementById('auth-error');

        input.focus();

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            if (authenticate(input.value)) {
                overlay.remove();
                document.body.style.overflow = '';
            } else {
                error.style.display = 'block';
                input.style.borderColor = '#ef4444';
                input.value = '';
                input.focus();
            }
        });

        input.addEventListener('input', function() {
            error.style.display = 'none';
            input.style.borderColor = '#e2e8f0';
        });
    }

    // Check auth on page load
    if (!isAuthenticated()) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', showLoginDialog);
        } else {
            showLoginDialog();
        }
    }

    // Export for manual use
    window.h13Auth = {
        isAuthenticated,
        authenticate,
        logout: function() {
            localStorage.removeItem(AUTH_KEY);
            location.reload();
        }
    };
})();
