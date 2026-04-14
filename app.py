import base64
import os

import streamlit as st
from dotenv import load_dotenv

st.set_page_config(page_title="DGA Operations Hub", layout="wide")

load_dotenv()


def get_env(key, default=None, cast=str):
    try:
        if key in st.secrets:
            val = st.secrets[key]
        else:
            val = os.getenv(key, default)
    except Exception:
        val = os.getenv(key, default)

    try:
        return cast(val) if val is not None else default
    except Exception:
        return default


@st.cache_resource(ttl=None)
def _get_logo_path_robustly(default_path: str = "assets/dga_logo.png") -> str | None:
    logo_path_base = get_env("COMPANY_LOGO_PATH", default_path)

    if os.path.exists(logo_path_base):
        return logo_path_base

    dirname, basename = os.path.split(logo_path_base)

    variations = [
        os.path.join(dirname.capitalize(), basename.capitalize()),
        os.path.join(dirname.lower(), basename.capitalize()),
        os.path.join(dirname.capitalize(), basename.lower()),
    ]

    for path in variations:
        if os.path.exists(path):
            return path

    if dirname == "assets":
        root_path = basename
        if os.path.exists(root_path):
            return root_path

    return None


COMPANY_LOGO_PATH = _get_logo_path_robustly()


@st.cache_resource(ttl=None)
def _get_app_logo_path(default_path: str = "assets/dga_logo_white.png") -> str | None:
    app_logo_path = get_env("APP_LOGO_PATH", default_path)
    if os.path.exists(app_logo_path):
        return app_logo_path
    return COMPANY_LOGO_PATH


@st.cache_resource(ttl=None)
def _asset_data_uri(path: str, mime_type: str) -> str:
    if not path or not os.path.exists(path):
        return ""
    with open(path, "rb") as asset_file:
        encoded = base64.b64encode(asset_file.read()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


APP_LOGO_PATH = _get_app_logo_path()
HUB_HEADER_LOGO_PATH = "assets/dga_logo_white.png" if os.path.exists("assets/dga_logo_white.png") else APP_LOGO_PATH
QUOTE_PATENT_TILE_PATH = "assets/ahhhh-whit.png"
QUOTE_TOOL_URL = get_env("QUOTE_TOOL_URL", "https://dga-quote-tool-v5.streamlit.app")
WAREHOUSE_QUEUE_URL = get_env("WAREHOUSE_QUEUE_URL", "https://dga-warehouse-inventory.netlify.app")
CUSTOM_DISC_ORDERING_URL = get_env("CUSTOM_DISC_ORDERING_URL", "https://dga-custom-disc-ordering.onrender.com")
ARTWORK_GENERATOR_URL = get_env("ARTWORK_GENERATOR_URL", "https://dga-artwork-preview-generator.streamlit.app")
PDGA_CONTACT_SCRAPER_URL = get_env("PDGA_CONTACT_SCRAPER_URL", "https://dga-scraper-app.streamlit.app")
MACH_FAMILY_FORECASTING_URL = get_env("MACH_FAMILY_FORECASTING_URL", "https://mach-family-po-planner.streamlit.app")
IT_TICKETS_URL = get_env("IT_TICKETS_URL", "https://it-tickets-jigv.onrender.com")
BCTS_FORM_URL = get_env("BCTS_FORM_URL", "")


TOOL_ROWS = [
    [
        {
            "label": "Sales",
            "label_class": "sales",
            "title": "Quote Tool",
            "description": "Build quotes, process orders, generate the exact customer-facing PDFs, and jump into the processed-orders history page.",
            "button_text": "Quote Tool",
            "url": QUOTE_TOOL_URL,
        },
        {
            "label": "Warehouse",
            "label_class": "warehouse",
            "title": "Orders / Warehouse Queue",
            "description": "Jump into the warehouse app to review today's orders, move jobs in the queue, apply inventory, and work from the warehouse inventory layout.",
            "button_text": "Warehouse Tool",
            "url": WAREHOUSE_QUEUE_URL,
        },
    ],
    [
        {
            "label": "Custom Orders",
            "label_class": "custom-orders",
            "title": "DGA Custom Disc Ordering",
            "description": "Open the custom disc ordering app for wholesale custom stamp and tournament ordering workflows.",
            "button_text": "Custom Disc Ordering",
            "url": CUSTOM_DISC_ORDERING_URL,
        },
        {
            "label": "Creative",
            "label_class": "creative",
            "title": "Artwork Preview Generator",
            "description": "Launch the artwork generator to build and review preview images for customer designs and internal approvals.",
            "button_text": "Artwork Preview Generator",
            "url": ARTWORK_GENERATOR_URL,
        },
    ],
    [
        {
            "label": "Outreach",
            "label_class": "outreach",
            "title": "PDGA Event Contact Scraper",
            "description": "Pull tournament director contact details and export event contact lists for outreach, planning, and operations follow-up.",
            "button_text": "PDGA Scraper",
            "url": PDGA_CONTACT_SCRAPER_URL,
        },
        {
            "label": "Forecasting",
            "label_class": "",
            "title": "Mach Family Forecasting",
            "description": "Open the Mach Family PO planner for live forecasting while the full hub experience is still being built out.",
            "button_text": "Mach Family Forecasting",
            "url": MACH_FAMILY_FORECASTING_URL,
            "status": "In Progress • Live Planner",
            "is_construction": True,
        },
    ],
    [
        {
            "label": "Operations",
            "label_class": "",
            "title": "BCTS Form",
            "description": "The BCTS Form is being built now, and this spot is reserved so it can drop straight into the hub when it's ready.",
            "button_text": "BCTS Form" if BCTS_FORM_URL else "UNDER CONSTRUCTION",
            "url": BCTS_FORM_URL,
            "status": "Live" if BCTS_FORM_URL else "Under Construction • Coming Soon",
            "is_construction": not bool(BCTS_FORM_URL),
        },
        {
            "label": "Support",
            "label_class": "support",
            "title": "IT Tickets",
            "description": "Jump into the IT ticket app to review submitted issues, track follow-up, and keep support requests moving.",
            "button_text": "Submit IT Ticket",
            "url": IT_TICKETS_URL,
        },
    ],
]


def render_tool_card(tool: dict) -> None:
    card_classes = ["welcome-card"]
    if tool.get("is_construction"):
        card_classes.append("is-construction")

    label_classes = ["welcome-card-label"]
    if tool.get("label_class"):
        label_classes.append(tool["label_class"])

    status_text = tool.get("status", "")
    status_classes = ["welcome-card-status"]
    if not status_text:
        status_classes.append("is-empty")
    status_markup = f'<span class="{" ".join(status_classes)}">{status_text}</span>'

    description = tool["description"].replace("'", "&apos;")

    st.markdown(
        f"""
        <div class="{' '.join(card_classes)}">
            <span class="{' '.join(label_classes)}">{tool["label"]}</span>
            <h3>{tool["title"]}</h3>
            <p>{description}</p>
            {status_markup}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if tool.get("url"):
        if hasattr(st, "link_button"):
            st.link_button(tool["button_text"], tool["url"], use_container_width=True)
        else:
            st.markdown(f'[{tool["button_text"]}]({tool["url"]})')
        return

    st.button(tool["button_text"], use_container_width=True, disabled=True)


def render_operations_hub() -> None:
    logo_markup = ""
    welcome_patent_uri = _asset_data_uri(QUOTE_PATENT_TILE_PATH, "image/png")
    if HUB_HEADER_LOGO_PATH and os.path.exists(HUB_HEADER_LOGO_PATH):
        with open(HUB_HEADER_LOGO_PATH, "rb") as logo_file:
            encoded_logo = base64.b64encode(logo_file.read()).decode("ascii")
        logo_markup = (
            '<div class="welcome-logo-wrap">'
            f'<img src="data:image/png;base64,{encoded_logo}" alt="DGA logo" class="welcome-logo" />'
            "</div>"
        )

    welcome_patent_markup = '<div class="welcome-patent-bg"></div>' if welcome_patent_uri else ""

    left_border_markup = ""
    right_border_markup = ""
    left_border_path = "assets/hub-border-right.jpeg"
    right_border_path = "assets/hub-border-left.jpeg"

    if os.path.exists(left_border_path):
        with open(left_border_path, "rb") as left_file:
            encoded_left = base64.b64encode(left_file.read()).decode("ascii")
        left_border_markup = (
            '<div class="welcome-side-art welcome-side-art-left">'
            f'<img src="data:image/jpeg;base64,{encoded_left}" alt="Disc golf basket" />'
            "</div>"
        )

    if os.path.exists(right_border_path):
        with open(right_border_path, "rb") as right_file:
            encoded_right = base64.b64encode(right_file.read()).decode("ascii")
        right_border_markup = (
            '<div class="welcome-side-art welcome-side-art-right">'
            f'<img src="data:image/jpeg;base64,{encoded_right}" alt="Disc golf basket" />'
            "</div>"
        )

    st.markdown(
        """
        <style>
            .welcome-stage {
                position: relative;
                overflow: hidden;
            }
            [data-testid="stAppViewContainer"] .main .block-container {
                position: relative;
                z-index: 3;
                max-width: 1200px;
                padding-top: 0.55rem;
                padding-bottom: 1.1rem;
                padding-left: 0.9rem;
                padding-right: 0.9rem;
                box-sizing: border-box;
            }
            .welcome-side-art {
                position: fixed;
                top: 0;
                bottom: 0;
                width: min(16vw, 220px);
                z-index: 1;
                overflow: hidden;
                pointer-events: none;
                opacity: 0.9;
                filter: grayscale(0.01) saturate(1.02) brightness(0.98) contrast(1.03);
            }
            .welcome-patent-bg {
                position: fixed;
                top: 0;
                bottom: 0;
                left: min(16vw, 220px);
                right: min(16vw, 220px);
                z-index: 0;
                pointer-events: none;
                opacity: 0.14;
                background-image: url("__WELCOME_PATENT_URI__");
                background-repeat: no-repeat;
                background-position: center top;
                background-size: 145% auto;
            }
            .welcome-side-art img {
                width: 100%;
                height: 100%;
                object-fit: cover;
                object-position: center;
                display: block;
            }
            .welcome-side-art-left {
                left: 0;
                object-position: 18% center;
                mask-image: linear-gradient(to right, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 1) 42%, rgba(0, 0, 0, 0.82) 62%, rgba(0, 0, 0, 0.38) 82%, transparent 100%);
                -webkit-mask-image: linear-gradient(to right, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 1) 42%, rgba(0, 0, 0, 0.82) 62%, rgba(0, 0, 0, 0.38) 82%, transparent 100%);
            }
            .welcome-side-art-right {
                right: 0;
                object-position: 42% center;
                mask-image: linear-gradient(to left, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 1) 42%, rgba(0, 0, 0, 0.82) 62%, rgba(0, 0, 0, 0.38) 82%, transparent 100%);
                -webkit-mask-image: linear-gradient(to left, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 1) 42%, rgba(0, 0, 0, 0.82) 62%, rgba(0, 0, 0, 0.38) 82%, transparent 100%);
            }
            .welcome-side-art-left img {
                object-position: 18% center;
            }
            .welcome-side-art-right img {
                object-position: 42% center;
            }
            .welcome-hero {
                text-align: center;
                margin-bottom: 0.75rem;
            }
            .welcome-logo-wrap {
                display: flex;
                justify-content: center;
                margin-bottom: 0.75rem;
            }
            .welcome-logo {
                display: block;
                width: 150px;
                height: auto;
            }
            .welcome-brand {
                text-align: center;
            }
            .welcome-brand h1 {
                margin: 0 0 5px;
                font-size: 1.75rem;
                line-height: 1.02;
            }
            .welcome-brand p {
                margin: 0 0 5px;
                color: rgba(250, 250, 250, 0.76);
                font-size: 0.85rem;
                max-width: 410px;
                margin-left: auto;
                margin-right: auto;
            }
            .welcome-signoff {
                display: inline-block;
                color: rgba(250, 250, 250, 0.64);
                font-size: 0.78rem;
                letter-spacing: 0.03em;
            }
            .welcome-card {
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 14px 14px 12px;
                background: rgba(17, 20, 26, 0.94);
                height: 204px;
                display: flex;
                flex-direction: column;
                overflow: hidden;
                box-sizing: border-box;
            }
            .welcome-card.is-construction {
                border-color: rgba(255, 184, 76, 0.35);
                background:
                    linear-gradient(135deg, rgba(255, 184, 76, 0.12), rgba(17, 20, 26, 0.94) 42%),
                    repeating-linear-gradient(
                        -45deg,
                        rgba(255, 184, 76, 0.08) 0 12px,
                        rgba(17, 20, 26, 0.0) 12px 24px
                    ),
                    rgba(17, 20, 26, 0.94);
                box-shadow: inset 0 0 0 1px rgba(255, 214, 102, 0.06);
            }
            .welcome-card-label {
                display: inline-flex;
                align-items: center;
                width: auto;
                max-width: fit-content;
                padding: 2px 8px;
                border-radius: 999px;
                font-size: 0.62rem;
                letter-spacing: 0.05em;
                text-transform: uppercase;
                color: rgba(250, 250, 250, 0.72);
                background: rgba(255, 255, 255, 0.1);
                margin-bottom: 7px;
                align-self: flex-start;
            }
            .welcome-card-label.sales {
                color: rgba(255, 163, 172, 0.95);
                background: rgba(255, 98, 117, 0.16);
                border: 1px solid rgba(255, 98, 117, 0.24);
            }
            .welcome-card-label.warehouse {
                color: rgba(134, 226, 255, 0.96);
                background: rgba(86, 196, 255, 0.16);
                border: 1px solid rgba(86, 196, 255, 0.24);
            }
            .welcome-card-label.custom-orders {
                color: rgba(171, 239, 126, 0.96);
                background: rgba(155, 231, 92, 0.14);
                border: 1px solid rgba(155, 231, 92, 0.22);
            }
            .welcome-card-label.creative {
                color: rgba(222, 147, 255, 0.96);
                background: rgba(192, 116, 255, 0.15);
                border: 1px solid rgba(192, 116, 255, 0.24);
            }
            .welcome-card-label.outreach {
                color: rgba(255, 175, 112, 0.96);
                background: rgba(255, 143, 86, 0.15);
                border: 1px solid rgba(255, 143, 86, 0.24);
            }
            .welcome-card-label.support {
                color: rgba(146, 183, 255, 0.96);
                background: rgba(124, 164, 255, 0.15);
                border: 1px solid rgba(124, 164, 255, 0.24);
            }
            .welcome-card.is-construction .welcome-card-label {
                color: rgba(255, 211, 101, 0.96);
                background: rgba(255, 197, 92, 0.16);
                border: 1px solid rgba(255, 197, 92, 0.26);
            }
            .welcome-card-status {
                display: block;
                margin-top: auto;
                padding-top: 8px;
                min-height: 1.1rem;
                font-size: 0.69rem;
                font-weight: 600;
                letter-spacing: 0.04em;
                text-transform: uppercase;
                color: rgba(255, 214, 102, 0.9);
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            .welcome-card-status.is-empty {
                visibility: hidden;
            }
            .welcome-card h3 {
                margin: 0 0 6px;
                font-size: 0.9rem;
            }
            .welcome-card p {
                color: rgba(250, 250, 250, 0.74);
                line-height: 1.34;
                flex: 1 1 auto;
                min-height: 0;
                margin: 0;
                font-size: 0.74rem;
                overflow: hidden;
            }
            .welcome-row {
                margin-top: 0.7rem;
            }
            .stButton > button,
            [data-testid="stLinkButton"] a {
                min-height: 2.5rem;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                font-size: 0.92rem;
                padding-left: 0.95rem;
                padding-right: 0.95rem;
                background: #ff3341;
                color: #ffffff;
                border: 1px solid #ff3341;
                transition: background 0.18s ease, border-color 0.18s ease, transform 0.18s ease;
            }
            .stButton > button:hover,
            [data-testid="stLinkButton"] a:hover {
                background: #ff4855;
                border-color: #ff4855;
                color: #ffffff;
            }
            .stButton > button:disabled {
                background: rgba(255, 51, 65, 0.3);
                border-color: rgba(255, 51, 65, 0.3);
                color: rgba(255, 255, 255, 0.72);
            }
            [data-testid="column"] {
                min-width: 0;
            }
            @media (min-width: 901px) {
                [data-testid="stHorizontalBlock"] {
                    align-items: stretch;
                }
                [data-testid="stHorizontalBlock"] > [data-testid="column"] > div {
                    height: 100%;
                }
            }
            @media (max-width: 1180px) {
                .welcome-side-art {
                    display: none;
                }
                .welcome-patent-bg {
                    left: 0;
                    right: 0;
                }
            }
            @media (max-width: 900px) {
                .welcome-card {
                    height: auto;
                }
                .welcome-card p {
                    flex: 0 0 auto;
                }
            }
            @media (min-width: 721px) and (max-width: 980px) {
                .welcome-card {
                    height: 220px;
                }
            }
            @media (max-width: 720px) {
                [data-testid="stAppViewContainer"] .main .block-container {
                    padding-left: 0.7rem;
                    padding-right: 0.7rem;
                }
            }
        </style>
        """.replace("__WELCOME_PATENT_URI__", welcome_patent_uri),
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="welcome-stage">{welcome_patent_markup}{left_border_markup}{right_border_markup}',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="welcome-hero">', unsafe_allow_html=True)
    if logo_markup:
        st.markdown(logo_markup, unsafe_allow_html=True)
    st.markdown(
        """
        <div class="welcome-brand">
            <h1>DGA Operations Hub</h1>
            <p>Your launch point for quoting, order processing, warehouse flow, artwork review, and event outreach.</p>
            <span class="welcome-signoff">Designed by CZ</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    for row in TOOL_ROWS:
        if st.session_state.get("_force_single_column_layout", False):
            single_col = st.columns(1)[0]
            with single_col:
                render_tool_card(row[0])
                st.markdown('<div class="welcome-row"></div>', unsafe_allow_html=True)
                render_tool_card(row[1])
        else:
            _, left_col, right_col, _ = st.columns([0.34, 1, 1, 0.34], gap="medium")

            with left_col:
                render_tool_card(row[0])

            with right_col:
                render_tool_card(row[1])

        st.markdown('<div class="welcome-row"></div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def main():
    render_operations_hub()


if __name__ == "__main__":
    main()
