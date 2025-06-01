# streamlit_app.py

import streamlit as st
from scraper import scrape_amazon_product, write_headers, FIELDS, CSV_FILE

st.set_page_config(
    page_title="Amazon Product Scraper",
    page_icon="🛍️",
    layout="centered"
)

st.markdown("# 🛍️ Amazon Product Scraper")
st.markdown("Paste an Amazon product URL below to extract product details.")
st.markdown(
    "📝 **Note:** Amazon may block requests if you paste multiple links too quickly. "
    "Please wait a few seconds between scrapes to avoid getting blocked."
)

write_headers()

url = st.text_input("🔗 Enter Amazon Product URL", placeholder="https://www.amazon.in/...")

if st.button("🚀 Scrape Product"):
    if not url.startswith("http"):
        st.warning("⚠️ Please enter a valid Amazon product URL.")
    else:
        with st.spinner("Scraping product data..."):
            result = scrape_amazon_product(url)

        if result.get("error"):
            st.error(f"❌ Error: {result['error']}")
        else:
            st.success("✅ Product scraped successfully!")

            if result["Image URL"] != "NA":
                st.image(result["Image URL"], caption=result["Title"], width=250)

            st.markdown("### 📦 Product Information")
            for field in FIELDS:
                if field != "Image URL":
                    st.markdown(f"**{field}:** {result[field]}")

            with open(CSV_FILE, "rb") as f:
                st.download_button(
                    label="📥 Download CSV",
                    data=f,
                    file_name="amazon_product_data.csv",
                    mime="text/csv"
                )

# Footer
st.markdown("---")
st.markdown(
    """
    Made with ❤️ using [Streamlit](https://streamlit.io/) by **Mehul Jain**  
    [![LinkedIn](https://cdn-icons-png.flaticon.com/24/174/174857.png)](https://www.linkedin.com/in/mehul-jain-368020193)
    """,
    unsafe_allow_html=True
)
