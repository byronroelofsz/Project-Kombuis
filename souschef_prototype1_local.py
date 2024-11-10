import streamlit as st
import os
import snowflake.connector
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image  # To ensure compatibility with different image formats


# Set page config to wide layout
st.set_page_config(layout="wide", page_title="Sous Chef - Your Personal AI Agent")

# Load and display logo
logo = Image.open("sous_chef_logo1.webp")
st.sidebar.image(logo, width=150)  # Adjust width as needed

def get_snowflake_connection():
    return snowflake.connector.connect(
        user='BYRONKOMBUIS',
        password='Vry<#233bur>g',
        account='ixmezcl-ku05983',
        warehouse='COMPUTE_WH',
        database='KOMBUIS_PROTOTYPE1',
        schema='PUBLIC'
    )


# Hide the Streamlit footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    footer:after {content:'Sous Chef © 2024'; visibility: visible; display: block; 
        position: relative; color: grey; padding: 5px; top: 3px;
    }
    </style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Set up the Streamlit app title and introductory text
st.title("Sous Chef - Your Personal AI Agent")
st.write("Welcome to prototype 1")

# Sidebar setup for Project Kombuis information
st.sidebar.header("Sous Chef")
st.sidebar.write("""
Sous Chef is an AI-powered data hub that helps food brands optimize operations in a dynamic market.
By integrating data from multiple sources—delivery platforms, supplier networks, industry news, 
and social media—it provides actionable insights to boost profitability, customer engagement, and revenue.
With strategic focus areas in Revenue, Supplier Costs, Core Industry Integrations, and Marketing Insights,
Sous Chef empowers data-driven decisions that enhance competitive advantage.
""")

# Sidebar setup for modules
st.sidebar.title("Modules")
module = st.sidebar.radio("Select Module", [
    "Home - Search", "P&L", "Revenue", "Suppliers", "Menu", 
    "Competitors", "Global Markets & News", "Marketing"
])

# Function for displaying search module
def display_search_module():
    st.header("What can I help you with?")
    search_query = st.text_input("Message your SOUS CHEF", "", placeholder="Type your question here...")

    # Suggested question examples organized by module categories
    st.write("### Question Examples")
    col1, col2 = st.columns(2)

    with col1:
        # P&L
        st.write("**P&L**")
        st.button("What are my key financial metrics this month?", key="pnl_key_metrics")
        st.button("What is my profit margin?", key="pnl_profit_margin")
        st.button("How is my EBITDA trending?", key="pnl_ebitda_trend")

        # Revenue
        st.write("**Revenue**")
        st.button("What was my revenue last week?", key="revenue_last_week")
        st.button("How did each location perform in terms of revenue?", key="revenue_per_location")
        st.button("What are the top revenue channels?", key="revenue_channels")

        # Suppliers
        st.write("**Suppliers**")
        st.button("Which supplier has the best prices this week?", key="supplier_best_price")
        st.button("What are my supplier trends over time?", key="supplier_trends")
        st.button("Which suppliers am I spending the most on?", key="supplier_most_spending")

    with col2:
        # Menu
        st.write("**Menu**")
        st.button("What was my top selling item last week?", key="menu_top_selling_item")
        st.button("Which menu item has the highest profit margin?", key="menu_highest_margin")
        st.button("What menu items are most popular by location?", key="menu_popular_by_location")

        # Competitors
        st.write("**Competitors**")
        st.button("How do my ratings compare to competitors?", key="competitor_rating_comparison")
        st.button("What are my competitors' top-selling items?", key="competitor_top_items")
        
        # Global Markets & News
        st.write("**Global Markets & News**")
        st.button("What are global prices for key ingredients?", key="global_prices")
        st.button("Are there any relevant industry updates this week?", key="global_news_updates")

        # Marketing
        st.write("**Marketing**")
        st.button("What are my social media stats?", key="marketing_social_stats")
        st.button("How is my brand rating across platforms?", key="marketing_brand_rating")
        st.button("What campaigns performed best last month?", key="marketing_campaign_performance")

    # If a search query is entered
    if search_query:
        st.write("**Response from SOUS CHEF:**")
        st.write(f"Searching for insights related to: {search_query}")
        st.write("Here’s an insight based on your query...")


# Function for displaying P&L module
def display_pnl_module():
    st.header("Profit & Loss (P&L) Overview")
    st.write("An in-depth look into your revenue, costs, and profitability metrics.")

    # Key Metrics at the top
    st.subheader("Key Financial Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)

    # Placeholder metrics for now; replace with real data
    revenue = 120000  # Sample data
    cogs = 60000      # Sample data
    orders = 1500     # Sample data
    profit_per_order = 12.50  # Sample data
    margin = 0.25     # Sample data

    with col1:
        st.metric(label="Revenue", value=f"${revenue:,.2f}")
    with col2:
        st.metric(label="COGS", value=f"${cogs:,.2f}")
    with col3:
        st.metric(label="Orders", value=f"{orders:,}")
    with col4:
        st.metric(label="Profit per Order", value=f"${profit_per_order:.2f}")
    with col5:
        st.metric(label="Margin", value=f"{margin:.2%}")

    # Detailed P&L
    st.subheader("Detailed P&L")
    st.write("Explore detailed profit and loss components below, including revenue actuals and forecasts, COGS, EBITDA, and operating profit.")

    # Side-by-side graphs for Revenue & COGS
    col1, col2 = st.columns(2)

    # Revenue Actuals & Forecasts in first column
    with col1:
        st.write("### Revenue Actuals & Forecasts")
        st.write("Compare actual revenue with aimed and adjusted forecasts.")

        # Placeholder data for actuals and forecasts
        actual_revenue = [100000, 105000, 110000]  # Monthly or weekly data
        aimed_forecast = [102000, 107000, 115000]
        adjusted_forecast = [98000, 104000, 108000]
        periods = ["Jan", "Feb", "Mar"]

        fig, ax = plt.subplots()
        ax.plot(periods, actual_revenue, label="Actual Revenue", marker="o")
        ax.plot(periods, aimed_forecast, label="Aimed Forecast", marker="o")
        ax.plot(periods, adjusted_forecast, label="Adjusted Forecast", marker="o")
        ax.set_xlabel("Period")
        ax.set_ylabel("Revenue ($)")
        ax.legend()
        st.pyplot(fig)

    # COGS (Cost of Goods Sold) in second column
    with col2:
        st.write("### Cost of Goods Sold (COGS)")
        st.write("Overview of costs directly associated with producing goods sold.")

        # Placeholder COGS breakdown
        cogs_data = pd.DataFrame({
            "Category": ["Raw Materials", "Packaging", "Labor", "Other"],
            "Cost": [30000, 10000, 15000, 5000]
        })
        fig, ax = plt.subplots()
        ax.pie(cogs_data["Cost"], labels=cogs_data["Category"], autopct='%1.1f%%', startangle=90)
        ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle
        st.pyplot(fig)

    # EBITDA and Operating Profit
    st.write("### EBITDA & Operating Profit")
    st.write("Analyze earnings before interest, taxes, depreciation, and amortization (EBITDA) at both site and head office levels.")

    # Placeholder data for EBITDA
    ebitda_site = 20000  # Sample site-based EBITDA
    ebitda_head_office = 15000  # Sample head-office EBITDA
    operating_profit_location = 5000  # Sample operating profit

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="EBITDA (Site)", value=f"${ebitda_site:,.2f}")
    with col2:
        st.metric(label="EBITDA (Head Office)", value=f"${ebitda_head_office:,.2f}")
    with col3:
        st.metric(label="Operating Profit (Location)", value=f"${operating_profit_location:,.2f}")

# Function for displaying revenue module
def display_revenue_module():
    st.header("Revenue Analytics")
    st.write("""
    This module provides comprehensive analytics for your brand and kitchens across various revenue channels. 
    Use filters to explore key insights such as order distribution by delivery channel and payout analysis. 
    You can select specific channels to focus on, or choose "All Channels" to view aggregated data across all channels. 
    Visualize order distribution, analyze payouts, and download filtered data for further exploration.
    """)

    # Get the current Snowflake session
    conn = get_snowflake_connection()


    # Query data from Snowflake
    query_result = pd.read_sql("SELECT * FROM KOMBUIS_PROTOTYPE1.PUBLIC.REVENUE_STREAM_OTTER_ORDERHISTORY", conn)
    conn.close()
    queried_data = query_result.rename(columns=str.lower)

    # Filter by brand
    st.write("### Filter by Brand & Location")
    brand_selection = st.selectbox("Select Brand", options=queried_data['organization'].unique(), key="brand_selection")
    filtered_data_by_brand = queried_data[queried_data['organization'] == brand_selection]

    # Filter by location
    location_selection = st.selectbox("Select Location", options=filtered_data_by_brand['location'].unique(), key="location_selection")
    filtered_data = filtered_data_by_brand[filtered_data_by_brand['location'] == location_selection]

    # Calculate key metrics on filtered data
    num_orders = len(filtered_data)
    total_subtotal = filtered_data['subtotal'].sum()
    total_discount = filtered_data['discount'].sum()
    total_items_quantity = filtered_data['items_quantity'].sum()

    # Calculate metrics
    average_basket_size = total_subtotal / num_orders if num_orders else 0
    average_discount_per_order = total_discount / num_orders if num_orders else 0
    average_items_per_order = total_items_quantity / num_orders if num_orders else 0
    average_orders_per_day = num_orders / 10

    # Display key metrics
    st.write("### Key Metrics")
    st.write(f"**Average Basket Size:** ${average_basket_size:.2f}")
    st.write(f"**Average Discount per Order:** ${average_discount_per_order:.2f}")
    st.write(f"**Average Items per Order:** {average_items_per_order:.2f}")
    st.write(f"**Average Orders per Day:** {average_orders_per_day:.2f}")

    # Display analytics
    st.write("### Analytics")
    col1, col2 = st.columns(2)

    # Pie chart for orders by delivery channel
    with col1:
        st.write("Orders by Delivery Channel")
        channel_counts = filtered_data['channel'].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(channel_counts, labels=channel_counts.index, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)

    # Bar chart for payout by delivery channel
    with col2:
        st.write("Payout by Delivery Channel")
        payout_by_channel = filtered_data.groupby('channel')['payout'].sum()
        fig2, ax2 = plt.subplots()
        payout_by_channel.plot(kind='bar', ax=ax2)
        ax2.set_ylabel("Total Payout")
        ax2.set_xlabel("Delivery Channel")
        st.pyplot(fig2)

    # Additional filters and data download
    st.write("### Filter (Otter) Data by Revenue Channel")
    channel_options = ['All Channels'] + list(filtered_data['channel'].unique())
    channel_selection = st.selectbox("Select Delivery Channel", options=channel_options, key="channel_selection")
    
    # Apply filtering based on selection
    if channel_selection == 'All Channels':
        filtered_data_by_channel = filtered_data
    else:
        filtered_data_by_channel = filtered_data[filtered_data['channel'] == channel_selection]
    
    # Convert the filtered data to CSV for download
    csv_data = filtered_data_by_channel.to_csv(index=False)
    
    st.download_button("Download data as CSV", data=csv_data, file_name='filtered_data.csv', mime='text/csv')
    st.write("Filtered Data Preview:")
    st.dataframe(filtered_data_by_channel)

# Function for displaying suppliers module
def display_suppliers_module():
    st.header("Supplier Comparisons")
    st.write("Analyze supplier options to find the best prices and compare with previous weeks.")

    # Comparison and selection sections
    st.subheader("Comparisons")
    st.write("Drop line of current suppliers")  # Placeholder for future supplier comparison feature

    st.subheader("Supplier Selection")
    supplier_type = st.selectbox("Select Current Supplier", ["Urban Foods", "JJ FOODSERVICES"], key="supplier_type")
    available_supplier = st.selectbox("Select All Available Suppliers", ["Supplier A", "Supplier B", "Supplier C"], key="available_supplier")

    st.subheader("Best Price Comparison")
    st.write("Compare this week's price with last week's price.")  # Placeholder for future price comparison feature
    st.write("---")

    # Display data based on selected supplier
    st.subheader(f"{supplier_type} - Supplier Cost Analytics")

    # Connect to Snowflake and query data based on supplier type
    conn = get_snowflake_connection()
    if supplier_type == "Urban Foods":
        supplier_data = pd.read_sql("SELECT * FROM KOMBUIS_PROTOTYPE1.PUBLIC.SUPPLIER_COST_URBAN_FOODS", conn)
        supplier_data.columns = supplier_data.columns.str.lower()
        supplier_data['urban_price'] = pd.to_numeric(supplier_data['urban_price'], errors='coerce')

        # Display analytics for Urban Foods
        col1, col2 = st.columns(2)
        with col1:
            st.write("Distribution by Major Description")
            major_counts = supplier_data['major_description'].value_counts()
            fig1, ax1 = plt.subplots()
            ax1.pie(major_counts, labels=major_counts.index, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)

        with col2:
            st.write("Future Graphic Placeholder")  # Placeholder for additional visualizations

        # Filters for detailed view for Urban Foods
        major_selection = st.selectbox("Select Major Description", options=supplier_data['major_description'].unique())
        minor_selection = st.selectbox("Select Minor Description", options=supplier_data[supplier_data['major_description'] == major_selection]['minor_description'].unique())

        # Filtered data display and download
        filtered_supplier_data = supplier_data[(supplier_data['major_description'] == major_selection) & (supplier_data['minor_description'] == minor_selection)]
        csv_supplier_data = filtered_supplier_data.to_csv(index=False)
        st.download_button("Download data as CSV", data=csv_supplier_data, file_name='filtered_supplier_data_urban_foods.csv', mime='text/csv')
        st.write("Filtered Supplier Data Preview:")
        st.dataframe(filtered_supplier_data)

    elif supplier_type == "JJ FOODSERVICES":
        # Query supplier data for JJ FOODSERVICES
        jjfoods_data = pd.read_sql("SELECT * FROM KOMBUIS_PROTOTYPE1.PUBLIC.SUPPLIER_COST_JJFOODSERVICES", conn)
        jjfoods_data.columns = jjfoods_data.columns.str.lower()
        jjfoods_data['del_price'] = pd.to_numeric(jjfoods_data['del_price'], errors='coerce')

        # Display analytics for JJ FOODSERVICES
        col1, col2 = st.columns(2)
        with col1:
            st.write("Distribution by Item Category")
            item_category_counts = jjfoods_data['item_category'].value_counts()
            fig2, ax2 = plt.subplots()
            ax2.pie(item_category_counts, labels=item_category_counts.index, autopct='%1.1f%%', startangle=90)
            ax2.axis('equal')
            st.pyplot(fig2)

        with col2:
            st.write("Future Graphic Placeholder")  # Placeholder for additional visualizations

        # Filter for item category in JJ FOODSERVICES
        item_category_selection = st.selectbox("Select Item Category", options=jjfoods_data['item_category'].unique())

        # Filter data based on selected item category
        filtered_jjfoods_data = jjfoods_data[jjfoods_data['item_category'] == item_category_selection]
        csv_jjfoods_data = filtered_jjfoods_data.to_csv(index=False)
        st.download_button("Download data as CSV", data=csv_jjfoods_data, file_name='filtered_supplier_data_jjfoods.csv', mime='text/csv')
        st.write("Filtered Supplier Data Preview:")
        st.dataframe(filtered_jjfoods_data)

    # Close the Snowflake connection
    conn.close()

def display_menu_module():
     # Example of AI-based ingredient and product suggestion
    st.subheader("Ingredient & Product List (Powered by AI)")
    st.write("""
    Specific ingredient list recommendations based on menu items:
    - Burgers: Beef, buns, cheese, sauces
    - Pizzas: Dough, cheese, tomato sauce, toppings
    - Salads: Lettuce, tomatoes, cucumbers, dressings
    """)
    st.write("Use AI to analyze and list ingredients and products from suppliers based on your menu.")


# Function for displaying competitors module
def display_competitors_module():
    st.header("Competitor Analytics")
    conn = get_snowflake_connection()

    competitor_data = pd.read_sql("SELECT * FROM KOMBUIS_PROTOTYPE1.PUBLIC.COMPETITOR_TAKEALYTICS", conn)
    conn.close()
    competitor_data.columns = competitor_data.columns.str.lower()

    name_selection = st.selectbox("Select Competitor Name", options=competitor_data['name'].unique())
    selected_data = competitor_data[competitor_data['name'] == name_selection]

    if not selected_data.empty:
        st.write("### Competitor Details")
        st.write(f"**City:** {selected_data['city'].iloc[0]}")
        st.write(f"**Ratings:** {selected_data['ratings'].iloc[0]}")
        st.write(f"**Hygiene:** {selected_data['hygiene'].iloc[0]}")
        st.write(f"**Social Score:** {selected_data['social'].iloc[0]}")
        st.write("**Food Types (DE):**", selected_data['venue_food_types_de'].iloc[0])
        st.write("**Food Types (JE):**", selected_data['venue_food_types_je'].iloc[0])
        st.dataframe(selected_data)

# Function for displaying global markets and news module
def display_global_markets_module():
    st.header("Global Markets")
    st.write("Explore the latest global market trends and data insights from top sources.")

    st.subheader("Bloomberg UK")
    st.markdown("[Visit Bloomberg UK](https://www.bloomberg.com/uk)")

    st.subheader("Reuters")
    st.markdown("[Visit Reuters](https://www.reuters.com/)")

    st.subheader("Statista")
    st.markdown("[Visit Statista](https://www.statista.com/)")

    st.header("Industry News")
    st.write("Stay updated with the latest news and trends in the restaurant and hospitality industry.")

    st.subheader("The Caterer - Restaurant News")
    st.markdown("[Visit The Caterer - Restaurant News](https://www.thecaterer.com/news/restaurant)")

    st.subheader("Restaurant Online")
    st.markdown("[Visit Restaurant Online](https://www.restaurantonline.co.uk/)")

    st.subheader("Code Hospitality")
    st.markdown("[Visit Code Hospitality](https://www.codehospitality.co.uk/)")

# Display selected module
if module == "Home - Search":
    display_search_module()
elif module == "P&L":
    display_pnl_module()
elif module == "Revenue":
    display_revenue_module()
elif module == "Suppliers":
    display_suppliers_module()
elif module == "Menu":
    display_menu_module()
elif module == "Competitors":
    display_competitors_module()
elif module == "Global Markets & News":
    display_global_markets_module()
else:
    st.write(f"The {module} module is currently under development.")

