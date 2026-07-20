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
    }
];

const DEFAULT_INVENTORY = {
    "prod-fashion-001": 25,
    "prod-fashion-002": 4,  // Low stock
    "prod-elec-001": 15,
    "prod-elec-002": 8,
    "prod-furn-001": 12,
    "prod-groc-001": 50,
    "prod-cosm-001": 3,   // Low stock
    "prod-uten-001": 18,
    "prod-shoes-001": 30
};

// --- App State ---
const state = {
    products: [...DEFAULT_PRODUCTS],
    inventory: { ...DEFAULT_INVENTORY },
    cart: [],
    orders: [],
    payments: [],
    currentUser: {
        username: "Guest",
        role: "user"
    },
    apiMode: "mock", // 'mock' or 'live'
    endpoints: {
        order: "http://localhost:8000",
        cart: "http://localhost:8001",
        inventory: "http://localhost:8002",
        payment: "http://localhost:8003",
        product: "http://localhost:8004"
    },
    selectedCategory: "all",
    selectedProductDetail: null,
    selectedCheckoutSize: null
};

// --- UI Selectors ---
const views = {
    storefront: document.getElementById("storefront-view"),
    userOrders: document.getElementById("user-orders-view"),
    login: document.getElementById("login-view"),
    admin: document.getElementById("admin-view"),
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
    if (state.currentUser.role === "admin" && (viewName === "storefront" || viewName === "userOrders")) {
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
            // Map live fields to state fields
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

        const card = document.createElement("div");
        card.className = "product-card";
        card.innerHTML = `
            <div class="product-img-container">
                <img src="${p.image}" class="product-img" alt="${p.name}">
            </div>
            <div class="product-info">
                <span class="product-category">${p.category}</span>
                <h3 class="product-name">${p.name}</h3>
                <div class="product-rating">
                    <span class="stars">${starsHtml}</span>
                    <span>(${p.rating_count})</span>
                </div>
                <div class="product-footer">
                    <span class="product-price">$${p.price.toFixed(2)}</span>
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
            <div class="detail-price">$${product.price.toFixed(2)}</div>
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
                <div class="cart-item-price">$${item.price.toFixed(2)}</div>
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
    document.getElementById("cart-total-value").innerText = `$${totalPrice.toFixed(2)}`;

    if (state.cart.length === 0) {
        container.innerHTML = `<div style="text-align: center; color: var(--text-muted); padding: 40px 0;"><i class="fa-solid fa-cart-shopping" style="font-size: 40px; margin-bottom: 12px; opacity: 0.3;"></i><p>Your cart is empty.</p></div>`;
    }
}

// --- Checkout & Payment Logic ---
function openCheckout() {
    if (state.cart.length === 0) {
        showToast("Your cart is empty!", "warning");
        return;
    }

    let totalPrice = 0;
    state.cart.forEach(i => totalPrice += i.price * i.quantity);

    document.getElementById("checkout-subtotal").innerText = `$${totalPrice.toFixed(2)}`;
    document.getElementById("checkout-total").innerText = `$${totalPrice.toFixed(2)}`;

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
    const finalAmount = state.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const orderId = "order-" + Math.floor(100000 + Math.random() * 900000);
    const activePayType = document.querySelector(".payment-tab.active").dataset.payType;

    showToast("Processing Payment via secure channel...", "warning");

    // Simulate Payment delay
    setTimeout(async () => {
        // Create Payment record
        const paymentRecord = {
            payment_id: "pay-" + Math.floor(100000 + Math.random() * 900000),
            order_id: orderId,
            amount: finalAmount,
            status: "SUCCESS",
            method: activePayType.toUpperCase(),
            timestamp: new Date().toISOString()
        };

        // Create Order records
        const newOrders = state.cart.map(item => ({
            order_id: orderId,
            user_id: state.currentUser.username,
            product_id: item.product_id,
            name: item.name,
            quantity: item.quantity,
            amount: item.price * item.quantity,
            size: item.size || "",
            status: "PENDING",
            timestamp: new Date().toISOString()
        }));

        if (state.apiMode === "live") {
            // Live microservices integration calls
            for (const order of newOrders) {
                // Call order-service POST /orders
                await apiCall("order", "/orders", "POST", {
                    user_id: order.user_id,
                    product_id: order.product_id,
                    quantity: order.quantity,
                    amount: order.amount,
                    size: order.size
                });

                // Decrement inventory stock on inventory-service
                await apiCall("inventory", `/inventory/${order.product_id}/decrement?quantity=${order.quantity}`, "POST");
            }

            // Call payment-service
            await apiCall("payment", "/payments", "POST", {
                order_id: orderId,
                amount: finalAmount
            });
        }

        // Always save locally in state for UI display
        state.payments.push(paymentRecord);
        state.orders.push(...newOrders);

        // Adjust local inventory stock
        state.cart.forEach(item => {
            if (state.inventory[item.product_id]) {
                state.inventory[item.product_id] = Math.max(0, state.inventory[item.product_id] - item.quantity);
            }
        });

        // Clear cart
        state.cart = [];
        renderCart();

        // Close Checkout
        views.checkoutModal.classList.remove("active");
        showToast(`Order Placed Successfully! Transaction ID: ${orderId}`, "success");
        
        // Refresh catalog to update stock badges if needed
        fetchAndRenderProducts();
    }, 1500);
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
        }
    });
});

function renderAdminDashboard() {
    // 1. Calculate Revenue from Payments logged as Success
    const totalRev = state.payments
        .filter(p => p.status === "SUCCESS")
        .reduce((sum, p) => sum + p.amount, 0);

    document.getElementById("stat-revenue").innerText = `$${totalRev.toFixed(2)}`;

    // 2. Count Total Orders
    // We group order rows by Order ID to count unique transactions
    const uniqueOrders = new Set(state.orders.map(o => o.order_id));
    document.getElementById("stat-orders").innerText = uniqueOrders.size;

    // 3. Count Low Stock alerts
    let lowStockAlerts = 0;
    Object.values(state.inventory).forEach(stock => {
        if (stock < 5) lowStockAlerts++;
    });
    document.getElementById("stat-low-stock").innerText = `${lowStockAlerts} Alert${lowStockAlerts !== 1 ? 's' : ''}`;

    // Recent transaction log
    const logBox = document.getElementById("dashboard-recent-log");
    if (state.payments.length > 0) {
        const lastPay = state.payments[state.payments.length - 1];
        logBox.innerHTML = `<strong>Recent Sale Success</strong>: order ID ${lastPay.order_id} generated <strong>$${lastPay.amount.toFixed(2)}</strong> via ${lastPay.method}!`;
    } else {
        logBox.innerText = "No payment transactions recorded yet.";
    }
}

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
            <td>$${p.price.toFixed(2)}</td>
            <td><strong style="font-size: 16px;">${stock}</strong> units</td>
            <td><span class="badge ${badgeClass}">${statusText}</span></td>
        `;

        tbody.appendChild(tr);
    });
}

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
            <td>${o.user_id}</td>
            <td>${o.name} ${o.size ? `(${o.size})` : ''}</td>
            <td>${o.quantity}</td>
            <td>$${o.amount.toFixed(2)}</td>
            <td><span class="badge badge-${o.status === 'DELIVERED' ? 'success' : o.status === 'CANCELLED' ? 'danger' : o.status === 'SHIPPED' ? 'accent' : 'warning'}">${o.status}</span></td>
            <td>${timeStr}</td>
            <td>${selectHtml}</td>
        `;

        tr.querySelector(".order-status-select").addEventListener("change", (e) => {
            const newStatus = e.target.value;
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
            <td>$${p.price.toFixed(2)}</td>
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
                state.products = state.products.filter(prod => prod.product_id !== p.product_id);
                delete state.inventory[p.product_id];

                if (state.apiMode === "live") {
                    await apiCall("product", `/products/${p.product_id}`, "DELETE");
                }

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
            p.name = name;
            p.category = category;
            p.price = price;
            p.description = description;
            p.image = image;

            if (state.apiMode === "live") {
                await apiCall("product", `/products/${productId}`, "PUT", {
                    name,
                    description,
                    price,
                    category,
                    image
                });
            }
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

        if (state.apiMode === "live") {
            await apiCall("product", "/products", "POST", {
                name,
                description,
                price,
                category,
                image
            });
            await apiCall("inventory", "/inventory", "POST", {
                product_id: newId,
                stock: 20
            });
        }

        state.products.push(newProduct);
        state.inventory[newId] = 20;
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
            <td style="font-weight: 700; color: var(--success);">$${p.amount.toFixed(2)}</td>
            <td><span class="badge badge-accent">${p.method}</span></td>
            <td><span class="badge badge-success">${p.status}</span></td>
            <td>${timeStr}</td>
        `;
        tbody.appendChild(tr);
    });
}

// --- Customer Order History ---
function renderUserOrders() {
    const container = document.getElementById("user-orders-container");
    container.innerHTML = "";

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
                    <div style="font-weight: 600;">$${item.amount.toFixed(2)}</div>
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
            <div class="user-order-price-qty">
                <span style="color: var(--text-secondary);">Total Paid:</span>
                <span class="user-order-total">$${totalAmount.toFixed(2)}</span>
            </div>
            ${timelineHtml}
        `;
        container.appendChild(card);
    });
}

// --- Auth System ---
const loginForm = document.getElementById("login-form");
let loginType = "user"; // 'user' or 'admin'

document.getElementById("tab-user-login").addEventListener("click", () => {
    document.getElementById("tab-user-login").classList.add("active", "btn-primary");
    document.getElementById("tab-user-login").style.borderColor = "var(--primary)";
    document.getElementById("tab-admin-login").classList.remove("active");
    document.getElementById("tab-admin-login").style.borderColor = "";
    document.getElementById("login-username").value = "user123";
    document.getElementById("register-prompt").classList.remove("d-none");
    loginType = "user";
});

document.getElementById("tab-admin-login").addEventListener("click", () => {
    document.getElementById("tab-admin-login").classList.add("active");
    document.getElementById("tab-admin-login").style.borderColor = "var(--primary)";
    document.getElementById("tab-user-login").classList.remove("active");
    document.getElementById("tab-user-login").style.borderColor = "";
    document.getElementById("login-username").value = "admin_master";
    document.getElementById("register-prompt").classList.add("d-none");
    loginType = "admin";
});

loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const username = document.getElementById("login-username").value;

    state.currentUser = {
        username,
        role: loginType
    };

    showToast(`Logged in successfully as ${username}!`);
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
        } else {
            adminBtn.classList.add("d-none");
            shopBtn.classList.remove("d-none");
            userOrdersBtn.classList.remove("d-none");
            cartTrigger.classList.remove("d-none");
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
    }
}

function logout() {
    state.currentUser = { username: "Guest", role: "user" };
    state.cart = [];
    renderCart();
    updateAuthUI();
    showToast("Logged out successfully.", "warning");
    showView("storefront");
}

// --- Settings Dialog & API Mode ---
const settingsTrigger = document.getElementById("api-settings-trigger");
const closeSettings = document.getElementById("close-settings-modal");
const saveSettings = document.getElementById("save-settings-btn");

settingsTrigger.addEventListener("click", () => {
    document.getElementById("btn-mode-mock").classList.remove("active");
    document.getElementById("btn-mode-live").classList.remove("active");
    
    if (state.apiMode === "mock") {
        document.getElementById("btn-mode-mock").classList.add("active");
    } else {
        document.getElementById("btn-mode-live").classList.add("active");
    }

    views.settingsModal.classList.add("active");
});

closeSettings.addEventListener("click", () => {
    views.settingsModal.classList.remove("active");
});

document.getElementById("btn-mode-mock").addEventListener("click", () => {
    document.getElementById("btn-mode-mock").classList.add("active");
    document.getElementById("btn-mode-live").classList.remove("active");
    document.getElementById("live-endpoints-container").classList.add("d-none");
});

document.getElementById("btn-mode-live").addEventListener("click", () => {
    document.getElementById("btn-mode-live").classList.add("active");
    document.getElementById("btn-mode-mock").classList.remove("active");
    document.getElementById("live-endpoints-container").classList.remove("d-none");
});

saveSettings.addEventListener("click", () => {
    const isMock = document.getElementById("btn-mode-mock").classList.contains("active");
    state.apiMode = isMock ? "mock" : "live";

    if (!isMock) {
        state.endpoints.order = document.getElementById("api-order-url").value;
        state.endpoints.cart = document.getElementById("api-cart-url").value;
        state.endpoints.inventory = document.getElementById("api-inventory-url").value;
        state.endpoints.payment = document.getElementById("api-payment-url").value;
        state.endpoints.product = document.getElementById("api-product-url").value;
    }

    const badge = document.getElementById("status-mode-badge");
    badge.innerText = state.apiMode === "mock" ? "Simulated / Mock Mode" : "Live API Gateway";
    badge.className = `badge badge-${state.apiMode === 'mock' ? 'success' : 'accent'}`;

    views.settingsModal.classList.remove("active");
    showToast(`Switched gateway to ${state.apiMode.toUpperCase()} mode!`);
    
    // Refresh products catalog
    fetchAndRenderProducts();
});

// --- Modal Overlays Close ---
window.addEventListener("click", (e) => {
    if (e.target === views.productModal) views.productModal.classList.remove("active");
    if (e.target === views.checkoutModal) views.checkoutModal.classList.remove("active");
    if (e.target === views.settingsModal) views.settingsModal.classList.remove("active");
    if (e.target === views.productFormModal) views.productFormModal.classList.remove("active");
});

document.getElementById("close-detail-modal").addEventListener("click", () => {
    views.productModal.classList.remove("active");
});

document.getElementById("close-checkout-modal").addEventListener("click", () => {
    views.checkoutModal.classList.remove("active");
});

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

document.getElementById("nav-user-orders-btn").addEventListener("click", () => {
    showView("userOrders");
});

document.getElementById("nav-admin-btn").addEventListener("click", () => {
    showView("admin");
});

document.getElementById("hero-explore-btn").addEventListener("click", () => {
    document.querySelector('.category-tab[data-category="Fashion"]').click();
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
    // Load theme preference
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "light") {
        document.body.classList.add("light-theme");
        document.getElementById("theme-toggle-btn").innerHTML = '<i class="fa-solid fa-sun"></i>';
    } else {
        document.body.classList.remove("light-theme");
        document.getElementById("theme-toggle-btn").innerHTML = '<i class="fa-solid fa-moon"></i>';
    }

    updateAuthUI();
    fetchAndRenderProducts();
    renderCart();
});
