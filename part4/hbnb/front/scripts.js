const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

document.addEventListener('DOMContentLoaded', () => {
    const page = document.body.dataset.page;

    setupNavigation();

    if (page === 'login') {
        initLoginPage();
    }

    if (page === 'index') {
        initIndexPage();
    }

    if (page === 'place') {
        initPlacePage();
    }

    if (page === 'add-review') {
        initAddReviewPage();
    }
});

function setupNavigation() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-button');

    if (loginLink) {
        loginLink.classList.toggle('hidden', Boolean(token));
    }

    if (logoutButton) {
        logoutButton.classList.toggle('hidden', !token);
        logoutButton.addEventListener('click', () => {
            deleteCookie('token');
            window.location.href = 'index.html';
        });
    }
}

function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split('; ') : [];

    for (const cookie of cookies) {
        const [key, ...valueParts] = cookie.split('=');
        if (key === name) {
            return decodeURIComponent(valueParts.join('='));
        }
    }

    return null;
}

function setCookie(name, value, days = 1) {
    const expires = new Date(Date.now() + days * 24 * 60 * 60 * 1000).toUTCString();
    document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
}

function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/`;
}

function getAuthHeaders() {
    const token = getCookie('token');
    const headers = {
        'Content-Type': 'application/json'
    };

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    return headers;
}

function showElementMessage(element, message, isError = false) {
    if (!element) {
        return;
    }

    element.textContent = message;
    element.classList.remove('hidden');
    element.classList.toggle('error-message', isError);
    element.classList.toggle('success-message', !isError);
}

function hideElementMessage(element) {
    if (!element) {
        return;
    }

    element.textContent = '';
    element.classList.add('hidden');
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

async function apiFetch(endpoint, options = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

    let data = null;
    try {
        data = await response.json();
    } catch (error) {
        data = null;
    }

    if (!response.ok) {
        const message = data && (data.error || data.message)
            ? (data.error || data.message)
            : 'Request failed';
        throw new Error(message);
    }

    return data;
}

function escapeHtml(value) {
    return String(value)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
}

function formatPrice(price) {
    const numericPrice = Number(price);
    return Number.isFinite(numericPrice) ? numericPrice.toFixed(2) : '0.00';
}

function renderStars(rating) {
    const value = Number(rating);

    if (!Number.isFinite(value) || value < 1) {
        return '☆☆☆☆☆';
    }

    const rounded = Math.max(1, Math.min(5, Math.round(value)));
    return '★'.repeat(rounded) + '☆'.repeat(5 - rounded);
}

function getReviewAuthorName(review) {
    if (review.user && typeof review.user === 'object') {
        const firstName = review.user.first_name || '';
        const lastName = review.user.last_name || '';
        const fullName = `${firstName} ${lastName}`.trim();

        if (fullName) {
            return fullName;
        }

        if (review.user.name) {
            return String(review.user.name).trim();
        }
    }

    if (review.first_name || review.last_name) {
        const fullName = `${review.first_name || ''} ${review.last_name || ''}`.trim();
        if (fullName) {
            return fullName;
        }
    }

    if (review.user_name) {
        return String(review.user_name).trim();
    }

    if (review.username) {
        return String(review.username).trim();
    }

    if (review.author_name) {
        return String(review.author_name).trim();
    }

    return null;
}

/* ---------------- LOGIN PAGE ---------------- */

function initLoginPage() {
    const form = document.getElementById('login-form');
    const errorBox = document.getElementById('login-error');

    if (!form) {
        return;
    }

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        hideElementMessage(errorBox);

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;

        try {
            const data = await apiFetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            if (!data || !data.access_token) {
                throw new Error('No token returned by API');
            }

            setCookie('token', data.access_token, 1);
            window.location.href = 'index.html';
        } catch (error) {
            showElementMessage(errorBox, error.message || 'Login failed', true);
        }
    });
}

/* ---------------- INDEX PAGE ---------------- */

async function initIndexPage() {
    const placesList = document.getElementById('places-list');
    const filter = document.getElementById('price-filter');
    const token = getCookie('token');
    const messageBox = document.getElementById('message-box');

    if (!placesList) {
        return;
    }

    await loadPlaces();

    if (filter) {
        filter.addEventListener('change', applyPriceFilter);
    }

    if (!token && messageBox) {
        messageBox.textContent = 'You can browse places without logging in, but login is required to add reviews.';
        messageBox.classList.remove('hidden');
    }
}

async function loadPlaces() {
    const placesList = document.getElementById('places-list');

    if (!placesList) {
        return;
    }

    placesList.innerHTML = '<p>Loading places...</p>';

    try {
        const responseData = await apiFetch('/places/', {
            method: 'GET',
            headers: getAuthHeaders()
        });

        const places = normalizePlacesResponse(responseData);
        displayPlaces(places);
        applyPriceFilter();
    } catch (error) {
        placesList.innerHTML = `<p class="error-message">Failed to load places: ${escapeHtml(error.message)}</p>`;
    }
}

function normalizePlacesResponse(data) {
    if (Array.isArray(data)) {
        return data;
    }

    if (data && Array.isArray(data.places)) {
        return data.places;
    }

    if (data && Array.isArray(data.results)) {
        return data.results;
    }

    if (data && Array.isArray(data.data)) {
        return data.data;
    }

    return [];
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');

    if (!placesList) {
        return;
    }

    placesList.innerHTML = '';

    if (!Array.isArray(places) || places.length === 0) {
        placesList.innerHTML = '<p>No places found.</p>';
        return;
    }

    places.forEach((place) => {
        const title = place.title || place.name || 'Untitled place';
        const rawPrice = place.price_by_night ?? place.price ?? 0;
        const price = Number(rawPrice);

        const card = document.createElement('article');
        card.className = 'place-card';
        card.dataset.price = Number.isFinite(price) ? String(price) : '0';

        card.innerHTML = `
            <h2>${escapeHtml(title)}</h2>
            <p><strong>Price per night:</strong> $${formatPrice(price)}</p>
            <a class="details-button" href="place.html?id=${encodeURIComponent(place.id)}">View Details</a>
        `;

        placesList.appendChild(card);
    });
}

function applyPriceFilter() {
    const filter = document.getElementById('price-filter');
    const cards = document.querySelectorAll('.place-card');

    if (!filter) {
        return;
    }

    const selectedValue = filter.value;

    cards.forEach((card) => {
        const price = Number(card.dataset.price);

        if (selectedValue === 'all') {
            card.style.display = 'block';
            return;
        }

        card.style.display = price <= Number(selectedValue) ? 'block' : 'none';
    });
}

/* ---------------- PLACE PAGE ---------------- */

async function initPlacePage() {
    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');
    const addReviewLink = document.getElementById('add-review-link');
    const detailsSection = document.getElementById('place-details');

    if (!placeId) {
        if (detailsSection) {
            detailsSection.innerHTML = '<p class="error-message">Missing place ID.</p>';
        }
        return;
    }

    if (token && addReviewSection) {
        addReviewSection.classList.remove('hidden');
    }

    if (addReviewLink) {
        addReviewLink.href = `add_review.html?id=${encodeURIComponent(placeId)}`;
    }

    try {
        const place = await apiFetch(`/places/${placeId}`, {
            method: 'GET',
            headers: getAuthHeaders()
        });

        console.log('Place details:', place);
        console.log('Reviews received:', place.reviews);

        displayPlaceDetails(place);
        displayReviews(place.reviews || []);
    } catch (error) {
        if (detailsSection) {
            detailsSection.innerHTML = `<p class="error-message">Failed to load place: ${escapeHtml(error.message)}</p>`;
        }
    }
}

function displayPlaceDetails(place) {
    const section = document.getElementById('place-details');

    if (!section) {
        return;
    }

    const title = place.title || place.name || 'Untitled place';
    const rawPrice = place.price_by_night ?? place.price ?? 0;
    const price = Number(rawPrice);

    let ownerName = 'Unknown';
    if (place.owner && typeof place.owner === 'object') {
        ownerName = `${place.owner.first_name || ''} ${place.owner.last_name || ''}`.trim() || place.owner.name || 'Unknown';
    } else if (place.host) {
        ownerName = place.host;
    }

    const amenities = Array.isArray(place.amenities) ? place.amenities : [];

    section.innerHTML = `
        <h1 class="page-title">${escapeHtml(title)}</h1>

        <div class="place-info">
            <p><strong>Host:</strong> ${escapeHtml(ownerName)}</p>
            <p><strong>Price per night:</strong> $${Number.isFinite(price) ? price.toFixed(2) : '0.00'}</p>
            <p><strong>Description:</strong> ${escapeHtml(place.description || 'No description')}</p>
        </div>

        <div class="place-info">
            <h3>Amenities</h3>
            ${
                amenities.length
                    ? `<ul>${amenities.map((amenity) => `<li>${escapeHtml(amenity.name || amenity.title || 'Amenity')}</li>`).join('')}</ul>`
                    : '<p>No amenities listed.</p>'
            }
        </div>
    `;
}

function displayReviews(reviews) {
    const reviewsList = document.getElementById('reviews-list');

    if (!reviewsList) {
        return;
    }

    reviewsList.innerHTML = '';

    if (!Array.isArray(reviews) || reviews.length === 0) {
        reviewsList.innerHTML = '<p>No reviews yet.</p>';
        return;
    }

    reviews.forEach((review) => {
        const card = document.createElement('article');
        card.className = 'review-card';

        const userName = getReviewAuthorName(review);
        const comment = review.text || review.comment || 'No comment';
        const stars = renderStars(review.rating);

        card.innerHTML = `
            <p class="review-author"><strong>${escapeHtml(userName || 'Anonymous')}</strong></p>
            <p class="review-comment">${escapeHtml(comment)}</p>
            <p class="review-rating">${escapeHtml(stars)}</p>
        `;

        reviewsList.appendChild(card);
    });
}

/* ---------------- ADD REVIEW PAGE ---------------- */

async function initAddReviewPage() {
    const token = getCookie('token');
    const form = document.getElementById('review-form');
    const placeId = getPlaceIdFromURL();
    const reviewMessage = document.getElementById('review-message');
    const reviewError = document.getElementById('review-error');
    const placeReviewTitle = document.getElementById('place-review-title');

    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    if (!placeId) {
        showElementMessage(reviewError, 'Missing place ID.', true);
        return;
    }

    try {
        const place = await apiFetch(`/places/${placeId}`, {
            method: 'GET',
            headers: getAuthHeaders()
        });

        const title = place.title || place.name || 'Untitled place';

        if (placeReviewTitle) {
            placeReviewTitle.innerHTML = `<h1 class="page-title small-title">Reviewing: ${escapeHtml(title)}</h1>`;
        }
    } catch (error) {
        showElementMessage(reviewError, `Unable to load place: ${error.message}`, true);
    }

    if (!form) {
        return;
    }

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        hideElementMessage(reviewMessage);
        hideElementMessage(reviewError);

        const reviewText = document.getElementById('review').value.trim();
        const rating = Number(document.getElementById('rating').value);

        if (!reviewText) {
            showElementMessage(reviewError, 'Review text is required.', true);
            return;
        }

        if (!rating || rating < 1 || rating > 5) {
            showElementMessage(reviewError, 'Please choose a valid rating.', true);
            return;
        }

        try {
            await apiFetch('/reviews/', {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify({
                    text: reviewText,
                    rating: rating,
                    place_id: placeId
                })
            });

            form.reset();
            showElementMessage(reviewMessage, 'Review submitted successfully!');
            setTimeout(() => {
                window.location.href = `place.html?id=${encodeURIComponent(placeId)}`;
            }, 1000);
        } catch (error) {
            showElementMessage(reviewError, error.message || 'Failed to submit review', true);
        }
    });
}
