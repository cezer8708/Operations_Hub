# DGA Operations Hub

Standalone Streamlit launcher for DGA internal operations tools.

## Local run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Environment

- `QUOTE_TOOL_URL`: URL for the quote tool app
- `WAREHOUSE_QUEUE_URL`: Warehouse queue app URL
- `CUSTOM_DISC_ORDERING_URL`: Custom ordering app URL
- `ARTWORK_GENERATOR_URL`: Artwork generator app URL
- `PDGA_CONTACT_SCRAPER_URL`: PDGA scraper app URL
- `MACH_FAMILY_FORECASTING_URL`: Mach Family planner URL
- `IT_TICKETS_URL`: IT tickets app URL

## Deploy

Deploy as a standalone Streamlit app and set `QUOTE_TOOL_URL` to the hosted quote tool URL.
