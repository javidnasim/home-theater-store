import os
import sys
from datetime import datetime, timedelta
import streamlit as st
from PIL import Image

# Ensure local modules can be imported
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

from database.database import (
    init_db,
    get_available_products,
    get_all_products,
    get_product_by_id,
    add_product,
    update_product,
    mark_product_as_sold,
    mark_product_as_available,
    delete_product,
    get_dashboard_stats,
    cleanup_expired_sold_products,
    register_customer,
    authenticate_customer,
    add_installation_request,
    get_installation_requests,
    update_installation_status
)

from utils.helpers import (
    WHATSAPP_NUMBER,
    BUSINESS_NAME,
    BUSINESS_SHORT_NAME,
    BUSINESS_TAGLINE,
    STORE_CITY,
    STORE_ADDRESS,
    STORE_PHONE_DISPLAY,
    STORE_HOURS,
    format_inr,
    get_whatsapp_link,
    get_installation_whatsapp_link,
    save_uploaded_image,
    get_image_path,
    create_starter_assets,
    verify_admin_password,
    hash_password
)

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title=f"{BUSINESS_NAME} - Home Theaters & Audio",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="expanded"
)

IMAGES_DIR = os.path.join(CURRENT_DIR, "images")

# Initialize database and sample assets on startup
init_db()
create_starter_assets(IMAGES_DIR)

# -----------------------------------------------------------------------------
# COLORFUL & VIBRANT CUSTOM STYLING (HTML & CSS)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 3.5rem;
        max-width: 1240px;
    }

    /* Vibrant Colorful Hero Container */
    .hero-container {
        background: linear-gradient(135deg, #312e81 0%, #4338ca 35%, #065f46 100%);
        border: 2px solid rgba(255, 255, 255, 0.18);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        color: #ffffff;
        box-shadow: 0 15px 35px -5px rgba(49, 46, 129, 0.45);
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .hero-badge {
        display: inline-block;
        background: linear-gradient(90deg, #f59e0b 0%, #ec4899 100%);
        color: #ffffff;
        padding: 0.35rem 1.1rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 0.9rem;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        box-shadow: 0 4px 12px rgba(236, 72, 153, 0.35);
    }

    .hero-title {
        font-size: 2.7rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0.2rem 0 0.5rem 0;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: #e0e7ff;
        max-width: 720px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.5;
        font-weight: 500;
    }

    .hero-trust-row {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.85rem;
        margin-top: 1.2rem;
    }

    .trust-pill-cyan {
        background: rgba(6, 182, 212, 0.22);
        border: 1px solid #06b6d4;
        padding: 0.45rem 0.95rem;
        border-radius: 10px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #cffafe;
    }

    .trust-pill-emerald {
        background: rgba(16, 185, 129, 0.22);
        border: 1px solid #10b981;
        padding: 0.45rem 0.95rem;
        border-radius: 10px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #d1fae5;
    }

    .trust-pill-purple {
        background: rgba(168, 85, 247, 0.25);
        border: 1px solid #a855f7;
        padding: 0.45rem 0.95rem;
        border-radius: 10px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #f3e8ff;
    }

    .trust-pill-amber {
        background: rgba(245, 158, 11, 0.25);
        border: 1px solid #f59e0b;
        padding: 0.45rem 0.95rem;
        border-radius: 10px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #fef3c7;
    }

    /* Colorful Category Cards */
    .cat-card-1 {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 2px solid #93c5fd;
        border-radius: 14px;
        padding: 1.3rem;
        text-align: center;
        transition: transform 0.2s ease;
    }
    .cat-card-2 {
        background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
        border: 2px solid #c4b5fd;
        border-radius: 14px;
        padding: 1.3rem;
        text-align: center;
        transition: transform 0.2s ease;
    }
    .cat-card-3 {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 2px solid #fca5a5;
        border-radius: 14px;
        padding: 1.3rem;
        text-align: center;
        transition: transform 0.2s ease;
    }
    .cat-card-4 {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border: 2px solid #6ee7b7;
        border-radius: 14px;
        padding: 1.3rem;
        text-align: center;
        transition: transform 0.2s ease;
    }

    /* Product Card Styling */
    .product-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1e1b4b;
        margin: 0.6rem 0 0.25rem 0;
        line-height: 1.35;
        min-height: 3.2rem;
    }

    .price-tag {
        font-size: 1.55rem;
        font-weight: 800;
        color: #047857;
        margin: 0.3rem 0 0.5rem 0;
    }

    .stock-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background: linear-gradient(90deg, #ecfdf5 0%, #d1fae5 100%);
        color: #065f46;
        border: 1px solid #10b981;
        padding: 0.3rem 0.75rem;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-bottom: 0.7rem;
    }

    .product-desc {
        color: #4b5563;
        font-size: 0.9rem;
        line-height: 1.45;
        margin-bottom: 0.8rem;
    }

    /* Colorful Metric Cards */
    .metric-card-purple {
        background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
        border: 2px solid #c084fc;
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
    }
    .metric-card-green {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 2px solid #4ade80;
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
    }
    .metric-card-blue {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 2px solid #38bdf8;
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
    }
    .metric-card-amber {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 2px solid #facc15;
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0.2rem 0;
    }

    .metric-label {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }

    /* Service card */
    .service-box {
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        color: #1e293b;
    }

    .store-footer {
        border-top: 2px solid #e2e8f0;
        margin-top: 4rem;
        padding-top: 2.5rem;
        text-align: center;
        color: #64748b;
        font-size: 0.9rem;
    }

    @media (max-width: 640px) {
        .hero-title { font-size: 1.8rem; }
        .hero-container { padding: 1.5rem 1rem; }
        .product-title { min-height: auto; }
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

if "customer_user" not in st.session_state:
    st.session_state["customer_user"] = None

if "edit_product_id" not in st.session_state:
    st.session_state["edit_product_id"] = None

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION MENU (Ensures visibility at all times)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"## {BUSINESS_NAME}")
    st.markdown("Main Navigation")
    nav_page = st.radio(
        "Go to:",
        ["Home", "Products", "Installation Support", "About", "Admin Portal"],
        label_visibility="collapsed"
    )
# =============================================================================
# SECTION: HOME
# =============================================================================
if nav_page == "Home":
    st.markdown(f"""
    <div class="hero-container">
        <div class="hero-badge">Certified Pre-Owned Audio Center</div>
        <div class="hero-title">{BUSINESS_NAME}</div>
        <div class="hero-subtitle">{BUSINESS_TAGLINE} - Bringing authentic cinema sound and expert acoustic installation to your home.</div>
        <div class="hero-trust-row">
            <span class="trust-pill-cyan">10-Point Bench Check</span>
            <span class="trust-pill-emerald">7-Day Testing Warranty</span>
            <span class="trust-pill-purple">On-Site Installation Support</span>
            <span class="trust-pill-amber">Direct Contact: {STORE_PHONE_DISPLAY}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Colorful Category Highlights
    st.markdown("### Explore Audio Categories")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="cat-card-1">
            <div style="font-size: 2.2rem; margin-bottom: 0.3rem;">🔊</div>
            <div style="font-weight: 800; font-size: 1.05rem; color: #1e40af;">AV Receivers</div>
            <small style="color: #3b82f6;">Denon | Yamaha | Marantz 4K/8K</small>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="cat-card-2">
            <div style="font-size: 2.2rem; margin-bottom: 0.3rem;">🎼</div>
            <div style="font-weight: 800; font-size: 1.05rem; color: #5b21b6;">5.1 & 7.1 Systems</div>
            <small style="color: #7c3aed;">Polk Audio | Klipsch | JBL Cinema</small>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="cat-card-3">
            <div style="font-size: 2.2rem; margin-bottom: 0.3rem;">🎸</div>
            <div style="font-weight: 800; font-size: 1.05rem; color: #991b1b;">Powered Subwoofers</div>
            <small style="color: #dc2626;">High SPL 10" & 12" Deep Bass</small>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="cat-card-4">
            <div style="font-size: 2.2rem; margin-bottom: 0.3rem;">📺</div>
            <div style="font-weight: 800; font-size: 1.05rem; color: #065f46;">Smart Soundbars</div>
            <small style="color: #059669;">Dolby Atmos with Wireless Sub</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

    # Featured Systems Spotlight
    st.markdown("### Available Systems Spotlight")
    featured_prods = get_available_products()[:3]
    if featured_prods:
        fcols = st.columns(3)
        for idx, fprod in enumerate(featured_prods):
            with fcols[idx]:
                thumb = get_image_path(fprod.get("image"), IMAGES_DIR)
                if thumb and os.path.exists(thumb):
                    st.image(thumb)
                st.markdown(f"**{fprod['product_name']}**")
                st.markdown(f"<span style='color: #047857; font-weight: 800; font-size: 1.3rem;'>{format_inr(fprod['price'])}</span>", unsafe_allow_html=True)
                st.caption(fprod.get("description", "")[:100] + "...")
                st.link_button(
                    f"WhatsApp Enquiry ({format_inr(fprod['price'])})",
                    get_whatsapp_link(fprod["product_name"], fprod["price"]),
                    type="primary"
                )
    
    st.markdown("---")
    cta1, cta2 = st.columns([3, 1])
    with cta1:
        st.markdown(f"""### Need a Custom Home Theater Solution?
Speak directly to our senior audio specialist at **{BUSINESS_NAME}**. We help you pick the exact receiver, matching speakers, and provide end-to-end installation.""")
    with cta2:
        st.link_button("Chat on WhatsApp", get_whatsapp_link(), type="primary")

# =============================================================================
# SECTION: PRODUCTS
# =============================================================================
elif nav_page == "Products":
    st.markdown(f"## Available Audio Inventory")
    st.markdown("Every unit has been thoroughly tested, inspected, and is ready for sound testing or immediate purchase.")

    col_search, col_sort = st.columns([3, 1])
    with col_search:
        search_query = st.text_input(
            "Search inventory",
            placeholder="Search by model, brand (Denon, Yamaha, Polk), Dolby Atmos, 4K, 5.1...",
            label_visibility="collapsed"
        )
    with col_sort:
        sort_choice = st.selectbox(
            "Sort by",
            ["Newest First", "Price: Low to High", "Price: High to Low"],
            label_visibility="collapsed"
        )

    products = get_available_products(search_query=search_query)

    if sort_choice == "Price: Low to High":
        products.sort(key=lambda x: x["price"])
    elif sort_choice == "Price: High to Low":
        products.sort(key=lambda x: x["price"], reverse=True)
    else:
        products.sort(key=lambda x: x["id"], reverse=True)

    st.markdown(f"<p style='color: #4338ca; font-size: 0.95rem; font-weight: 600; margin: 0.5rem 0 1.2rem 0;'>Showing <b>{len(products)}</b> verified available system{'s' if len(products) != 1 else ''}</p>", unsafe_allow_html=True)

    if not products:
        st.info("No matching home theater systems found. Check back soon or contact us directly on WhatsApp!")
        st.link_button("Chat with Shah Digital Store", get_whatsapp_link())
    else:
        COLS_COUNT = 3
        for i in range(0, len(products), COLS_COUNT):
            row_products = products[i:i + COLS_COUNT]
            cols = st.columns(COLS_COUNT)

            for col_idx, prod in enumerate(row_products):
                with cols[col_idx]:
                    img_path = get_image_path(prod.get("image"), IMAGES_DIR)
                    if img_path and os.path.exists(img_path):
                        try:
                            st.image(img_path)
                        except Exception:
                            st.image(get_image_path("default_theater.jpg", IMAGES_DIR))
                    else:
                        st.image(get_image_path("default_theater.jpg", IMAGES_DIR))

                    st.markdown(f"<div class='product-title'>{prod['product_name']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='price-tag'>{format_inr(prod['price'])}</div>", unsafe_allow_html=True)
                    st.markdown("<div class='stock-badge'>In Stock & Ready for Demo</div>", unsafe_allow_html=True)

                    if prod.get("description"):
                        st.markdown(f"<div class='product-desc'>{prod['description']}</div>", unsafe_allow_html=True)

                    if prod.get("specifications"):
                        with st.expander("Technical Specifications", expanded=False):
                            specs_lines = prod["specifications"].split("\n")
                            for line in specs_lines:
                                if line.strip():
                                    st.markdown(f"<small>{line.strip()}</small>", unsafe_allow_html=True)

                    wa_url = get_whatsapp_link(product_name=prod["product_name"], price=prod["price"])
                    st.link_button(
                        f"Enquire on WhatsApp ({format_inr(prod['price'])})",
                        wa_url,
                        type="primary"
                    )
                    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

# =============================================================================
# SECTION: INSTALLATION SUPPORT
# =============================================================================
elif nav_page == "Installation Support":
    st.markdown(f"## Professional Home Theater Installation & Calibration")
    st.markdown(f"**{BUSINESS_NAME}** doesn't just sell equipment - our certified audio technicians provide complete on-site installation, precision speaker mounting, and acoustic tuning.")

    s1, s2 = st.columns(2)
    with s1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border: 2px solid #3b82f6; border-radius: 14px; padding: 1.3rem; margin-bottom: 1rem;">
            <h4 style="color: #1e40af; margin-top: 0;">1. Speaker Wall-Mounting & Placement</h4>
            <p style="color: #1e293b; font-size: 0.9rem;">Proper ear-level positioning for front left, center, right, and Dolby Atmos height elevation speakers to create an authentic 360-degree sound dome.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%); border: 2px solid #a855f7; border-radius: 14px; padding: 1.3rem; margin-bottom: 1rem;">
            <h4 style="color: #6b21a8; margin-top: 0;">2. Concealed In-Wall Acoustic Wiring</h4>
            <p style="color: #1e293b; font-size: 0.9rem;">Oxygen-Free Copper (OFC) speaker cables routed cleanly through conduits or molding for a pristine, zero-wire living room look.</p>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 2px solid #10b981; border-radius: 14px; padding: 1.3rem; margin-bottom: 1rem;">
            <h4 style="color: #065f46; margin-top: 0;">3. AVR Acoustic Calibration</h4>
            <p style="color: #1e293b; font-size: 0.9rem;">Precision microphone calibration (Audyssey MultEQ / Yamaha YPAO) to eliminate room echo, set exact speaker distances, and level crossover frequencies.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border: 2px solid #f59e0b; border-radius: 14px; padding: 1.3rem; margin-bottom: 1rem;">
            <h4 style="color: #92400e; margin-top: 0;">4. Projector & Screen Alignment</h4>
            <p style="color: #1e293b; font-size: 0.9rem;">Laser level mounting for 4K projectors, motorized/fixed-frame screens, and eARC/HDMI 2.1 cable handshake optimization.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Book an Installation / Technician Visit")
    with st.form("installation_booking_form", clear_on_submit=True):
        fcol1, fcol2 = st.columns(2)
        with fcol1:
            req_name = st.text_input("Your Full Name *", placeholder="e.g. Ramesh Shah")
            req_phone = st.text_input("Phone Number (10 Digits) *", placeholder="e.g. 9600173174")
            req_setup = st.selectbox(
                "Setup Type Needed *",
                ["5.1 Surround Speaker Installation", "7.1 / 7.2 Dolby Atmos Setup", "Soundbar & Subwoofer Setup", "AV Receiver Tuning & Calibration", "Full Home Cinema & Projector Installation"]
            )
        with fcol2:
            req_room = st.text_input("Room Dimensions / Type", placeholder="e.g. 16 x 14 ft Living Room")
            req_address = st.text_area("Your Address / Locality *", placeholder="Enter your address for technician visit...")

        btn_submit_install = st.form_submit_button("Submit Installation Request", type="primary")

        if btn_submit_install:
            if not req_name.strip() or not req_phone.strip() or not req_address.strip():
                st.error("Please fill in your name, phone number, and address.")
            else:
                req_id = add_installation_request(
                    customer_name=req_name,
                    phone=req_phone,
                    setup_type=req_setup,
                    room_size=req_room,
                    address=req_address
                )
                st.success(f"Installation request #{req_id} registered successfully! Our technician will call you shortly.")
                # Also provide instant WhatsApp button
                wa_install_url = get_installation_whatsapp_link(req_name, req_phone, req_setup, req_room)
                st.link_button("Confirm Request on WhatsApp Instantly", wa_install_url, type="primary")

# =============================================================================
# SECTION: ABOUT
# =============================================================================
elif nav_page == "About":
    st.markdown(f"## About {BUSINESS_NAME}")
    st.markdown(f"""
    Welcome to **{BUSINESS_NAME}**, your premier destination for certified pre-owned home theater systems, AV receivers, and high-fidelity surround sound equipment.
    
    Founded with a passion for true audio fidelity, our mission is to make high-end cinema sound accessible without paying exorbitant retail brand-new markups. Every single component in our inventory undergoes extensive bench testing, channel balance checks, and acoustic sweeps.
    """)

    st.markdown("### Why Choose Shah Digital Store?")
    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown("""
        <div style="border: 2px solid #38bdf8; border-radius: 12px; padding: 1.2rem; background: #f0f9ff;">
            <h4 style="color: #0369a1;">100% Genuine Components</h4>
            <p style="font-size: 0.9rem; color: #334155;">We do not sell duplicate or altered units. All boards, capacitors, and speaker voice coils are inspected for factory performance.</p>
        </div>
        """, unsafe_allow_html=True)
    with a2:
        st.markdown("""
        <div style="border: 2px solid #34d399; border-radius: 12px; padding: 1.2rem; background: #ecfdf5;">
            <h4 style="color: #047857;">7-Day Testing Warranty</h4>
            <p style="font-size: 0.9rem; color: #334155;">Test the equipment comfortably in your own home with your own movies and music. If any defect is found, we service or replace it.</p>
        </div>
        """, unsafe_allow_html=True)
    with a3:
        st.markdown("""
        <div style="border: 2px solid #c084fc; border-radius: 12px; padding: 1.2rem; background: #faf5ff;">
            <h4 style="color: #7e22ce;">Complete Installation</h4>
            <p style="font-size: 0.9rem; color: #334155;">From speaker placement to AVR frequency calibration, our technicians ensure you get pristine theater audio.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Store & Contact Information")
    c_info1, c_info2 = st.columns([2, 1])
    with c_info1:
        st.markdown(f"""
        - **Business Name**: {BUSINESS_NAME}  
        - **Phone & WhatsApp**: **{STORE_PHONE_DISPLAY}**  
        - **Operating Hours**: {STORE_HOURS}  
        - **Address**: {STORE_ADDRESS}  
        """)
    with c_info2:
        st.link_button("Chat on WhatsApp", get_whatsapp_link(), type="primary")
        st.link_button(f"Call {STORE_PHONE_DISPLAY}", f"tel:{WHATSAPP_NUMBER}")

# =============================================================================
# SECTION: ADMIN PORTAL
# =============================================================================
elif nav_page == "Admin Portal":
    if not st.session_state["admin_logged_in"]:
        st.markdown("### Store Management & Admin Portal")
        st.markdown("This section is reserved exclusively for **Shah Digital Store Administrators**.")

        with st.form("admin_login_form"):
            admin_pwd = st.text_input("Enter Admin Master Password", type="password", placeholder="••••••••")
            submit_login = st.form_submit_button("Log In to Admin Dashboard", type="primary")

            if submit_login:
                if verify_admin_password(admin_pwd):
                    st.session_state["admin_logged_in"] = True
                    st.success("Admin authentication successful!")
                    st.rerun()
                else:
                    st.error("Incorrect administrator password. Default password is 'admin123'.")
    else:
        admin_h1, admin_h2 = st.columns([3, 1])
        with admin_h1:
            st.markdown(f"## {BUSINESS_NAME} Admin Suite")
        with admin_h2:
            if st.button("Admin Log Out", type="secondary"):
                st.session_state["admin_logged_in"] = False
                st.rerun()

        cleaned_up = cleanup_expired_sold_products()
        stats = get_dashboard_stats()

        if cleaned_up > 0:
            st.toast(f"Cleaned up {cleaned_up} sold product(s) older than 2 days.")

        # Colorful Admin Metric Cards
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="metric-card-green">
                <div class="metric-label" style="color: #15803d;">Available Stock</div>
                <div class="metric-value" style="color: #166534;">{stats['available_count']}</div>
                <small style="color: #15803d;">Live on customer website</small>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-card-amber">
                <div class="metric-label" style="color: #b45309;">Recently Sold</div>
                <div class="metric-value" style="color: #92400e;">{stats['sold_count']}</div>
                <small style="color: #b45309;">Retained for 2 days</small>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-card-purple">
                <div class="metric-label" style="color: #7e22ce;">Registered Customers</div>
                <div class="metric-value" style="color: #6b21a8;">{stats['customer_count']}</div>
                <small style="color: #7e22ce;">Customer accounts</small>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class="metric-card-blue">
                <div class="metric-label" style="color: #0369a1;">Pending Installations</div>
                <div class="metric-value" style="color: #075985;">{stats['pending_installations']}</div>
                <small style="color: #0369a1;">Technician requests</small>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        admin_subtabs = st.tabs([
            "Add New Product",
            "Manage Available Products",
            "Sold Items (2-Day Retention)",
            "Installation Requests",
            "Security & Settings"
        ])

        # 1. Add Product
        with admin_subtabs[0]:
            st.markdown("### Add a New Refurbished System")
            with st.form("add_product_form", clear_on_submit=True):
                p_name = st.text_input("Product Name / Model *", placeholder="e.g. Denon AVR-X250BT 5.2 4K Receiver")
                p_price = st.number_input("Selling Price (INR) *", min_value=500.0, step=500.0, value=25000.0)
                p_desc = st.text_area("Customer Description", placeholder="Highlight service history, cosmetic grade, and standout audio features...")
                p_specs = st.text_area(
                    "Specifications (One line per bullet)",
                    value="""Channels:
Power:
HDMI:
Audio Decoding:
Condition: 9/10 Refurbished
Inclusions: Remote, Power Cable
Warranty: 7-Day Testing Warranty by Shah Digital Store""",
                    height=150
                )
                p_image = st.file_uploader("Upload Product Photo (JPG, PNG, WEBP)", type=["jpg", "jpeg", "png", "webp"])

                btn_add = st.form_submit_button("Add Product to Catalog", type="primary")

                if btn_add:
                    if not p_name.strip():
                        st.error("Please provide a product name.")
                    else:
                        saved_img_name = None
                        if p_image is not None:
                            saved_img_name = save_uploaded_image(p_image, IMAGES_DIR)
                        else:
                            saved_img_name = "default_theater.jpg"

                        new_id = add_product(
                            product_name=p_name.strip(),
                            description=p_desc.strip(),
                            price=float(p_price),
                            image=saved_img_name,
                            specifications=p_specs.strip()
                        )
                        st.success(f"Product '{p_name}' successfully added with ID #{new_id}!")
                        st.rerun()

        # 2. Manage Products
        with admin_subtabs[1]:
            st.markdown("### Manage Available Systems")
            available_items = get_all_products(status_filter="available")

            if not available_items:
                st.info("No active available products in inventory.")
            else:
                for item in available_items:
                    with st.container():
                        card_col1, card_col2, card_col3 = st.columns([1, 3, 2])

                        with card_col1:
                            thumb_path = get_image_path(item.get("image"), IMAGES_DIR)
                            if thumb_path and os.path.exists(thumb_path):
                                st.image(thumb_path)

                        with card_col2:
                            st.markdown(f"**#{item['id']} - {item['product_name']}**")
                            st.markdown(f"<span style='color: #047857; font-weight: 800; font-size: 1.15rem;'>{format_inr(item['price'])}</span>", unsafe_allow_html=True)
                            st.caption(f"Added: {item['created_at'][:10]} | Status: **Available**")
                            if item.get("description"):
                                st.caption(item["description"][:120] + ("..." if len(item["description"]) > 120 else ""))

                        with card_col3:
                            bcol1, bcol2 = st.columns(2)
                            with bcol1:
                                if st.button(f"Edit", key=f"edit_btn_{item['id']}"):
                                    st.session_state["edit_product_id"] = item["id"]
                                    st.rerun()

                            with bcol2:
                                if st.button(f"Mark SOLD", key=f"sold_btn_{item['id']}", type="primary"):
                                    mark_product_as_sold(item["id"])
                                    st.toast(f"Marked #{item['id']} as SOLD. Hidden from public and auto-deletes in 2 days.")
                                    st.rerun()

                            if st.button(f"Delete", key=f"del_btn_{item['id']}"):
                                delete_product(item["id"])
                                st.toast(f"Product #{item['id']} permanently deleted.")
                                st.rerun()

                        if st.session_state.get("edit_product_id") == item["id"]:
                            st.markdown(f"#### Editing Product #{item['id']}")
                            with st.form(f"edit_form_{item['id']}"):
                                e_name = st.text_input("Product Name", value=item["product_name"])
                                e_price = st.number_input("Selling Price (INR)", min_value=100.0, step=500.0, value=float(item["price"]))
                                e_desc = st.text_area("Description", value=item.get("description", ""))
                                e_specs = st.text_area("Specifications", value=item.get("specifications", ""), height=130)
                                e_new_img = st.file_uploader("Replace Image (Optional)", type=["jpg", "jpeg", "png", "webp"], key=f"file_edit_{item['id']}")

                                e_save_col, e_cancel_col = st.columns(2)
                                with e_save_col:
                                    save_btn = st.form_submit_button("Save Changes", type="primary")
                                with e_cancel_col:
                                    cancel_btn = st.form_submit_button("Cancel")

                                if save_btn:
                                    new_image_file = None
                                    if e_new_img is not None:
                                        new_image_file = save_uploaded_image(e_new_img, IMAGES_DIR)

                                    update_product(
                                        product_id=item["id"],
                                        product_name=e_name.strip(),
                                        description=e_desc.strip(),
                                        price=float(e_price),
                                        specifications=e_specs.strip(),
                                        image=new_image_file
                                    )
                                    st.session_state["edit_product_id"] = None
                                    st.success("Product updated successfully!")
                                    st.rerun()

                                if cancel_btn:
                                    st.session_state["edit_product_id"] = None
                                    st.rerun()

                        st.markdown("<hr style='margin: 0.8rem 0; opacity: 0.3;'/>", unsafe_allow_html=True)

        # 3. Sold Products (2-Day Retention)
        with admin_subtabs[2]:
            st.markdown("### Sold Products (2-Day Retention Window)")
            st.markdown("> **Rule**: When marked as **SOLD**, products are **immediately hidden from customers**. They remain here for **2 days (48 hours)**, after which they are **automatically deleted** from the database.")

            sold_items = get_all_products(status_filter="sold")
            if not sold_items:
                st.info("No recently sold products within the 2-day grace period.")
            else:
                for s_item in sold_items:
                    with st.container():
                        scol1, scol2, scol3 = st.columns([1, 3, 2])
                        with scol1:
                            thumb_path = get_image_path(s_item.get("image"), IMAGES_DIR)
                            if thumb_path and os.path.exists(thumb_path):
                                st.image(thumb_path)

                        with scol2:
                            st.markdown(f"**#{s_item['id']} - {s_item['product_name']}**")
                            st.markdown(f"<span style='color: #b45309; font-weight: 700;'>Sold for: {format_inr(s_item['price'])}</span>", unsafe_allow_html=True)

                            sold_at_str = s_item.get("sold_at")
                            if sold_at_str:
                                try:
                                    sold_dt = datetime.fromisoformat(sold_at_str)
                                    time_since_sold = datetime.now() - sold_dt
                                    hours_since = int(time_since_sold.total_seconds() // 3600)
                                    hours_left = max(0, 48 - hours_since)
                                    st.caption(f"Sold on: {sold_dt.strftime('%d %b %Y, %I:%M %p')}")
                                    st.markdown(f"**Retention**: Sold {hours_since}h ago | **Auto-deletion in {hours_left}h**")
                                except Exception:
                                    st.caption(f"Sold at: {sold_at_str}")

                        with scol3:
                            if st.button(f"Revert to Available", key=f"revert_btn_{s_item['id']}"):
                                mark_product_as_available(s_item["id"])
                                st.toast(f"Reverted #{s_item['id']} back to Available!")
                                st.rerun()

                            if st.button(f"Delete Immediately", key=f"del_sold_btn_{s_item['id']}"):
                                delete_product(s_item["id"])
                                st.toast(f"Product #{s_item['id']} deleted.")
                                st.rerun()

                        st.markdown("<hr style='margin: 0.8rem 0; opacity: 0.3;'/>", unsafe_allow_html=True)

        # 4. Installation Requests
        with admin_subtabs[3]:
            st.markdown("### Customer Installation Requests")
            requests_list = get_installation_requests()

            if not requests_list:
                st.info("No installation requests received yet.")
            else:
                for req in requests_list:
                    with st.container():
                        r1, r2 = st.columns([3, 1])
                        with r1:
                            status_badge = "Pending" if req["status"] == "pending" else "Completed"
                            st.markdown(f"**Request #{req['id']} - {req['customer_name']}** ({status_badge})")
                            st.markdown(f"**Phone**: `{req['phone']}`  |  **Setup**: {req['setup_type']}")
                            st.markdown(f"**Room**: {req['room_size'] or 'Standard'}  |  **Address**: {req['address']}")
                            st.caption(f"Date: {req['created_at'][:10]}")
                        with r2:
                            wa_call_link = f"https://wa.me/91{req['phone']}?text=Hello%20{req['customer_name']}!%20This%20is%20Shah%20Digital%20Store%20regarding%20your%20installation%20request."
                            st.link_button("WhatsApp Customer", wa_call_link)
                            if req["status"] == "pending":
                                if st.button("Mark Completed", key=f"comp_{req['id']}"):
                                    update_installation_status(req["id"], "completed")
                                    st.rerun()

                        st.markdown("<hr style='margin: 0.6rem 0; opacity: 0.3;'/>", unsafe_allow_html=True)

        # 5. Security & Settings
        with admin_subtabs[4]:
            st.markdown("### Store Configuration & Password Generator")
            st.info(f"Configured Business WhatsApp Number: **`+{WHATSAPP_NUMBER}`**")

            with st.form("pwd_hash_gen_form"):
                st.markdown("#### Change Admin Password")
                new_plain_pwd = st.text_input("Enter New Password", placeholder="e.g. ShahStore2024!")
                btn_gen = st.form_submit_button("Generate New Hash")

                if btn_gen and new_plain_pwd:
                    gen_hash = hash_password(new_plain_pwd)
                    st.success("Copy the line below into `utils/helpers.py` under `ADMIN_PASSWORD_HASH`:")
                    st.code(f"ADMIN_PASSWORD_HASH = '{gen_hash}'", language="python")

# -----------------------------------------------------------------------------
# GLOBAL FOOTER
# -----------------------------------------------------------------------------
st.markdown(f"""
<div class="store-footer">
    <p><b>{BUSINESS_NAME}</b> - Certified Pre-Owned Home Theaters & Sound Engineering</p>
    <p>Phone / WhatsApp: <b>{STORE_PHONE_DISPLAY}</b> | Hours: {STORE_HOURS}</p>
    <p style="margin-top: 0.5rem; color: #94a3b8;">
        All systems 100% bench-tested, optical/HDMI verified, and backed by our 7-Day Testing Guarantee.
    </p>
    <p style="font-size: 0.8rem; color: #cbd5e1; margin-top: 1rem;">
        &copy; {datetime.now().year} {BUSINESS_NAME}. All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)
