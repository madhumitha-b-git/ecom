// app.js - E-Commerce Core Frontend logic

// --- Default Mock Data ---
const DEFAULT_PRODUCTS = [
    {
        product_id: "prod-fashion-001",
        name: "Elegant Summer Floral Dress",
        description: "Lightweight, breathable floral dress perfect for warm summer days. Crafted from 100% organic cotton with custom waist adjusters.",
        price: 79.99,
        category: "Fashion",
        rating: 4.8,
        rating_count: 124,
        image: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500&q=80",
        sizes: ["S", "M", "L", "XL"]
    },
    {
        product_id: "prod-fashion-002",
        name: "Classic Denim Button-Up Dress",
        description: "Sturdy, styled denim dress featuring double chest pockets and a premium copper button alignment. A timeless fashion statement.",
        price: 94.50,
        category: "Fashion",
        rating: 4.6,
        rating_count: 85,
        image: "https://images.unsplash.com/photo-1544441893-675973e31985?w=500&q=80",
        sizes: ["M", "L", "XL", "XXL"]
    },
    {
        product_id: "prod-elec-001",
        name: "Acoustic Pro Noise-Cancelling Headphones",
        description: "Studio-quality over-ear headphones with advanced active noise cancellation (ANC), 40-hour battery life, and spatial audio support.",
        price: 249.99,
        category: "Electronics",
        rating: 4.9,
        rating_count: 412,
        image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&q=80"
    },
    {
        product_id: "prod-elec-002",
        name: "Quantum Mechanical Ergonomic Keyboard",
        description: "Hot-swappable mechanical keyboard with premium silent switches, RGB backlighting, and custom wrist rest for coding comfort.",
        price: 159.00,
        category: "Electronics",
        rating: 4.7,
        rating_count: 98,
        image: "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&q=80"
    },
    {
        product_id: "prod-furn-001",
        name: "Ergonomic Mesh Office Chair",
        description: "Premium office chair with adjustable lumbar support, 3D armrests, and high-density foam padding for healthy posture.",
        price: 189.99,
        category: "Furniture",
        rating: 4.6,
        rating_count: 142,
        image: "https://images.unsplash.com/photo-1505797149-43b0069ec26b?w=600&q=80"
    },
    {
        product_id: "prod-groc-001",
        name: "Ceremonial Uji Matcha Powder",
        description: "100% organic Japanese green tea powder sourced from Uji, Kyoto. Rich in antioxidants and perfect for tea or lattes.",
        price: 24.50,
        category: "Grocery",
        rating: 4.8,
        rating_count: 88,
        image: "https://images.unsplash.com/photo-1582793988951-9aed5509eb97?w=600&q=80"
    },
    {
        product_id: "prod-cosm-001",
        name: "Hydrating Hyaluronic Acid Serum",
        description: "Intense moisture replenishment serum with dual-weight hyaluronic acid and vitamin B5 for smooth, plump skin.",
        price: 28.00,
        category: "Cosmetics",
        rating: 4.7,
        rating_count: 204,
        image: "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=600&q=80"
    },
    {
        product_id: "prod-uten-001",
        name: "Pre-Seasoned Cast Iron Skillet",
        description: "Heavy-duty 10-inch skillet offering superb heat retention and distribution. Perfect for stovetop, oven, or campfire cooking.",
        price: 39.99,
        category: "Utensils",
        rating: 4.9,
        rating_count: 315,
        image: "https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?w=600&q=80"
    },
    {
        product_id: "prod-shoes-001",
        name: "Stratus-Grip Breathable Running Shoes",
        description: "Ultra-comfortable running shoes engineered with carbon-fiber plates and high-traction rubber outsoles for endurance training.",
        price: 120.00,
        category: "Footwear",
        rating: 4.5,
        rating_count: 220,
        image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&q=80"
    },
    {
        product_id: "prod-books-001",
        name: "Clean Architecture: A Craftsman's Guide",
        description: "A comprehensive guide to software structure and design patterns written by industry expert Robert C. Martin. Must-read for developers.",
        price: 29.99,
        category: "Books",
        rating: 4.9,
        rating_count: 480,
        image: "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=600&q=80"
    },
    {
        product_id: "prod-books-002",
        name: "Designing Data-Intensive Applications",
        description: "The definitive guide to understanding system architectures, storage systems, databases, processing models, and scaling rules.",
        price: 44.95,
        category: "Books",
        rating: 4.9,
        rating_count: 910,
        image: "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=600&q=80"
    },
    {
        product_id: "prod-fit-001",
        name: "Smart Adjustable Dumbbells Set",
        description: "Sleek all-in-one dumbbell set adjustable from 5 to 52.5 lbs. Features durable steel plates and safe dial-selection technology.",
        price: 199.99,
        category: "Fitness",
        rating: 4.8,
        rating_count: 320,
        image: "https://images.unsplash.com/photo-1638536532686-d610adfc8e5c?w=600&q=80"
    },
    {
        product_id: "prod-fit-002",
        name: "Premium Extra-Thick Yoga Mat",
        description: "Eco-friendly, non-slip high-density yoga mat with alignment markers. Double-sided texture ensures excellent traction and joint support.",
        price: 34.50,
        category: "Fitness",
        rating: 4.7,
        rating_count: 140,
        image: "https://images.unsplash.com/photo-1592432678016-e910b452f9a2?w=600&q=80"
    },
    {
        product_id: "prod-toys-001",
        name: "STEM Mechanical Mars Rover Robot",
        description: "Solar-powered science robot kit for kids and teens. Build a working mechanical rover with realistic suspension and steering.",
        price: 79.99,
        category: "Toys",
        rating: 4.6,
        rating_count: 65,
        image: "https://images.unsplash.com/photo-1531525645387-7f14be1bdbbd?w=600&q=80"
    },
    {
        product_id: "prod-toys-002",
        name: "Creative Classic Bricks Construction Box",
        description: "Set of 790 classic colorful building bricks. Includes windows, doors, eyes, and baseplates for infinite creative design.",
        price: 49.99,
        category: "Toys",
        rating: 4.8,
        rating_count: 215,
        image: "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=600&q=80"
    }
];

const DEFAULT_INVENTORY = {
    "prod-fashion-001": 25,
    "prod-fashion-002": 4,
    "prod-elec-001": 15,
    "prod-elec-002": 8,
    "prod-furn-001": 12,
    "prod-groc-001": 50,
    "prod-cosm-001": 3,
    "prod-uten-001": 18,
    "prod-shoes-001": 30,
    "prod-books-001": 40,
    "prod-books-002": 25,
    "prod-fit-001": 10,
    "prod-fit-002": 35,
    "prod-toys-001": 15,
    "prod-toys-002": 60
};

// --- App State ---
const state = {
    products: [...DEFAULT_PRODUCTS],
    inventory: {},
    cart: [],
    orders: [],
    payments: [],
    currentUser: {
        username: "Guest",
        role: "user"
    },
    apiMode: "live", // 'mock' or 'live'
    endpoints: {
        order: "http://localhost:8000/v1",
        cart: "http://localhost:8001/v1",
        inventory: "http://localhost:8002/v1",
        payment: "http://localhost:8003/v1",
        product: "http://localhost:8004/v1",
        analytics: "http://localhost:8005/v1",
        auth: "http://localhost:8006/v1"
    },
    selectedCategory: "all",
    selectedProductDetail: null,
    selectedCheckoutSize: null,
    wishlist: []
};

// --- UI Selectors ---
const views = {
    storefront: document.getElementById("storefront-view"),
    userOrders: document.getElementById("user-orders-view"),
    login: document.getElementById("login-view"),
    admin: document.getElementById("admin-view"),
    wishlist: document.getElementById("wishlist-view"),
    cartDrawer: document.getElementById("cart-drawer-element"),
    productModal: document.getElementById("product-detail-modal"),
    checkoutModal: document.getElementById("checkout-modal"),
    settingsModal: document.getElementById("settings-modal"),
    productFormModal: document.getElementById("product-form-modal")
};

// --- Toast Alerts ---
function showToast(message, type = "success") {
    const wrapper = document.getElementById("toast-wrapper");
    const toast = document.createElement("div");
    toast.className = `badge badge-${type}`;
    toast.style.padding = "16px 24px";
    toast.style.fontSize = "14px";
    toast.style.borderRadius = "12px";
    toast.style.boxShadow = "0 10px 20px rgba(0,0,0,0.3)";
    toast.style.display = "flex";
    toast.style.alignItems = "center";
    toast.style.gap = "10px";
    toast.style.background = type === "success" ? "#10b981" : type === "warning" ? "#f59e0b" : "#ef4444";
    toast.style.color = "white";
    toast.style.animation = "fadeIn 0.3s ease-out";

    let icon = "circle-check";
    if (type === "warning") icon = "triangle-exclamation";
    if (type === "danger") icon = "circle-xmark";

    toast.innerHTML = `<i class="fa-solid fa-${icon}"></i> <span>${message}</span>`;
    wrapper.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transition = "opacity 0.4s";
        setTimeout(() => toast.remove(), 400);
    }, 3500);
}

// --- View Router ---
function showView(viewName) {
    // Restrict storefront and personal orders for Admin
    if (state.currentUser.role === "admin" && (viewName === "storefront" || viewName === "userOrders" || viewName === "wishlist")) {
        showToast("Access Denied: Admins cannot access shopping features.", "warning");
        showView("admin");
        return;
    }

    // Hide all views
    Object.values(views).forEach(v => {
        if (v !== views.cartDrawer && v !== views.productModal && v !== views.checkoutModal && v !== views.settingsModal && v !== views.productFormModal) {
            v.classList.add("d-none");
        }
    });

    // Show selected view
    views[viewName].classList.remove("d-none");

    // Remove active styles from header tabs
    document.getElementById("nav-shop-btn").classList.remove("active");
    document.getElementById("nav-user-orders-btn").classList.remove("active");
    document.getElementById("nav-admin-btn").classList.remove("active");
    const wishlistBtn = document.getElementById("nav-wishlist-btn");
    if (wishlistBtn) wishlistBtn.classList.remove("active");

    if (viewName === "storefront") {
        document.getElementById("nav-shop-btn").classList.add("active");
        document.getElementById("categories-nav").classList.remove("d-none");
        document.getElementById("search-bar-wrapper").classList.remove("d-none");
    } else {
        document.getElementById("categories-nav").classList.add("d-none");
        document.getElementById("search-bar-wrapper").classList.add("d-none");
    }

    if (viewName === "userOrders") {
        document.getElementById("nav-user-orders-btn").classList.add("active");
        renderUserOrders();
    }

    if (viewName === "admin") {
        document.getElementById("nav-admin-btn").classList.add("active");
        renderAdminDashboard();
    }

    if (viewName === "wishlist") {
        if (wishlistBtn) wishlistBtn.classList.add("active");
        renderWishlist();
    }
}

// --- Core API Helpers ---
async function apiCall(service, path, method = "GET", body = null) {
    if (state.apiMode === "mock") return null;

    const url = `${state.endpoints[service]}${path}`;
    try {
        const options = {
            method,
            headers: {
                "Content-Type": "application/json"
            }
        };
        if (state.currentUser && state.currentUser.token) {
            options.headers["Authorization"] = `Bearer ${state.currentUser.token}`;
        }
        if (body) {
            options.body = JSON.stringify(body);
        }
        const res = await fetch(url, options);
        if (!res.ok) throw new Error(`HTTP Error: ${res.status}`);
        return await res.json();
    } catch (err) {
        console.warn(`API call to ${service} failed. Falling back to mock.`, err);
        return null;
    }
}

// --- Catalog Rendering ---
async function fetchAndRenderProducts() {
    let productsList = [];
    if (state.apiMode === "live") {
        const liveProducts = await apiCall("product", "/products");
        if (liveProducts && liveProducts.length > 0) {
            state.products = liveProducts.map(p => ({
                product_id: p.product_id,
                name: p.name,
                description: p.description,
                price: parseFloat(p.price),
                category: p.category,
                rating: p.rating || 4.5,
                rating_count: p.rating_count || 50,
                image: p.image || "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=600&q=80",
                sizes: p.category === "Fashion" ? ["S", "M", "L", "XL"] : null
            }));
        }
    }

    productsList = state.products;

    // Filter by category
    if (state.selectedCategory !== "all") {
        productsList = productsList.filter(p => p.category === state.selectedCategory);
    }

    // Filter by search bar query
    const searchQuery = document.getElementById("product-search").value.toLowerCase();
    if (searchQuery) {
        productsList = productsList.filter(p => 
            p.name.toLowerCase().includes(searchQuery) || 
            p.description.toLowerCase().includes(searchQuery) ||
            p.category.toLowerCase().includes(searchQuery)
        );
    }

    const container = document.getElementById("products-list-container");
    container.innerHTML = "";
    document.getElementById("catalog-count-label").innerText = `Showing ${productsList.length} items`;

    if (productsList.length === 0) {
        container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-secondary);">No products match your search.</div>`;
        return;
    }

    productsList.forEach(p => {
        // Calculate stars
        let starsHtml = "";
        const fullStars = Math.floor(p.rating);
        for (let i = 0; i < 5; i++) {
            if (i < fullStars) starsHtml += '<i class="fa-solid fa-star"></i>';
            else if (i === fullStars && p.rating % 1 !== 0) starsHtml += '<i class="fa-solid fa-star-half-stroke"></i>';
            else starsHtml += '<i class="fa-regular fa-star"></i>';
        }

        const isWishlisted = state.wishlist.includes(p.product_id);
        const heartColor = isWishlisted ? "#ef4444" : "rgba(255,255,255,0.4)";
        const heartIcon = isWishlisted ? "fa-solid fa-heart" : "fa-regular fa-heart";

        const card = document.createElement("div");
        card.className = "product-card";
        card.innerHTML = `
            <div class="product-img-container" style="position: relative;">
                <img src="${p.image}" class="product-img" alt="${p.name}">
                <button class="wishlist-btn" style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.5); border: none; width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 10;" onclick="event.stopPropagation(); toggleWishlist('${p.product_id}')">
                    <i class="${heartIcon}" style="color: ${heartColor}; font-size: 16px;"></i>
                </button>
            </div>
            <div class="product-info">
                <span class="product-category">${p.category}</span>
                <h3 class="product-name">${p.name}</h3>
                <div class="product-rating">
                    <span class="stars">${starsHtml}</span>
                    <span>(${p.rating_count})</span>
                </div>
                <div class="product-footer">
                    <span class="product-price">₹${p.price.toFixed(2)}</span>
                    <button class="add-to-cart-quick" data-id="${p.product_id}" title="Quick View"><i class="fa-solid fa-eye"></i></button>
                </div>
            </div>
        `;

        // Card click opens detail modal
        card.addEventListener("click", (e) => {
            if (e.target.closest(".add-to-cart-quick")) {
                e.stopPropagation();
                openProductDetail(p.product_id);
            } else {
                openProductDetail(p.product_id);
            }
        });

        container.appendChild(card);
    });
}

// --- Detail Modal ---
function openProductDetail(productId) {
    const product = state.products.find(p => p.product_id === productId);
    if (!product) return;

    state.selectedProductDetail = product;
    state.selectedCheckoutSize = product.sizes ? product.sizes[0] : null;

    let starsHtml = "";
    const fullStars = Math.floor(product.rating);
    for (let i = 0; i < 5; i++) {
        if (i < fullStars) starsHtml += '<i class="fa-solid fa-star"></i>';
        else if (i === fullStars && product.rating % 1 !== 0) starsHtml += '<i class="fa-solid fa-star-half-stroke"></i>';
        else starsHtml += '<i class="fa-regular fa-star"></i>';
    }

    // Build sizes panel if applicable
    let sizeSelectorHtml = "";
    if (product.sizes) {
        sizeSelectorHtml = `
            <div class="size-selector-label">Select Dress Size:</div>
            <div class="size-selector" id="modal-size-picker">
                ${product.sizes.map((s, idx) => `
                    <button class="size-btn ${idx === 0 ? 'active' : ''}" data-size="${s}">${s}</button>
                `).join('')}
            </div>
        `;
    }

    const layout = document.getElementById("modal-detail-content");
    layout.innerHTML = `
        <div class="detail-img-col">
            <img src="${product.image}" class="detail-img" alt="${product.name}">
        </div>
        <div class="detail-info-col">
            <span class="detail-category">${product.category}</span>
            <h1 class="detail-title">${product.name}</h1>
            <div class="detail-rating">
                <span class="stars">${starsHtml}</span>
                <span style="color: var(--text-secondary);">(${product.rating} stars / ${product.rating_count} reviews)</span>
            </div>
            <div class="detail-price">₹${product.price.toFixed(2)}</div>
            <p class="detail-desc">${product.description}</p>
            
            ${sizeSelectorHtml}

            ${state.currentUser.role === 'admin' ? `
                <div class="modal-admin-badge">
                    <i class="fa-solid fa-user-shield"></i> Admin View Only - Shopping Disabled
                </div>
            ` : `
                <button class="btn" id="modal-add-to-cart-btn" style="margin-top: 15px; height: 50px;">
                    <i class="fa-solid fa-shopping-cart"></i> Add to Shopping Cart
                </button>
            `}
        </div>
    `;

    // Size Selection Handler
    if (product.sizes) {
        const btns = layout.querySelectorAll(".size-btn");
        btns.forEach(btn => {
            btn.addEventListener("click", () => {
                btns.forEach(b => b.classList.remove("active"));
                btn.classList.add("active");
                state.selectedCheckoutSize = btn.dataset.size;
            });
        });
    }

    // Add to Cart Handler
    if (state.currentUser.role !== 'admin') {
        document.getElementById("modal-add-to-cart-btn").addEventListener("click", () => {
            addToCart(product.product_id, 1, state.selectedCheckoutSize);
            views.productModal.classList.remove("active");
        });
    }

    views.productModal.classList.add("active");
}

// --- Cart Operations ---
async function syncCartWithBackend() {
    if (state.apiMode === "live" && state.currentUser.username !== "Guest") {
        // Send updates to FastAPI cart-service if live
        const cartItems = state.cart.map(i => ({
            user_id: state.currentUser.username,
            product_id: i.product_id,
            quantity: i.quantity,
            size: i.size || ""
        }));
        // We'll run a post call to save the user's cart state
        for (const item of cartItems) {
            await apiCall("cart", "/cart", "POST", item);
        }
    }
}

function addToCart(productId, qty = 1, size = null) {
    const product = state.products.find(p => p.product_id === productId);
    if (!product) return;

    // Check if item already exists in cart with same size
    const existing = state.cart.find(i => i.product_id === productId && i.size === size);
    if (existing) {
        existing.quantity += qty;
    } else {
        state.cart.push({
            cart_id: "cart-item-" + Date.now(),
            product_id: productId,
            name: product.name,
            price: product.price,
            image: product.image,
            size: size,
            quantity: qty
        });
    }

    renderCart();
    syncCartWithBackend();
    showToast(`Added ${product.name} ${size ? `(Size ${size})` : ''} to cart!`);
}

function updateCartQuantity(cartId, delta) {
    const item = state.cart.find(i => i.cart_id === cartId);
    if (!item) return;

    item.quantity += delta;
    if (item.quantity <= 0) {
        state.cart = state.cart.filter(i => i.cart_id !== cartId);
        showToast("Item removed from cart.", "warning");
    }

    renderCart();
    syncCartWithBackend();
}

function removeFromCart(cartId) {
    state.cart = state.cart.filter(i => i.cart_id !== cartId);
    renderCart();
    syncCartWithBackend();
    showToast("Item removed from cart.", "warning");
}

function renderCart() {
    // Persist cart state to localStorage per-user
    const cartKey = state.currentUser.username !== "Guest" ? `ecom_cart_${state.currentUser.username}` : "ecom_cart";
    localStorage.setItem(cartKey, JSON.stringify(state.cart));

    const container = document.getElementById("cart-items-container");
    container.innerHTML = "";

    let totalCount = 0;
    let totalPrice = 0;

    state.cart.forEach(item => {
        totalCount += item.quantity;
        totalPrice += item.price * item.quantity;

        const el = document.createElement("div");
        el.className = "cart-item";
        el.innerHTML = `
            <div class="cart-item-img">
                <img src="${item.image}" alt="${item.name}">
            </div>
            <div class="cart-item-details">
                <h4 class="cart-item-name">${item.name}</h4>
                <div class="cart-item-meta">${item.size ? `Size: ${item.size}` : 'Standard Edition'}</div>
                <div class="cart-item-price">₹${item.price.toFixed(2)}</div>
                <div class="cart-item-controls">
                    <div style="display: flex; align-items: center;">
                        <button class="qty-btn" onclick="updateCartQuantity('${item.cart_id}', -1)">-</button>
                        <span class="qty-val">${item.quantity}</span>
                        <button class="qty-btn" onclick="updateCartQuantity('${item.cart_id}', 1)">+</button>
                    </div>
                    <button class="remove-item-btn" onclick="removeFromCart('${item.cart_id}')"><i class="fa-solid fa-trash-can"></i> Remove</button>
                </div>
            </div>
        `;
        container.appendChild(el);
    });

    document.getElementById("cart-item-count").innerText = totalCount;
    document.getElementById("cart-total-value").innerText = `₹${totalPrice.toFixed(2)}`;

    if (state.cart.length === 0) {
        container.innerHTML = `<div style="text-align: center; color: var(--text-muted); padding: 40px 0;"><i class="fa-solid fa-cart-shopping" style="font-size: 40px; margin-bottom: 12px; opacity: 0.3;"></i><p>Your cart is empty.</p></div>`;
    }
}

async function pollOrderStatus(orderId, retries = 10) {
    if (retries <= 0) {
        showToast(`Order status check timed out. Please check your purchase history.`, "warning");
        return;
    }
    setTimeout(async () => {
        try {
            // Fetch live orders
            const liveOrders = await apiCall("order", "/orders");
            if (liveOrders) {
                const targetOrders = liveOrders.filter(o => o.order_id === orderId);
                if (targetOrders.length > 0) {
                    const status = targetOrders[0].status || "PENDING";
                    if (status === "SUCCESS") {
                        showToast(`Order ${orderId} completed successfully!`, "success");
                        // Refresh products and inventory to reflect decremented stock
                        fetchAndRenderProducts();
                        renderUserOrders();
                        return;
                    } else if (status === "FAILED") {
                        showToast(`Order ${orderId} failed (out of stock or payment failure).`, "danger");
                        fetchAndRenderProducts();
                        renderUserOrders();
                        return;
                    }
                }
            }
            pollOrderStatus(orderId, retries - 1);
        } catch (e) {
            console.error("Error polling order status:", e);
            pollOrderStatus(orderId, retries - 1);
        }
    }, 2000);
}

// --- Checkout & Payment Logic ---
function openCheckout() {
    if (state.currentUser.username === "Guest") {
        showToast("Please log in to place an order!", "warning");
        document.getElementById("nav-login-btn")?.click();
        return;
    }
    if (state.cart.length === 0) {
        showToast("Your cart is empty!", "warning");
        return;
    }

    let totalPrice = 0;
    state.cart.forEach(i => totalPrice += i.price * i.quantity);

    document.getElementById("checkout-subtotal").innerText = `₹${totalPrice.toFixed(2)}`;
    document.getElementById("checkout-total").innerText = `₹${totalPrice.toFixed(2)}`;

    // Populate checkout names automatically from the user's session profile
    if (state.currentUser && state.currentUser.name) {
        document.getElementById("checkout-name").value = state.currentUser.name;
        document.getElementById("card-name-input").value = state.currentUser.name;
    } else if (state.currentUser && state.currentUser.username !== "Guest") {
        const fallbackName = state.currentUser.username.split('@')[0];
        const formattedName = fallbackName.charAt(0).toUpperCase() + fallbackName.slice(1);
        document.getElementById("checkout-name").value = formattedName;
        document.getElementById("card-name-input").value = formattedName;
    } else {
        document.getElementById("checkout-name").value = "Jane Doe";
        document.getElementById("card-name-input").value = "Jane Doe";
    }

    views.cartDrawer.classList.remove("active");
    views.checkoutModal.classList.add("active");
}

// Card Inputs Event Listeners
const cardInputs = {
    num: document.getElementById("card-num-input"),
    name: document.getElementById("card-name-input"),
    exp: document.getElementById("card-expiry-input"),
    cvv: document.getElementById("card-cvv-input")
};

cardInputs.num.addEventListener("input", (e) => {
    let val = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    let matches = val.match(/\d{4,16}/g);
    let match = matches && matches[0] || '';
    let parts = [];

    for (let i=0, len=match.length; i<len; i+=4) {
        parts.push(match.substring(i, i+4));
    }

    if (parts.length > 0) {
        e.target.value = parts.join(' ');
    } else {
        e.target.value = val;
    }

    document.getElementById("card-preview-number").innerText = e.target.value || "•••• •••• •••• ••••";
});

cardInputs.name.addEventListener("input", (e) => {
    document.getElementById("card-preview-name").innerText = e.target.value.toUpperCase() || "JANE DOE";
});

cardInputs.exp.addEventListener("input", (e) => {
    let val = e.target.value.replace(/^([1-9]\/|[2-9])$/g, '0$1/').replace(/^(0[1-9]|1[0-2])$/g, '$1/').replace(/[^\d\/]/g, '');
    e.target.value = val;
    document.getElementById("card-preview-expiry").innerText = val || "MM/YY";
});

cardInputs.cvv.addEventListener("input", (e) => {
    let val = e.target.value.replace(/[^0-9]/g, '');
    e.target.value = val;
    document.getElementById("card-preview-cvv").innerText = val || "CVV";
});

cardInputs.cvv.addEventListener("focus", () => {
    document.getElementById("interactive-card").classList.add("flip");
});

cardInputs.cvv.addEventListener("blur", () => {
    document.getElementById("interactive-card").classList.remove("flip");
});

// Payment Method Selector Handler
const payTabs = document.querySelectorAll(".payment-tab");
payTabs.forEach(tab => {
    tab.addEventListener("click", () => {
        payTabs.forEach(t => t.classList.remove("active"));
        tab.classList.add("active");

        const payType = tab.dataset.payType;
        document.getElementById("payment-panel-card").classList.add("d-none");
        document.getElementById("payment-panel-netbanking").classList.add("d-none");
        document.getElementById("payment-panel-cod").classList.add("d-none");
        document.getElementById("credit-card-preview-wrapper").classList.add("d-none");

        if (payType === "card") {
            document.getElementById("payment-panel-card").classList.remove("d-none");
            document.getElementById("credit-card-preview-wrapper").classList.remove("d-none");
        } else if (payType === "netbanking") {
            document.getElementById("payment-panel-netbanking").classList.remove("d-none");
        } else if (payType === "cod") {
            document.getElementById("payment-panel-cod").classList.remove("d-none");
        }
    });
});

// Net banking selections
const bankOptions = document.querySelectorAll(".bank-option");
bankOptions.forEach(opt => {
    opt.addEventListener("click", () => {
        bankOptions.forEach(o => o.classList.remove("selected"));
        opt.classList.add("selected");
    });
});

// Complete Purchase / Submit Order
document.getElementById("place-order-submit-btn").addEventListener("click", async () => {
    if (state.cart.length === 0) {
        showToast("Your cart is empty", "warning");
        return;
    }

    const finalAmount = state.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const orderId = "order-" + Math.floor(100000 + Math.random() * 900000);
    const activePayType = document.querySelector(".payment-tab.active").dataset.payType;
    const shippingName = document.getElementById("checkout-name").value.trim() || "Jane Doe";
    const shippingAddress = document.getElementById("checkout-address").value.trim() || "123 Main St, Singapore 189720";
    const phone = document.getElementById("checkout-phone") ? document.getElementById("checkout-phone").value.trim() : "";

    let selectedPaymentDetail = activePayType;
    if (activePayType === "netbanking") {
        const selectedBank = document.querySelector(".bank-option.selected");
        if (selectedBank) selectedPaymentDetail = selectedBank.dataset.bank.toUpperCase();
    }

    // Close checkout modal
    views.checkoutModal.classList.remove("active");

    // Initialize Order Tracker Modal UI
    document.getElementById("tracker-order-id").innerText = `Order ID: ${orderId}`;
    
    const steps = ["step-order-created", "step-inventory-reserved", "step-payment-processed", "step-order-complete"];
    steps.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.className = "pipeline-step";
        }
    });

    document.getElementById("tracker-success-action").classList.add("d-none");
    document.getElementById("tracker-failure-action").classList.add("d-none");
    document.getElementById("order-tracker-modal").classList.add("active");

    // Start Step 1
    document.getElementById("step-order-created").classList.add("active");

    const orderTimestamp = new Date().toISOString();

    const paymentRecord = {
        payment_id: "pay-" + Math.floor(100000 + Math.random() * 900000),
        order_id: orderId,
        amount: finalAmount,
        status: "SUCCESS",
        method: selectedPaymentDetail.toUpperCase(),
        timestamp: orderTimestamp
    };

    const newOrders = state.cart.map(item => ({
        order_id: orderId,
        user_id: state.currentUser.username,
        product_id: item.product_id,
        name: item.name,
        quantity: item.quantity,
        amount: item.price * item.quantity,
        size: item.size || "",
        shipping_name: shippingName,
        shipping_address: shippingAddress,
        phone: phone,
        payment_method: selectedPaymentDetail,
        status: "PENDING",
        timestamp: orderTimestamp
    }));

    state.payments.push(paymentRecord);
    state.orders.push(...newOrders);

    if (state.apiMode === "live") {
        try {
            let wsUrl = state.endpoints.analytics.replace(/^http/, "ws") + "/analytics/ws";
            const ws = new WebSocket(wsUrl);

            ws.onopen = async () => {
                console.log("WebSocket | Connected to Event Broker at:", wsUrl);

                const realOrderIds = [];
                for (const order of newOrders) {
                    const res = await apiCall("order", "/orders", "POST", {
                        user_id: order.user_id,
                        product_id: order.product_id,
                        quantity: order.quantity,
                        amount: order.amount,
                        size: order.size,
                        shipping_name: order.shipping_name,
                        shipping_address: order.shipping_address,
                        phone: order.phone,
                        payment_method: order.payment_method
                    });
                    if (res && res.order_id) {
                        realOrderIds.push(res.order_id);
                        // Update state.orders with real order_id from backend
                        const idx = state.orders.findIndex(o => o.order_id === orderId && o.product_id === order.product_id);
                        if (idx !== -1) state.orders[idx].order_id = res.order_id;
                    }
                }
                // Use first real order_id for polling/email
                if (realOrderIds.length > 0) window._lastRealOrderId = realOrderIds[0];

                await apiCall("payment", "/payments", "POST", {
                    order_id: realOrderIds[0] || orderId,
                    amount: finalAmount,
                    method: selectedPaymentDetail
                });
            };

            ws.onmessage = (event) => {
                try {
                    const msg = JSON.parse(event.data);
                    if (msg.event_type === "order_status_update" && msg.data.order_id === orderId) {
                        const status = msg.data.status;
                        console.log("WebSocket | Received status update:", status);

                        if (status === "PENDING") {
                            document.getElementById("step-order-created").className = "pipeline-step success";
                            document.getElementById("step-inventory-reserved").className = "pipeline-step active";
                        } else if (status === "INVENTORY_RESERVED") {
                            document.getElementById("step-order-created").className = "pipeline-step success";
                            document.getElementById("step-inventory-reserved").className = "pipeline-step success";
                            document.getElementById("step-payment-processed").className = "pipeline-step active";
                        } else if (status === "INVENTORY_FAILED") {
                            document.getElementById("step-inventory-reserved").className = "pipeline-step failed";
                            document.getElementById("tracker-failure-reason").innerHTML = `<i class="fa-solid fa-circle-xmark" style="margin-right: 6px;"></i> Order Failed: Stock reservation failed (${msg.data.reason || 'Out of stock'}).`;
                            document.getElementById("tracker-failure-action").classList.remove("d-none");
                            ws.close();
                        } else if (status === "SUCCESS") {
                            document.getElementById("step-order-created").className = "pipeline-step success";
                            document.getElementById("step-inventory-reserved").className = "pipeline-step success";
                            document.getElementById("step-payment-processed").className = "pipeline-step success";
                            document.getElementById("step-order-complete").className = "pipeline-step success";
                            document.getElementById("tracker-success-action").classList.remove("d-none");
                            ws.close();
                        } else if (status === "FAILED") {
                            document.getElementById("step-payment-processed").className = "pipeline-step failed";
                            document.getElementById("tracker-failure-reason").innerHTML = `<i class="fa-solid fa-circle-xmark" style="margin-right: 6px;"></i> Order Failed: Payment processing failed.`;
                            document.getElementById("tracker-failure-action").classList.remove("d-none");
                            ws.close();
                        }
                    }
                } catch (e) {
                    console.error("WebSocket | Message parsing error:", e);
                }
            };

            const runLocalSimulation = async () => {
                // Place orders via API and capture real order IDs
                const realOrderIds = [];
                for (const order of newOrders) {
                    const res = await apiCall("order", "/orders", "POST", {
                        user_id: order.user_id,
                        product_id: order.product_id,
                        quantity: order.quantity,
                        amount: order.amount,
                        size: order.size,
                        shipping_name: order.shipping_name,
                        shipping_address: order.shipping_address,
                        phone: order.phone,
                        payment_method: order.payment_method
                    });
                    if (res && res.order_id) {
                        realOrderIds.push(res.order_id);
                        const idx = state.orders.findIndex(o => o.order_id === orderId && o.product_id === order.product_id);
                        if (idx !== -1) state.orders[idx].order_id = res.order_id;
                    }
                }
                if (realOrderIds.length > 0) window._lastRealOrderId = realOrderIds[0];
                await apiCall("payment", "/payments", "POST", {
                    order_id: realOrderIds[0] || orderId,
                    amount: finalAmount,
                    method: selectedPaymentDetail
                });

                setTimeout(() => {
                    document.getElementById("step-order-created").className = "pipeline-step success";
                    document.getElementById("step-inventory-reserved").className = "pipeline-step active";
                    setTimeout(() => {
                        document.getElementById("step-inventory-reserved").className = "pipeline-step success";
                        document.getElementById("step-payment-processed").className = "pipeline-step active";
                        setTimeout(() => {
                            document.getElementById("step-payment-processed").className = "pipeline-step success";
                            document.getElementById("step-order-complete").className = "pipeline-step active";
                            setTimeout(() => {
                                document.getElementById("step-order-complete").className = "pipeline-step success";
                                document.getElementById("tracker-success-action").classList.remove("d-none");
                            }, 800);
                        }, 800);
                    }, 800);
                }, 800);
            };

            ws.onerror = (err) => {
                console.error("WebSocket | Connection error:", err);
                runLocalSimulation();
            };

        } catch (err) {
            console.error("Order live pipeline error:", err);
            showToast("Failed to connect to backend services.", "danger");
        }
    } else {
        // --- MOCK MODE: Local Timeout Simulation ---
        setTimeout(() => {
            document.getElementById("step-order-created").className = "pipeline-step success";
            document.getElementById("step-inventory-reserved").className = "pipeline-step active";
            
            setTimeout(() => {
                document.getElementById("step-inventory-reserved").className = "pipeline-step success";
                document.getElementById("step-payment-processed").className = "pipeline-step active";
                
                setTimeout(() => {
                    document.getElementById("step-payment-processed").className = "pipeline-step success";
                    document.getElementById("step-order-complete").className = "pipeline-step active";
                    
                    setTimeout(() => {
                        document.getElementById("step-order-complete").className = "pipeline-step success";
                        document.getElementById("tracker-success-action").classList.remove("d-none");
                    }, 800);
                }, 800);
            }, 800);
        }, 800);
    }
});

// --- Email Notification ---
async function sendOrderConfirmationEmail(orderItems, totalPaid) {
    if (!orderItems || orderItems.length === 0) return;

    const realOrderId = window._lastRealOrderId || orderItems[0].order_id;
    const userName = orderItems[0].shipping_name || state.currentUser.name || state.currentUser.username;
    const userEmail = state.currentUser.username;
    const orderDate = new Date(orderItems[0].timestamp).toLocaleString();
    const paymentMethod = orderItems[0].payment_method || "CARD";
    const firstItem = orderItems[0];

    if (state.apiMode === "live") {
        try {
            await fetch(`${state.endpoints.auth}/auth/send-order-email`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${state.currentUser.token}`
                },
                body: JSON.stringify({
                    to: userEmail,
                    order_id: realOrderId,
                    user_name: userName,
                    shipping_name: firstItem.shipping_name || "",
                    shipping_address: firstItem.shipping_address || "",
                    phone: firstItem.phone || "",
                    payment_method: paymentMethod,
                    order_date: orderDate,
                    items: orderItems.map(o => ({
                        name: o.name,
                        quantity: o.quantity,
                        amount: o.amount,
                        size: o.size || ""
                    })),
                    total_paid: totalPaid
                })
            });
            showToast(`Order confirmation email sent to ${userEmail}!`, "success");
        } catch (err) {
            console.warn("Order email failed:", err);
        }
    }
}

// Close Tracker Modal manually (fallback top-right close button)
document.getElementById("close-order-tracker-btn").addEventListener("click", async () => {
    document.getElementById("order-tracker-modal").classList.remove("active");

    const realId = window._lastRealOrderId || (state.orders[state.orders.length - 1]?.order_id);
    const lastOrderItems = state.orders.filter(o => o.order_id === realId);
    const totalPaid = lastOrderItems.reduce((sum, item) => sum + item.amount, 0);
    await sendOrderConfirmationEmail(lastOrderItems.length ? lastOrderItems : newOrders, totalPaid || finalAmount);

    state.cart = [];
    renderCart();
    showView("storefront");
    fetchAndRenderProducts();
});

// Close Tracker Modal on SUCCESS
document.getElementById("btn-close-tracker-modal").addEventListener("click", async () => {
    document.getElementById("order-tracker-modal").classList.remove("active");

    const realId = window._lastRealOrderId || (state.orders[state.orders.length - 1]?.order_id);
    const lastOrderItems = state.orders.filter(o => o.order_id === realId);
    const totalPaid = lastOrderItems.reduce((sum, item) => sum + item.amount, 0);
    await sendOrderConfirmationEmail(lastOrderItems.length ? lastOrderItems : newOrders, totalPaid || finalAmount);

    state.cart = [];
    renderCart();
    showView("storefront");
    fetchAndRenderProducts();
});

// Close Tracker Modal on FAILURE
document.getElementById("btn-close-tracker-fail-btn").addEventListener("click", () => {
    document.getElementById("order-tracker-modal").classList.remove("active");
    showView("storefront");
    document.getElementById("cart-drawer-trigger").click(); // reopen cart
});

// --- Admin Panel Logic ---
const adminTabButtons = document.querySelectorAll(".sidebar-btn");
adminTabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        adminTabButtons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        // Hide all admin panels
        document.querySelectorAll(".admin-panel-content").forEach(p => p.classList.add("d-none"));
        // Show target panel
        document.getElementById(`admin-panel-${btn.dataset.adminPanel}`).classList.remove("d-none");

        if (btn.dataset.adminPanel === "dashboard") {
            renderAdminDashboard();
        } else if (btn.dataset.adminPanel === "products") {
            renderAdminProducts();
        } else if (btn.dataset.adminPanel === "inventory") {
            renderAdminInventory();
        } else if (btn.dataset.adminPanel === "orders") {
            renderAdminOrders();
        } else if (btn.dataset.adminPanel === "payments") {
            renderAdminPayments();
        } else if (btn.dataset.adminPanel === "users") {
            renderAdminUsers();
        }
    });
});

async function renderAdminDashboard() {
    // Fetch live data in live mode for accurate stats
    if (state.apiMode === "live") {
        try {
            const liveOrders = await apiCall("order", "/orders");
            if (liveOrders) {
                state.orders = liveOrders.map(o => ({
                    order_id: o.order_id,
                    user_id: o.user_id,
                    product_id: o.product_id,
                    name: state.products.find(p => p.product_id === o.product_id)?.name || o.product_id,
                    quantity: o.quantity,
                    amount: o.amount,
                    size: o.size || "",
                    shipping_name: o.shipping_name || "",
                    shipping_address: o.shipping_address || "",
                    phone: o.phone || "",
                    payment_method: o.payment_method || "",
                    status: o.status || "PENDING",
                    timestamp: o.timestamp || new Date().toISOString()
                }));
            }
        } catch (err) {
            console.error("Dashboard: Failed to sync orders", err);
        }
        try {
            const livePayments = await apiCall("payment", "/payments");
            if (livePayments) {
                state.payments = livePayments.map(p => ({
                    payment_id: p.payment_id || `pay-${p.order_id}`,
                    order_id: p.order_id,
                    amount: p.amount,
                    status: p.status || "SUCCESS",
                    method: p.method || "CARD",
                    timestamp: p.timestamp || new Date().toISOString()
                }));
            }
        } catch (err) {
            console.error("Dashboard: Failed to sync payments", err);
        }
    }

    const totalRev = state.payments
        .filter(p => p.status === "SUCCESS")
        .reduce((sum, p) => sum + p.amount, 0);

    const uniqueOrders = new Set(state.orders.map(o => o.order_id));
    
    document.getElementById("stat-revenue").innerText = `₹${totalRev.toFixed(2)}`;
    document.getElementById("stat-orders").innerText = uniqueOrders.size;
    document.getElementById("stat-aov").innerText = `₹${(uniqueOrders.size > 0 ? totalRev / uniqueOrders.size : 0.0).toFixed(2)}`;
    
    if (state.apiMode === "live") {
        refreshAnalyticsData();
    }
}

// Admin Stats Dashboard Perspectives Toggling
const btnPerspCompany = document.getElementById("btn-perspective-company");
const btnPerspCustomer = document.getElementById("btn-perspective-customer");
const btnPerspEngineer = document.getElementById("btn-perspective-engineer");

const panelCompany = document.getElementById("perspective-panel-company");
const panelCustomer = document.getElementById("perspective-panel-customer");
const panelEngineer = document.getElementById("perspective-panel-engineer");

function switchPerspective(activeBtn, activePanel) {
    [btnPerspCompany, btnPerspCustomer, btnPerspEngineer].forEach(btn => btn?.classList.remove("active"));
    [panelCompany, panelCustomer, panelEngineer].forEach(panel => panel?.classList.add("d-none"));
    activeBtn.classList.add("active");
    activePanel.classList.remove("d-none");
    refreshAnalyticsData();
}

btnPerspCompany?.addEventListener("click", () => switchPerspective(btnPerspCompany, panelCompany));
btnPerspCustomer?.addEventListener("click", () => switchPerspective(btnPerspCustomer, panelCustomer));
btnPerspEngineer?.addEventListener("click", () => switchPerspective(btnPerspEngineer, panelEngineer));

async function refreshAnalyticsData() {
    if (state.apiMode !== "live") return;
    
    // 1. Fetch Company Perspective (Sales)
    try {
        const revRes = await fetch(`${state.endpoints.analytics}/v1/analytics/company/revenue`);
        if (revRes.ok) {
            const data = await revRes.json();
            document.getElementById("stat-revenue").innerText = `₹${parseFloat(data.total_revenue || 0.0).toFixed(2)}`;
            document.getElementById("stat-orders").innerText = data.total_orders || 0;
            document.getElementById("stat-aov").innerText = `₹${parseFloat(data.average_order_value || 0.0).toFixed(2)}`;
            
            const distList = document.getElementById("product-sales-distribution-list");
            if (data.product_sales && Object.keys(data.product_sales).length > 0) {
                distList.innerHTML = Object.entries(data.product_sales)
                    .map(([pid, qty]) => `
                        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <span>Product ID: <strong>${pid}</strong></span>
                            <span style="color: var(--primary); font-weight: bold;">${qty} units sold</span>
                        </div>
                    `).join("");
            } else {
                distList.innerHTML = "No sales recorded in S3 stage bucket yet.";
            }
        }
    } catch (err) {
        console.warn("Failed to fetch revenue analytics", err);
    }

    // 2. Fetch Customer Perspective (Abandonment)
    try {
        const abRes = await fetch(`${state.endpoints.analytics}/v1/analytics/customer/abandoned-carts`);
        if (abRes.ok) {
            const data = await abRes.json();
            document.getElementById("stat-abandoned-count").innerText = data.abandoned_count || 0;
            
            const tbody = document.getElementById("table-abandoned-carts-body");
            if (data.abandoned_carts && data.abandoned_carts.length > 0) {
                tbody.innerHTML = data.abandoned_carts.map(cart => `
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.05); text-align: left;">
                        <td style="padding: 12px 10px;">${cart.user_id}</td>
                        <td style="padding: 12px 10px;">${cart.product_id}</td>
                        <td style="padding: 12px 10px;">${new Date(cart.added_at * 1000).toLocaleTimeString()}</td>
                        <td style="padding: 12px 10px; color: var(--warning);">${Math.round(cart.abandoned_duration)}s idle</td>
                    </tr>
                `).join("");
            } else {
                tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; padding: 25px; color: var(--text-muted);">No active abandoned carts detected.</td></tr>`;
            }
        }
    } catch (err) {
        console.warn("Failed to fetch cart abandonment analytics", err);
    }

    // 3. Fetch Engineer Perspective (Reliability SLA & TAT)
    try {
        const engRes = await fetch(`${state.endpoints.analytics}/v1/analytics/engineer/reliability`);
        if (engRes.ok) {
            const data = await engRes.json();
            const rawTat = data.average_tat_seconds !== undefined ? parseFloat(data.average_tat_seconds) : 0.0;
            const rawSla = data.success_rate_sla !== undefined ? parseFloat(data.success_rate_sla) : 100.0;
            
            document.getElementById("stat-sla-percentage").innerText = `${rawSla.toFixed(1)}%`;
            document.getElementById("stat-avg-tat").innerText = `${rawTat.toFixed(2)}s`;
            
            const alarmLog = document.getElementById("dashboard-recent-log");
            if (rawTat > 5.0) {
                alarmLog.innerHTML = `<span style="color: var(--danger); font-weight: bold;"><i class="fa-solid fa-triangle-exclamation"></i> SLA LATENCY BREACH ALERT:</span> Turn Around Time (${rawTat.toFixed(2)}s) exceeds safety threshold of 5.0s!`;
            } else {
                alarmLog.innerHTML = `<span style="color: var(--success);"><i class="fa-solid fa-circle-check"></i> SLA HEALTHY:</span> average processing TAT is ${rawTat.toFixed(2)}s. Operating within boundaries.`;
            }
        }
    } catch (err) {
        console.warn("Failed to fetch engineer metrics", err);
    }
}

document.getElementById("btn-trigger-cart-recovery")?.addEventListener("click", async () => {
    if (state.apiMode !== "live") {
        showToast("Cart recovery simulation only runs in Live API Mode.", "warning");
        return;
    }
    showToast("Triggering automated cart recovery notifications...", "warning");
    setTimeout(() => {
        showToast("Recovery messages broadcasted to SNS & logged successfully!", "success");
    }, 1000);
});

async function renderAdminInventory() {
    const tbody = document.getElementById("admin-inventory-rows");
    tbody.innerHTML = "";

    if (state.apiMode === "live") {
        try {
            await Promise.all(state.products.map(async p => {
                const inv = await apiCall("inventory", `/inventory/${p.product_id}`);
                if (inv && inv.stock !== undefined) {
                    state.inventory[p.product_id] = inv.stock;
                }
            }));
        } catch (err) {
            console.error("Failed to sync live inventory", err);
        }
    }

    state.products.forEach(p => {
        const stock = state.inventory[p.product_id] !== undefined ? state.inventory[p.product_id] : 10;
        
        let badgeClass = "badge-success";
        let statusText = "In Stock";
        if (stock === 0) {
            badgeClass = "badge-danger";
            statusText = "Out of Stock";
        } else if (stock < 5) {
            badgeClass = "badge-warning";
            statusText = "Low Stock";
        }

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><strong>${p.name}</strong></td>
            <td>${p.category}</td>
            <td>₹${p.price.toFixed(2)}</td>
            <td>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <strong style="font-size: 16px; min-width: 40px; color: var(--text-primary);">${stock}</strong>
                    <input type="number" min="0" value="${stock}" class="form-input" style="width: 70px; padding: 4px 8px; margin: 0; background: rgba(255,255,255,0.05); border-color: rgba(255,255,255,0.1);" id="input-stock-${p.product_id}">
                    <button class="btn btn-primary" style="padding: 4px 10px; font-size: 12px; margin: 0; border-radius: 4px;" onclick="updateLocalStock('${p.product_id}')">Update</button>
                </div>
            </td>
            <td><span class="badge ${badgeClass}">${statusText}</span></td>
        `;

        tbody.appendChild(tr);
    });
}

window.updateLocalStock = async function(productId) {
    const input = document.getElementById(`input-stock-${productId}`);
    const newStock = parseInt(input.value);
    if (isNaN(newStock) || newStock < 0) {
        showToast("Invalid stock amount!", "danger");
        return;
    }

    try {
        if (state.apiMode === "live") {
            await apiCall("inventory", `/inventory/${productId}?stock=${newStock}`, "PUT");
        }
        state.inventory[productId] = newStock;
        showToast("Stock updated successfully!", "success");
        renderAdminInventory();
    } catch (err) {
        console.error("Failed to update stock:", err);
        showToast("Failed to update stock in database", "danger");
    }
};

async function renderAdminOrders() {
    const tbody = document.getElementById("admin-orders-rows");
    tbody.innerHTML = "";

    if (state.apiMode === "live") {
        try {
            const liveOrders = await apiCall("order", "/orders");
            if (liveOrders) {
                state.orders = liveOrders.map(o => ({
                    order_id: o.order_id,
                    user_id: o.user_id,
                    product_id: o.product_id,
                    name: state.products.find(p => p.product_id === o.product_id)?.name || o.product_id,
                    quantity: o.quantity,
                    amount: o.amount,
                    size: o.size || "",
                    shipping_name: o.shipping_name || "",
                    shipping_address: o.shipping_address || "",
                    phone: o.phone || "",
                    payment_method: o.payment_method || "",
                    status: o.status || "PENDING",
                    timestamp: o.timestamp || new Date().toISOString()
                }));
            }
        } catch (err) {
            console.error("Failed to sync live orders", err);
        }
    }

    if (state.orders.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-muted);">No orders placed yet.</td></tr>`;
        return;
    }

    // Sort orders descending
    const sortedOrders = [...state.orders].sort((a,b) => new Date(b.timestamp) - new Date(a.timestamp));

    sortedOrders.forEach(o => {
        const timeStr = new Date(o.timestamp).toLocaleString();
        
        const statuses = ["PENDING", "SHIPPED", "DELIVERED", "CANCELLED"];
        const selectHtml = `
            <select class="order-status-select" data-order-id="${o.order_id}">
                ${statuses.map(s => `<option value="${s}" ${o.status === s ? 'selected' : ''}>${s}</option>`).join('')}
            </select>
        `;

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><code>${o.order_id}</code></td>
            <td>
                <strong>${o.user_id}</strong>
                ${o.shipping_name ? `<br><small style="color: var(--text-secondary);">${o.shipping_name}</small>` : ''}
                ${o.phone ? `<br><small style="color: var(--text-secondary);">📞 ${o.phone}</small>` : ''}
                ${o.shipping_address ? `<br><small style="color: var(--text-muted); font-size: 11px;">📍 ${o.shipping_address}</small>` : ''}
            </td>
            <td>${o.name} ${o.size ? `(${o.size})` : ''}</td>
            <td>${o.quantity}</td>
            <td>₹${o.amount.toFixed(2)}</td>
            <td><span class="badge badge-${o.status === 'DELIVERED' ? 'success' : o.status === 'CANCELLED' ? 'danger' : o.status === 'SHIPPED' ? 'accent' : 'warning'}">${o.status}</span></td>
            <td>${timeStr}</td>
            <td>${selectHtml}</td>
        `;

        tr.querySelector(".order-status-select").addEventListener("change", async (e) => {
            const newStatus = e.target.value;
            
            if (state.apiMode === "live") {
                try {
                    // Update status in the backend order-service database
                    await apiCall("order", `/orders/${o.order_id}/status?status=${newStatus}`, "PUT");
                } catch (err) {
                    console.error("Failed to update order status on server", err);
                    showToast("Failed to update order status on server.", "danger");
                    return;
                }
            }

            state.orders.forEach(ord => {
                if (ord.order_id === o.order_id) {
                    ord.status = newStatus;
                }
            });
            showToast(`Order ${o.order_id} status updated to ${newStatus}`);
            renderAdminOrders();
            renderAdminDashboard();
        });

        tbody.appendChild(tr);
    });
}

// --- Product Catalog Management & Editing ---
function renderAdminProducts() {
    const tbody = document.getElementById("admin-products-rows");
    tbody.innerHTML = "";

    state.products.forEach(p => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><img src="${p.image}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px;"></td>
            <td><strong>${p.name}</strong></td>
            <td>${p.category}</td>
            <td>₹${p.price.toFixed(2)}</td>
            <td class="actions-cell">
                <button class="icon-btn edit-product-btn" data-id="${p.product_id}" title="Edit Product"><i class="fa-solid fa-pen"></i></button>
                <button class="icon-btn delete delete-product-btn" data-id="${p.product_id}" title="Delete Product"><i class="fa-solid fa-trash"></i></button>
            </td>
        `;

        tr.querySelector(".edit-product-btn").addEventListener("click", () => {
            openProductFormModal(p.product_id);
        });

        tr.querySelector(".delete-product-btn").addEventListener("click", async () => {
            if (confirm(`Are you sure you want to delete ${p.name}?`)) {
                if (state.apiMode === "live") {
                    const resp = await apiCall("product", `/products/${p.product_id}`, "DELETE");
                    if (!resp) {
                        showToast("Failed to delete product on API Gateway.", "danger");
                        return;
                    }
                }

                state.products = state.products.filter(prod => prod.product_id !== p.product_id);
                delete state.inventory[p.product_id];

                showToast("Product deleted successfully.", "warning");
                renderAdminProducts();
                renderAdminInventory();
                fetchAndRenderProducts();
                renderAdminDashboard();
            }
        });

        tbody.appendChild(tr);
    });
}

function openProductFormModal(productId = null) {
    const title = document.getElementById("product-form-title");
    const form = document.getElementById("product-upsert-form");
    const submitBtn = document.getElementById("product-form-submit-btn");

    if (productId) {
        const p = state.products.find(prod => prod.product_id === productId);
        if (!p) return;

        title.innerText = "Edit Product Details";
        document.getElementById("form-prod-id").value = p.product_id;
        document.getElementById("form-prod-name").value = p.name;
        document.getElementById("form-prod-category").value = p.category;
        document.getElementById("form-prod-price").value = p.price;
        document.getElementById("form-prod-desc").value = p.description || "";
        document.getElementById("form-prod-img").value = p.image || "";
        submitBtn.innerText = "Save Product Changes";
    } else {
        title.innerText = "Add New Product to Database";
        form.reset();
        document.getElementById("form-prod-id").value = "";
        submitBtn.innerText = "Create Product via API";
    }

    views.productFormModal.classList.add("active");
}

document.getElementById("product-upsert-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const productId = document.getElementById("form-prod-id").value;
    const name = document.getElementById("form-prod-name").value;
    const category = document.getElementById("form-prod-category").value;
    const price = parseFloat(document.getElementById("form-prod-price").value);
    const description = document.getElementById("form-prod-desc").value;
    const image = document.getElementById("form-prod-img").value;

    if (productId) {
        const p = state.products.find(prod => prod.product_id === productId);
        if (p) {
            if (state.apiMode === "live") {
                const resp = await apiCall("product", `/products/${productId}`, "PUT", {
                    name,
                    description,
                    price,
                    category,
                    image
                });
                if (!resp) {
                    showToast("Failed to update product on API Gateway.", "danger");
                    return;
                }
            }
            p.name = name;
            p.category = category;
            p.price = price;
            p.description = description;
            p.image = image;
            showToast("Product details updated successfully!");
        }
    } else {
        const newId = "prod-" + Date.now();
        const newProduct = {
            product_id: newId,
            name,
            description,
            price,
            category,
            rating: 4.5,
            rating_count: 1,
            image,
            sizes: category === "Fashion" ? ["S", "M", "L", "XL"] : null
        };

        let actualId = newId;
        if (state.apiMode === "live") {
            const resp = await apiCall("product", "/products", "POST", {
                name,
                description,
                price,
                category,
                image
            });
            if (resp && resp.product_id) {
                actualId = resp.product_id;
                newProduct.product_id = actualId;
                
                const invResp = await apiCall("inventory", "/inventory", "POST", {
                    product_id: actualId,
                    stock: 20
                });
                if (!invResp) {
                    showToast("Product created, but inventory setup failed.", "warning");
                }
            } else {
                showToast("Failed to create product on API Gateway.", "danger");
                return;
            }
        }

        state.products.push(newProduct);
        state.inventory[actualId] = 20;
        showToast("New product created successfully!");
    }

    views.productFormModal.classList.remove("active");
    renderAdminProducts();
    renderAdminInventory();
    fetchAndRenderProducts();
    renderAdminDashboard();
});

document.getElementById("close-product-form-modal").addEventListener("click", () => {
    views.productFormModal.classList.remove("active");
});

document.getElementById("btn-show-add-product-modal").addEventListener("click", () => {
    openProductFormModal(null);
});

// --- Payments Ledger ---
async function renderAdminPayments() {
    const tbody = document.getElementById("admin-payments-rows");
    tbody.innerHTML = "";

    if (state.apiMode === "live") {
        try {
            const livePayments = await apiCall("payment", "/payments");
            if (livePayments) {
                state.payments = livePayments.map(p => ({
                    payment_id: p.payment_id || `pay-${p.order_id}`,
                    order_id: p.order_id,
                    amount: p.amount,
                    status: p.status || "SUCCESS",
                    method: p.method || "CARD",
                    timestamp: p.timestamp || new Date().toISOString()
                }));
            }
        } catch (err) {
            console.error("Failed to sync live payments", err);
        }
    }

    if (state.payments.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-muted);">No payment records found.</td></tr>`;
        return;
    }

    const sortedPayments = [...state.payments].sort((a,b) => new Date(b.timestamp) - new Date(a.timestamp));

    sortedPayments.forEach(p => {
        const timeStr = new Date(p.timestamp).toLocaleString();
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><code>${p.payment_id}</code></td>
            <td><code>${p.order_id}</code></td>
            <td style="font-weight: 700; color: var(--success);">₹${p.amount.toFixed(2)}</td>
            <td><span class="badge badge-accent">${p.method}</span></td>
            <td><span class="badge badge-success">${p.status}</span></td>
            <td>${timeStr}</td>
        `;
        tbody.appendChild(tr);
    });
}

// --- Customer Order History ---
async function renderUserOrders() {
    const container = document.getElementById("user-orders-container");
    container.innerHTML = "";

    if (state.apiMode === "live") {
        try {
            const liveOrders = await apiCall("order", "/orders");
            if (liveOrders) {
                state.orders = liveOrders.map(o => ({
                    order_id: o.order_id,
                    user_id: o.user_id,
                    product_id: o.product_id,
                    name: state.products.find(p => p.product_id === o.product_id)?.name || o.product_id,
                    quantity: o.quantity,
                    amount: o.amount,
                    size: o.size || "",
                    shipping_name: o.shipping_name || "",
                    shipping_address: o.shipping_address || "",
                    phone: o.phone || "",
                    payment_method: o.payment_method || "",
                    status: o.status || "PENDING",
                    timestamp: o.timestamp || new Date().toISOString()
                }));
            }
        } catch (err) {
            console.error("Failed to sync live orders", err);
        }
    }

    const userOrders = state.orders.filter(o => o.user_id === state.currentUser.username);
    document.getElementById("user-orders-count-label").innerText = `${userOrders.length} order${userOrders.length !== 1 ? 's' : ''} placed`;

    if (userOrders.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; color: var(--text-secondary); padding: 50px 0;">
                <i class="fa-solid fa-clock-rotate-left" style="font-size: 48px; opacity: 0.2; margin-bottom: 15px;"></i>
                <p style="font-size: 16px;">You haven't placed any orders yet.</p>
                <button class="btn" style="margin-top: 15px;" onclick="showView('storefront')">Go to Shop</button>
            </div>
        `;
        return;
    }

    const ordersGrouped = {};
    userOrders.forEach(o => {
        if (!ordersGrouped[o.order_id]) {
            ordersGrouped[o.order_id] = {
                order_id: o.order_id,
                timestamp: o.timestamp,
                status: o.status,
                items: []
            };
        }
        ordersGrouped[o.order_id].items.push(o);
    });

    const sortedGrouped = Object.values(ordersGrouped).sort((a,b) => new Date(b.timestamp) - new Date(a.timestamp));

    sortedGrouped.forEach(order => {
        const timeStr = new Date(order.timestamp).toLocaleString();
        const totalAmount = order.items.reduce((sum, item) => sum + item.amount, 0);
        
        let itemsHtml = "";
        order.items.forEach(item => {
            const product = state.products.find(p => p.product_id === item.product_id) || { image: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500&q=80" };
            itemsHtml += `
                <div class="user-order-body">
                    <img src="${product.image}" class="user-order-img" alt="${item.name}">
                    <div class="user-order-info">
                        <h4 class="user-order-name">${item.name}</h4>
                        <div class="user-order-meta">${item.size ? `Size: ${item.size}` : 'Standard Edition'} &times; ${item.quantity}</div>
                    </div>
                    <div style="font-weight: 600;">₹${item.amount.toFixed(2)}</div>
                </div>
            `;
        });

        const steps = ["PENDING", "SHIPPED", "DELIVERED"];
        let currentStepIdx = steps.indexOf(order.status);

        let timelineHtml = "";
        if (order.status === "CANCELLED") {
            timelineHtml = `
                <div class="modal-admin-badge" style="background: rgba(239, 68, 68, 0.1); color: var(--danger); border-color: rgba(239, 68, 68, 0.2); margin-top: 15px;">
                    <i class="fa-solid fa-circle-xmark"></i> This order was cancelled.
                </div>
            `;
        } else {
            timelineHtml = `
                <div class="order-status-tracker">
                    <div class="status-connector" style="width: ${currentStepIdx === 1 ? '50%' : currentStepIdx === 2 ? '100%' : '0%'};"></div>
                    <div class="order-status-step ${currentStepIdx >= 0 ? (currentStepIdx === 0 ? 'active' : 'completed') : ''}">
                        <div class="status-dot"><i class="fa-solid fa-receipt"></i></div>
                        <div class="status-label">Placed</div>
                    </div>
                    <div class="order-status-step ${currentStepIdx >= 1 ? (currentStepIdx === 1 ? 'active' : 'completed') : ''}">
                        <div class="status-dot"><i class="fa-solid fa-truck-fast"></i></div>
                        <div class="status-label">Shipped</div>
                    </div>
                    <div class="order-status-step ${currentStepIdx >= 2 ? (currentStepIdx === 2 ? 'active' : 'completed') : ''}">
                        <div class="status-dot"><i class="fa-solid fa-house-chimney-user"></i></div>
                        <div class="status-label">Delivered</div>
                    </div>
                </div>
            `;
        }

        const firstItem = order.items[0] || {};
        const shippingDetailsHtml = (firstItem.shipping_name || firstItem.phone || firstItem.payment_method) ? `
            <div style="background: rgba(255,255,255,0.02); border-radius: 10px; padding: 12px 16px; margin: 10px 0; border: 1px solid var(--glass-border); font-size: 13px; color: var(--text-secondary);">
                ${firstItem.shipping_name ? `<div><i class="fa-solid fa-user" style="margin-right: 6px;"></i> ${firstItem.shipping_name}</div>` : ''}
                ${firstItem.phone ? `<div style="margin-top: 4px;"><i class="fa-solid fa-phone" style="margin-right: 6px;"></i> ${firstItem.phone}</div>` : ''}
                ${firstItem.shipping_address ? `<div style="margin-top: 4px;"><i class="fa-solid fa-location-dot" style="margin-right: 6px;"></i> ${firstItem.shipping_address}</div>` : ''}
                ${firstItem.payment_method ? `<div style="margin-top: 4px;"><i class="fa-solid fa-credit-card" style="margin-right: 6px;"></i> Paid via ${firstItem.payment_method.toUpperCase()}</div>` : ''}
            </div>
        ` : '';

        const card = document.createElement("div");
        card.className = "user-order-card";
        card.innerHTML = `
            <div class="user-order-header">
                <div>
                    <span class="user-order-date">${timeStr}</span>
                    <div class="user-order-id" style="margin-top: 4px;">ID: ${order.order_id}</div>
                </div>
                <div class="badge badge-${order.status === 'DELIVERED' ? 'success' : order.status === 'CANCELLED' ? 'danger' : order.status === 'SHIPPED' ? 'accent' : 'warning'}">
                    ${order.status}
                </div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 15px;">
                ${itemsHtml}
            </div>
            ${shippingDetailsHtml}
            <div class="user-order-price-qty">
                <span style="color: var(--text-secondary);">Total Paid:</span>
                <span class="user-order-total">₹${totalAmount.toFixed(2)}</span>
            </div>
            ${timelineHtml}
        `;
        container.appendChild(card);
    });
}

// --- Auth System ---
const loginForm = document.getElementById("login-form");
const signupForm = document.getElementById("signup-form");
const verifyCodeForm = document.getElementById("verify-code-form");
const authToggleLink = document.getElementById("link-auth-toggle");
const authTextPrompt = document.getElementById("auth-text-prompt");
const authFooterContainer = document.getElementById("auth-footer-container");
let loginType = "user"; // 'user' or 'admin'

authToggleLink.addEventListener("click", (e) => {
    e.preventDefault();
    if (loginForm.classList.contains("d-none")) {
        // Show Login
        loginForm.classList.remove("d-none");
        signupForm.classList.add("d-none");
        verifyCodeForm.classList.add("d-none");
        authTextPrompt.innerText = "Don't have an account?";
        authToggleLink.innerText = "Create account";
    } else {
        // Show Signup
        loginForm.classList.add("d-none");
        signupForm.classList.remove("d-none");
        verifyCodeForm.classList.add("d-none");
        authTextPrompt.innerText = "Already have an account?";
        authToggleLink.innerText = "Login";
    }
});

document.getElementById("tab-user-login").addEventListener("click", () => {
    document.getElementById("tab-user-login").classList.add("active", "btn-primary");
    document.getElementById("tab-user-login").style.borderColor = "var(--primary)";
    document.getElementById("tab-admin-login").classList.remove("active");
    document.getElementById("tab-admin-login").style.borderColor = "";
    document.getElementById("login-username").value = "madhumithab6825@gmail.com";
    authFooterContainer.classList.remove("d-none");
    loginForm.classList.remove("d-none");
    signupForm.classList.add("d-none");
    verifyCodeForm.classList.add("d-none");
    authTextPrompt.innerText = "Don't have an account?";
    authToggleLink.innerText = "Create account";
    loginType = "user";
});

document.getElementById("tab-admin-login").addEventListener("click", () => {
    document.getElementById("tab-admin-login").classList.add("active");
    document.getElementById("tab-admin-login").style.borderColor = "var(--primary)";
    document.getElementById("tab-user-login").classList.remove("active");
    document.getElementById("tab-user-login").style.borderColor = "";
    document.getElementById("login-username").value = "madhumithamalu6@gmail.com";
    authFooterContainer.classList.add("d-none");
    loginForm.classList.remove("d-none");
    signupForm.classList.add("d-none");
    verifyCodeForm.classList.add("d-none");
    loginType = "admin";
});

signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("signup-name").value;
    const email = document.getElementById("signup-email").value;
    const password = document.getElementById("signup-password").value;
    const confirmPassword = document.getElementById("signup-confirm-password").value;

    if (password !== confirmPassword) {
        showToast("Passwords do not match", "danger");
        return;
    }

    const passwordErrors = [];
    if (password.length < 8) passwordErrors.push("at least 8 characters");
    if (!/[A-Z]/.test(password)) passwordErrors.push("one uppercase letter");
    if (!/[a-z]/.test(password)) passwordErrors.push("one lowercase letter");
    if (!/[0-9]/.test(password)) passwordErrors.push("one number");
    if (!/[!@#$%^&*(),.?\":{}|<>]/.test(password)) passwordErrors.push("one special character (!@#$%^&* etc.)");

    if (passwordErrors.length > 0) {
        showToast(`Password needs: ${passwordErrors.join(", ")}`, "danger");
        return;
    }

    if (state.apiMode === "live") {
        try {
            showToast("Registering account...", "warning");
            const response = await fetch(`${state.endpoints.auth}/auth/register`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password,
                    confirm_password: confirmPassword
                })
            });

            if (response.ok) {
                const data = await response.json();
                showToast("Verification code sent to your email!", "success");
                loginForm.classList.add("d-none");
                signupForm.classList.add("d-none");
                verifyCodeForm.classList.remove("d-none");
                authTextPrompt.innerText = "Back to";
                authToggleLink.innerText = "Login";
                verifyCodeForm.dataset.email = email;
            } else {
                const err = await response.json();
                showToast(err.detail || "Registration failed.", "danger");
            }
        } catch (err) {
            console.error("Auth register error:", err);
            showToast("Signup request failed. Check internet.", "danger");
        }
    } else {
        showToast("Registration successful (Mock Mode)!", "success");
        loginForm.classList.remove("d-none");
        signupForm.classList.add("d-none");
        authTextPrompt.innerText = "Don't have an account?";
        authToggleLink.innerText = "Create account";
    }
});

verifyCodeForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = verifyCodeForm.dataset.email;
    const code = document.getElementById("verify-code").value;

    if (state.apiMode === "live") {
        try {
            showToast("Verifying code...", "warning");
            const response = await fetch(`${state.endpoints.auth}/auth/verify`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: email, verification_code: code })
            });

            if (response.ok) {
                showToast("Account verified successfully! Please log in.", "success");
                verifyCodeForm.classList.add("d-none");
                loginForm.classList.remove("d-none");
                document.getElementById("login-username").value = email;
                document.getElementById("login-password").value = "";
                authTextPrompt.innerText = "Don't have an account?";
                authToggleLink.innerText = "Create account";
            } else {
                const err = await response.json();
                showToast(err.detail || "Verification failed.", "danger");
            }
        } catch (err) {
            console.error("Auth verify error:", err);
            showToast("Verification request failed.", "danger");
        }
    } else {
        showToast("Verified and logged in (Mock Mode)!", "success");
        state.currentUser = {
            username: email || "user@example.com",
            role: "user",
            token: btoa(`${email || 'user'}:${Date.now()}`)
        };
        sessionStorage.setItem("jwt_token", state.currentUser.token);
        sessionStorage.setItem("username", state.currentUser.username);
        sessionStorage.setItem("role", "user");
        updateAuthUI();
        showView("storefront");
    }
});

loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    let token = "";
    let displayName = "";
    let loginSuccess = false;

    if (state.apiMode === "live") {
        try {
            showToast("Authenticating...", "warning");
            const response = await fetch(`${state.endpoints.auth}/auth/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: username,
                    password: password
                })
            });

            if (response.ok) {
                const data = await response.json();
                token = data.token;
                displayName = data.name || data.username.split('@')[0];
                try {
                    const payload = JSON.parse(atob(token.split('.')[1]));
                    loginType = payload.role || "user";
                    const adminEmails = ["madhumithamalu6@gmail.com", "admin@gmail.com"];
                    if (adminEmails.includes(username) || username.toLowerCase().includes("admin")) {
                        loginType = "admin";
                    }
                } catch (e) {
                    loginType = "user";
                }
                loginSuccess = true;
                showToast(`Logged in successfully as ${username}!`, "success");
            } else {
                const errData = await response.json();
                console.warn("Login failed:", errData);
                showToast(errData.detail || "Authentication failed. Invalid username or password.", "danger");
                return;
            }
        } catch (err) {
            console.error("Auth request error:", err);
            showToast("Authentication server unreachable. Check connection.", "danger");
            return;
        }
    } else {
        // Mock Mode Fallback
        token = btoa(`${username}:${Date.now()}`);
        displayName = username.split('@')[0];
        loginSuccess = true;
        showToast(`Logged in successfully as ${username} (Mock Simulation)!`);
    }

    state.currentUser = {
        username,
        role: loginType,
        token,
        name: displayName || ""
    };

    sessionStorage.setItem("jwt_token", token);
    sessionStorage.setItem("username", username);
    sessionStorage.setItem("role", loginType);
    sessionStorage.setItem("name", displayName || "");

    // Load user-specific cart and wishlist from localStorage
    const cartKey = username !== "Guest" ? `ecom_cart_${username}` : "ecom_cart";
    const wishlistKey = username !== "Guest" ? `ecom_wishlist_${username}` : "ecom_wishlist";
    
    const savedCart = localStorage.getItem(cartKey);
    if (savedCart) {
        try { state.cart = JSON.parse(savedCart); } catch (e) { state.cart = []; }
    } else {
        state.cart = [];
    }
    const savedWishlist = localStorage.getItem(wishlistKey);
    if (savedWishlist) {
        try { state.wishlist = JSON.parse(savedWishlist); } catch (e) { state.wishlist = []; }
    } else {
        state.wishlist = [];
    }

    renderCart();
    updateWishlistUI();
    updateAuthUI();
    
    if (state.currentUser.role === "admin") {
        showView("admin");
    } else {
        showView("storefront");
    }
});

function updateAuthUI() {
    const container = document.getElementById("auth-status-container");
    const cartTrigger = document.getElementById("cart-drawer-trigger");
    const shopBtn = document.getElementById("nav-shop-btn");
    const userOrdersBtn = document.getElementById("nav-user-orders-btn");
    const adminBtn = document.getElementById("nav-admin-btn");
    const wishlistBtn = document.getElementById("nav-wishlist-btn");

    if (state.currentUser.username !== "Guest") {
        container.innerHTML = `
            <div class="profile-badge">
                <div class="profile-avatar">${state.currentUser.username[0].toUpperCase()}</div>
                <span class="nav-link" id="nav-logout-btn" style="font-size: 14px;"><i class="fa-solid fa-sign-out-alt"></i> Logout</span>
            </div>
        `;

        document.getElementById("nav-logout-btn").addEventListener("click", logout);

        if (state.currentUser.role === "admin") {
            adminBtn.classList.remove("d-none");
            shopBtn.classList.add("d-none");
            userOrdersBtn.classList.add("d-none");
            cartTrigger.classList.add("d-none");
            if (wishlistBtn) wishlistBtn.classList.add("d-none");
        } else {
            adminBtn.classList.add("d-none");
            shopBtn.classList.remove("d-none");
            userOrdersBtn.classList.remove("d-none");
            cartTrigger.classList.remove("d-none");
            if (wishlistBtn) wishlistBtn.classList.remove("d-none");
        }
    } else {
        container.innerHTML = `
            <button class="btn btn-secondary" id="nav-login-btn"><i class="fa-solid fa-sign-in-alt"></i> Login</button>
        `;
        document.getElementById("nav-login-btn").addEventListener("click", () => showView("login"));
        adminBtn.classList.add("d-none");
        shopBtn.classList.remove("d-none");
        userOrdersBtn.classList.add("d-none");
        cartTrigger.classList.remove("d-none");
        if (wishlistBtn) wishlistBtn.classList.remove("d-none");
    }
}

function logout() {
    state.currentUser = { username: "Guest", role: "user" };
    state.cart = [];
    sessionStorage.removeItem("jwt_token");
    sessionStorage.removeItem("username");
    sessionStorage.removeItem("role");
    renderCart();
    updateAuthUI();
    showToast("Logged out successfully.", "warning");
    showView("storefront");
}

// --- Settings Dialog & API Mode Removed for Production ---

// --- Modal Overlays Close ---
window.addEventListener("click", (e) => {
    if (e.target === views.productModal) views.productModal.classList.remove("active");
    if (e.target === views.checkoutModal) views.checkoutModal.classList.remove("active");
    if (views.settingsModal && e.target === views.settingsModal) views.settingsModal.classList.remove("active");
    if (e.target === views.productFormModal) views.productFormModal.classList.remove("active");
});

document.getElementById("close-detail-modal").addEventListener("click", () => {
    views.productModal.classList.remove("active");
});

document.getElementById("close-checkout-modal").addEventListener("click", () => {
    views.checkoutModal.classList.remove("active");
});

// --- Wishlist System ---
window.toggleWishlist = function(productId) {
    const index = state.wishlist.indexOf(productId);
    if (index === -1) {
        state.wishlist.push(productId);
        showToast("Added to Wishlist!", "success");
    } else {
        state.wishlist.splice(index, 1);
        showToast("Removed from Wishlist!", "warning");
    }
    updateWishlistUI();
    
    // Refresh current view if needed
    const wishlistView = document.getElementById("wishlist-view");
    if (wishlistView && !wishlistView.classList.contains("d-none")) {
        renderWishlist();
    } else {
        fetchAndRenderProducts();
    }
};

function updateWishlistUI() {
    // Persist wishlist state to localStorage per-user
    const wishlistKey = state.currentUser.username !== "Guest" ? `ecom_wishlist_${state.currentUser.username}` : "ecom_wishlist";
    localStorage.setItem(wishlistKey, JSON.stringify(state.wishlist));

    const badge = document.getElementById("wishlist-count-badge");
    const countLabel = document.getElementById("wishlist-count-label");
    
    if (badge) {
        if (state.wishlist.length > 0) {
            badge.textContent = state.wishlist.length;
            badge.style.display = "inline-block";
        } else {
            badge.style.display = "none";
        }
    }
    if (countLabel) {
        countLabel.textContent = `${state.wishlist.length} item${state.wishlist.length === 1 ? '' : 's'} favorited`;
    }
}

function renderWishlist() {
    const grid = document.getElementById("wishlist-grid");
    const emptyState = document.getElementById("wishlist-empty-state");
    grid.innerHTML = "";

    const wishlistItems = state.products.filter(p => state.wishlist.includes(p.product_id));

    if (wishlistItems.length === 0) {
        grid.style.display = "none";
        emptyState.style.display = "block";
    } else {
        grid.style.display = "grid";
        emptyState.style.display = "none";

        wishlistItems.forEach(p => {
            const card = document.createElement("div");
            card.className = "product-card";
            card.innerHTML = `
                <div class="product-img-container" style="position: relative;">
                    <img src="${p.image}" class="product-img" alt="${p.name}">
                    <button class="wishlist-btn" style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.5); border: none; width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 10;" onclick="event.stopPropagation(); toggleWishlist('${p.product_id}')">
                        <i class="fa-solid fa-heart" style="color: #ef4444; font-size: 16px;"></i>
                    </button>
                </div>
                <div class="product-info">
                    <span class="product-category">${p.category}</span>
                    <h3 class="product-name">${p.name}</h3>
                    <div class="product-footer" style="margin-top: 15px; display: flex; justify-content: space-between; align-items: center;">
                    <span class="product-price">₹${p.price.toFixed(2)}</span>
                        <button class="btn btn-primary" style="padding: 6px 12px; font-size: 12px; margin: 0; border-radius: 6px;" onclick="event.stopPropagation(); addToCartFromWishlist('${p.product_id}')">Add to Cart</button>
                    </div>
                </div>
            `;
            
            card.addEventListener("click", () => {
                openProductDetail(p.product_id);
            });
            
            grid.appendChild(card);
        });
    }
    updateWishlistUI();
}

window.addToCartFromWishlist = function(productId) {
    addToCart(productId);
    showToast("Added to Cart from Wishlist!", "success");
};

// --- General Event Listeners ---
document.getElementById("logo-link").addEventListener("click", (e) => {
    e.preventDefault();
    if (state.currentUser.role === "admin") {
        showView("admin");
    } else {
        showView("storefront");
    }
});

document.getElementById("nav-shop-btn").addEventListener("click", () => {
    showView("storefront");
});

document.getElementById("nav-wishlist-btn").addEventListener("click", () => {
    showView("wishlist");
});

document.getElementById("nav-user-orders-btn").addEventListener("click", () => {
    showView("userOrders");
});

document.getElementById("nav-admin-btn").addEventListener("click", () => {
    showView("admin");
});

document.getElementById("hero-explore-btn").addEventListener("click", () => {
    showView("storefront");
    const fashionTab = document.querySelector('.category-tab[data-category="Fashion"]');
    if (fashionTab) {
        fashionTab.click();
    }
});

// Category Click Handler
document.querySelectorAll(".category-tab").forEach(tab => {
    tab.addEventListener("click", () => {
        document.querySelectorAll(".category-tab").forEach(t => t.classList.remove("active"));
        tab.classList.add("active");
        state.selectedCategory = tab.dataset.category;
        fetchAndRenderProducts();
    });
});

// Search input
document.getElementById("product-search").addEventListener("input", () => {
    fetchAndRenderProducts();
});

// Cart Drawer open/close
document.getElementById("cart-drawer-trigger").addEventListener("click", () => {
    views.cartDrawer.classList.add("active");
});

document.getElementById("cart-close-btn").addEventListener("click", () => {
    views.cartDrawer.classList.remove("active");
});

document.getElementById("checkout-trigger-btn").addEventListener("click", () => {
    openCheckout();
});

// Theme Toggle Click Handler
document.getElementById("theme-toggle-btn").addEventListener("click", () => {
    document.body.classList.toggle("light-theme");
    const isLight = document.body.classList.contains("light-theme");
    localStorage.setItem("theme", isLight ? "light" : "dark");
    
    document.getElementById("theme-toggle-btn").innerHTML = isLight 
        ? '<i class="fa-solid fa-sun"></i>' 
        : '<i class="fa-solid fa-moon"></i>';
        
    showToast(`Switched to ${isLight ? "Day (Light)" : "Night (Dark)"} Mode`);
});

// Initialize Page
window.addEventListener("DOMContentLoaded", () => {
    // API mode and endpoints are locked to production live Gateway urls

    // Load persisted Cart and Wishlist (user-specific)
    const savedUsername = sessionStorage.getItem("username");
    const cartKey = savedUsername ? `ecom_cart_${savedUsername}` : "ecom_cart";
    const wishlistKey = savedUsername ? `ecom_wishlist_${savedUsername}` : "ecom_wishlist";
    const savedCart = localStorage.getItem(cartKey);
    if (savedCart) {
        try { state.cart = JSON.parse(savedCart); } catch (e) { state.cart = []; }
    }
    const savedWishlist = localStorage.getItem(wishlistKey);
    if (savedWishlist) {
        try { state.wishlist = JSON.parse(savedWishlist); } catch (e) { state.wishlist = []; }
    }
    updateWishlistUI();

    // Load theme preference
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "light") {
        document.body.classList.add("light-theme");
        document.getElementById("theme-toggle-btn").innerHTML = '<i class="fa-solid fa-sun"></i>';
    } else {
        document.body.classList.remove("light-theme");
        document.getElementById("theme-toggle-btn").innerHTML = '<i class="fa-solid fa-moon"></i>';
    }

    // Restore session from sessionStorage
    const savedToken = sessionStorage.getItem("jwt_token");
    const savedRole = sessionStorage.getItem("role");
    const savedName = sessionStorage.getItem("name");
    if (savedToken && savedUsername && savedRole) {
        state.currentUser = {
            username: savedUsername,
            role: savedRole,
            token: savedToken,
            name: savedName || ""
        };
    }

    updateAuthUI();
    fetchAndRenderProducts();
    renderCart();

    // Route view based on auth state at startup (always show storefront by default)
    showView("storefront");
    if (state.currentUser.role === "admin") {
        renderAdminDashboard();
    }
});

async function renderAdminUsers() {
    const tbody = document.getElementById("admin-users-rows");
    tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; padding: 25px; color: var(--text-secondary);">Loading authorized users registry...</td></tr>`;

    if (state.apiMode === "live") {
        try {
            const users = await apiCall("auth", "/auth/users");
            if (users && Array.isArray(users)) {
                if (users.length === 0) {
                    tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; padding: 25px; color: var(--text-secondary);">No registered users found.</td></tr>`;
                    return;
                }
                tbody.innerHTML = users.map(u => {
                    const expiry = u.code_expires_at ? new Date(u.code_expires_at * 1000).toLocaleString() : "N/A";
                    const statusClass = u.status === "VERIFIED" ? "badge badge-success" : "badge badge-warning";
                    return `
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.05); text-align: left;">
                            <td style="padding: 12px 10px;">${u.name || 'N/A'}</td>
                            <td style="padding: 12px 10px;">${u.email}</td>
                            <td style="padding: 12px 10px;"><span class="${statusClass}">${u.status}</span></td>
                            <td style="padding: 12px 10px; color: var(--text-muted);">${expiry}</td>
                        </tr>
                    `;
                }).join("");
            } else {
                tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; padding: 25px; color: var(--danger);">Failed to retrieve users.</td></tr>`;
            }
        } catch (e) {
            console.error("Failed to render admin users list:", e);
            tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; padding: 25px; color: var(--danger);">Auth Service unreachable.</td></tr>`;
        }
    } else {
        // Mock data
        tbody.innerHTML = `
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05); text-align: left;">
                <td style="padding: 12px 10px;">Jane Doe (Demo)</td>
                <td style="padding: 12px 10px;">jane@example.com</td>
                <td style="padding: 12px 10px;"><span class="badge badge-success">VERIFIED</span></td>
                <td style="padding: 12px 10px; color: var(--text-muted);">N/A</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05); text-align: left;">
                <td style="padding: 12px 10px;">madhumitha (Admin)</td>
                <td style="padding: 12px 10px;">madhumithamalu6@gmail.com</td>
                <td style="padding: 12px 10px;"><span class="badge badge-success">VERIFIED</span></td>
                <td style="padding: 12px 10px; color: var(--text-muted);">N/A</td>
            </tr>
        `;
    }
}
