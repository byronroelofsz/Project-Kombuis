import streamlit as st
import os
import snowflake.connector
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from geopy.adapters import RequestsAdapter
import requests
from datetime import datetime 

# Set page config to wide layout
st.set_page_config(layout="wide", page_title="Sous Chef - Your Personal AI Agent")

# Load and display logo
logo = Image.open("sous_chef_logo1.webp")
st.sidebar.image(logo, width=300)  # Adjust width as needed

# Display current date and time in the sidebar
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.sidebar.markdown(f"Welcome back, Jane Doe")
st.sidebar.markdown(f"**Date & Time:** {current_datetime}")

def get_snowflake_connection():
    return snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )


# Hide the Streamlit footer
hide_streamlit_style = """
    <style>
    footer {visibility: hidden;}
    footer:after {content:'Sous Chef © 2024'; visibility: visible; display: block; 
        position: relative; color: grey; padding: 5px; top: 3px;
    }
    </style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Sidebar setup for modules

st.sidebar.title("Modules")
module = st.sidebar.radio("Select Module", [
    "Home - Search", "P&L", "Revenue", "Suppliers", "Menu", 
    "Competitors", "Global Markets & News", "Marketing"
])

# Set up the Streamlit app title and introductory text
st.title("Sous Chef - Your Personal AI Agent")
st.write("Welcome to prototype 1")

# Sidebar setup for Project Kombuis information
st.sidebar.header("About")
st.sidebar.write("""
Sous Chef is an AI-powered data hub that helps food brands optimize operations in a dynamic market.
By integrating data from multiple sources—delivery platforms, supplier networks, industry news, 
and social media—it provides actionable insights to boost profitability, customer engagement, and revenue.
With strategic focus areas in Revenue, Supplier Costs, Core Industry Integrations, and Marketing Insights,
Sous Chef empowers data-driven decisions that enhance competitive advantage.
""")



#
def display_uk_postcode_map_with_multiple_pins(postcodes):
    # Check if the list of postcodes is empty
    if len(postcodes) == 0:
        st.write("No postcodes available to display on the map.")
        return

    first_postcode = postcodes[0]
    url = f"https://api.postcodes.io/postcodes/{first_postcode}"
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        data = response.json()["result"]
        map_obj = folium.Map(location=[data['latitude'], data['longitude']], zoom_start=10)

        # Loop over each postcode, adding a pin to the map
        for postcode in postcodes:
            url = f"https://api.postcodes.io/postcodes/{postcode}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()["result"]
                lat, lon = data['latitude'], data['longitude']
                folium.Marker([lat, lon], popup=f"Location: {postcode}").add_to(map_obj)
            else:
                st.write(f"Could not retrieve data for postcode: {postcode}")

        folium_static(map_obj)
    else:
        st.write("Could not initialize map with the first postcode.")

# Function for displaying search module
def display_search_module():
    st.header("What can I help you with?")
    search_query = st.text_input("Message your SOUS CHEF", "", placeholder="Type your question here...")

    # Suggested question examples organized by module categories
    st.write("### Question Examples")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # P&L
        st.write("**P&L**")
        st.button("What are my key financial metrics this month?", key="pnl_key_metrics")
        st.button("What is my profit margin?", key="pnl_profit_margin")
        st.button("How is my EBITDA trending?", key="pnl_ebitda_trend")

    with col2:
        # Revenue
        st.write("**Revenue**")
        st.button("What was my revenue last week?", key="revenue_last_week")
        st.button("How did each location perform in terms of revenue?", key="revenue_per_location")
        st.button("What are the top revenue channels?", key="revenue_channels")

    with col3:
        # Suppliers
        st.write("**Suppliers**")
        st.button("Which supplier has the best prices this week?", key="supplier_best_price")
        st.button("What are my supplier trends over time?", key="supplier_trends")
        st.button("Which suppliers am I spending the most on?", key="supplier_most_spending")

    with col4:
        # Menu
        st.write("**Menu**")
        st.button("What was my top selling item last week?", key="menu_top_selling_item")
        st.button("Which menu item has the highest profit margin?", key="menu_highest_margin")
        st.button("What menu items are most popular by location?", key="menu_popular_by_location")

    # Additional columns for other modules
    with col1:
        # Competitors
        st.write("**Competitors**")
        st.button("How do my ratings compare to competitors?", key="competitor_rating_comparison")
        st.button("What are my competitors' top-selling items?", key="competitor_top_items")
        
    with col2:
        # Global Markets & News
        st.write("**Global Markets & News**")
        st.button("What are global prices for key ingredients?", key="global_prices")
        st.button("Are there any relevant industry updates this week?", key="global_news_updates")

    with col3:
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

    st.write("### Find Location and Details by UK Postcode")
    postcode = st.text_input("Enter a UK postcode:", placeholder="e.g., SW1A 1AA")
    if postcode:
        display_uk_postcode_map_and_details(postcode)


# Function for displaying P&L module
def display_pnl_module():
    st.header("Profit & Loss (P&L) Overview")
    st.write("An in-depth look into your revenue, costs, and profitability metrics.")

    # Core Inputs Section
    st.subheader("Core Inputs")
    st.write("Primary revenue and cost inputs that impact gross profit.")

    core_data = {
        "Category": ["Revenue", "ODP Commission", "COGS"],
        "Notes": ["All forms of revenue", "Platform commission fees", "Supply Costs"],
        "Input/Value": [84704.89, 25411.47, 21176.22]
    }
    core_df = pd.DataFrame(core_data)
    st.table(core_df)

    # Gross Profit Section
    st.subheader("Gross Profit")
    st.write("Gross profit calculation based on fixed, variable, and labor costs.")

    gross_data = {
        "Category": ["Fixed Costs", "Variable Costs", "Labour"],
        "Notes": ["Rent, Rates, Service charge", "Utilities, waste management, consumables", "Zero hour contracts (shift staff)"],
        "Input/Value": [3500.00, 1000.00, 10920.00]
    }
    gross_df = pd.DataFrame(gross_data)
    st.table(gross_df)

    # Operating Profit Section
    st.subheader("Operating Profit")
    st.write("Calculation of operating profit after accounting for additional staff, marketing, and head office costs.")

    operating_data = {
        "Category": ["Staff Cost", "Marketing", "Head Office Costs"],
        "Notes": ["Full time (e.g., Managers)", "All marketing", "Included in business P&L not site P&L"],
        "Input/Value": [0.00, 500.00, 0.00]
    }
    operating_df = pd.DataFrame(operating_data)
    st.table(operating_df)

    # EBITDA Section
    st.subheader("EBITDA")
    st.write("Earnings before interest, taxes, depreciation, and amortization.")

    ebitda_value = core_data["Input/Value"][0] - core_data["Input/Value"][2] - sum(gross_data["Input/Value"]) - sum(operating_data["Input/Value"])
    st.metric(label="EBITDA", value=f"${ebitda_value:,.2f}")

    # Additional Key Metrics to Highlight
    st.subheader("Key Metrics to Highlight")
    highlight_data = {
        "Metric": ["Basket Size", "Gross Profit Margin", "Operating Profit Margin", "EBITDA Margin"],
        "Notes": ["Value", "Percentage", "Percentage", "Percentage"],
        "Calculation": [
            core_data["Input/Value"][0] / 1500,  # Placeholder calculation for basket size
            (core_data["Input/Value"][0] - core_data["Input/Value"][2]) / core_data["Input/Value"][0] * 100,
            ebitda_value / core_data["Input/Value"][0] * 100,
            ebitda_value / core_data["Input/Value"][0] * 100
        ]
    }
    highlight_df = pd.DataFrame(highlight_data)
    highlight_df["Calculation"] = highlight_df["Calculation"].apply(lambda x: f"{x:.2f}%" if isinstance(x, float) else f"${x:.2f}")
    st.table(highlight_df)

    # Graphs for Revenue & COGS
    col1, col2 = st.columns(2)

    # Revenue Actuals & Forecasts in the first column
    with col1:
        st.write("### Revenue Actuals & Forecasts")
        actual_revenue = [84704.89, 85400.00, 87000.00]  # Example data
        aimed_forecast = [86000.00, 87500.00, 88000.00]
        adjusted_forecast = [84000.00, 85000.00, 86000.00]
        periods = ["Jan", "Feb", "Mar"]

        fig, ax = plt.subplots()
        ax.plot(periods, actual_revenue, label="Actual Revenue", marker="o")
        ax.plot(periods, aimed_forecast, label="Aimed Forecast", marker="o")
        ax.plot(periods, adjusted_forecast, label="Adjusted Forecast", marker="o")
        ax.set_xlabel("Period")
        ax.set_ylabel("Revenue ($)")
        ax.legend()
        st.pyplot(fig)

    # COGS Breakdown in the second column
    with col2:
        st.write("### Cost of Goods Sold (COGS) Breakdown")
        cogs_data = pd.DataFrame({
            "Category": ["Raw Materials", "Packaging", "Labor", "Other"],
            "Cost": [12000, 4000, 3000, 176.22]
        })
        fig, ax = plt.subplots()
        ax.pie(cogs_data["Cost"], labels=cogs_data["Category"], autopct='%1.1f%%', startangle=90)
        ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle
        st.pyplot(fig)

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

    # Filters by brand and location in two columns
    st.write("### Filter by Brand & Location")
    col1, col2 = st.columns(2)
    with col1:
        brand_selection = st.selectbox("Select Brand", options=queried_data['organization'].unique(), key="brand_selection")
        filtered_data_by_brand = queried_data[queried_data['organization'] == brand_selection]
    with col2:
        location_selection = st.selectbox("Select Location", options=filtered_data_by_brand['location'].unique(), key="location_selection")
        filtered_data = filtered_data_by_brand[filtered_data_by_brand['location'] == location_selection]

    # Calculate key metrics on filtered data
    num_orders = len(filtered_data)
    total_subtotal = filtered_data['subtotal'].sum()
    total_discount = filtered_data['discount'].sum()
    total_items_quantity = filtered_data['items_quantity'].sum()

    # Calculate additional metrics
    average_basket_size = total_subtotal / num_orders if num_orders else 0
    average_discount_per_order = total_discount / num_orders if num_orders else 0
    average_items_per_order = total_items_quantity / num_orders if num_orders else 0
    average_orders_per_day = num_orders / 10

    # Display key metrics in table format
    st.write("### Key Metrics")
    metrics_data = {
        "Metric": ["Average Basket Size", "Average Discount per Order", "Average Items per Order", "Average Orders per Day"],
        "Value": [f"${average_basket_size:.2f}", f"${average_discount_per_order:.2f}", f"{average_items_per_order:.2f}", f"{average_orders_per_day:.2f}"]
    }
    metrics_df = pd.DataFrame(metrics_data)
    st.table(metrics_df)

    # Display analytics
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

# Function for displaying menu module
def display_menu_module():
    st.subheader("Ingredient & Product List (Powered by AI)")
    menu_items = ["Burgers", "Pizzas", "Salads", "Wraps", "Pasta"]
    selected_item = st.selectbox("Select a Menu Item to view recommendations and details:", menu_items)

    # Ingredient recommendations
    recommendations = {
        "Burgers": ["Beef, buns, cheese, sauces"],
        "Pizzas": ["Dough, cheese, tomato sauce, toppings"],
        "Salads": ["Lettuce, tomatoes, cucumbers, dressings"],
        "Wraps": ["Tortilla wraps, chicken, lettuce, sauces"],
        "Pasta": ["Pasta, tomato sauce, garlic, olive oil, herbs"]
    }
    st.write(f"**Ingredient Recommendations for {selected_item}:**")
    st.write(recommendations[selected_item])

    # Nutritional information
    nutritional_info = {
        "Burgers": {"Calories": "500 kcal", "Protein": "25g", "Carbs": "40g", "Fat": "20g"},
        "Pizzas": {"Calories": "600 kcal", "Protein": "20g", "Carbs": "70g", "Fat": "25g"},
        "Salads": {"Calories": "150 kcal", "Protein": "5g", "Carbs": "10g", "Fat": "8g"},
        "Wraps": {"Calories": "300 kcal", "Protein": "15g", "Carbs": "35g", "Fat": "12g"},
        "Pasta": {"Calories": "400 kcal", "Protein": "10g", "Carbs": "50g", "Fat": "15g"},
    }
    st.write(f"**Nutritional Information for {selected_item}:**")
    st.write(nutritional_info[selected_item])

    # Recipe suggestion
    recipe_suggestions = {
        "Burgers": "Grill a beef patty and place it between buns with cheese, lettuce, tomato, and sauces.",
        "Pizzas": "Spread tomato sauce on dough, add cheese and toppings, and bake until golden.",
        "Salads": "Chop lettuce, tomatoes, cucumbers, add dressing, and toss.",
        "Wraps": "Add grilled chicken, lettuce, and sauces into a wrap, fold, and serve.",
        "Pasta": "Boil pasta, sauté garlic in olive oil, add tomato sauce, and toss pasta in sauce."
    }
    st.write(f"**AI-Generated Recipe for {selected_item}:**")
    st.write(recipe_suggestions[selected_item])

    # Supplier recommendations
    supplier_recommendations = {
        "Burgers": ["Supplier A for Beef", "Supplier B for Buns", "Supplier C for Cheese"],
        "Pizzas": ["Supplier D for Dough", "Supplier E for Cheese", "Supplier F for Tomato Sauce"],
        "Salads": ["Supplier G for Lettuce", "Supplier H for Tomatoes", "Supplier I for Cucumbers"],
        "Wraps": ["Supplier J for Wraps", "Supplier K for Chicken", "Supplier L for Sauces"],
        "Pasta": ["Supplier M for Pasta", "Supplier N for Tomato Sauce", "Supplier O for Herbs"]
    }
    st.write(f"**Supplier Recommendations for {selected_item}:**")
    for supplier in supplier_recommendations[selected_item]:
        st.write(f"- {supplier}")

    # Cost analysis
    ingredient_costs = {
        "Burgers": {"Beef": "$2.50", "Buns": "$0.50", "Cheese": "$0.75", "Sauces": "$0.25"},
        "Pizzas": {"Dough": "$1.00", "Cheese": "$1.50", "Tomato Sauce": "$0.50", "Toppings": "$0.75"},
        "Salads": {"Lettuce": "$0.50", "Tomatoes": "$0.75", "Cucumbers": "$0.30", "Dressings": "$0.40"},
        "Wraps": {"Tortilla Wraps": "$0.75", "Chicken": "$1.50", "Lettuce": "$0.50", "Sauces": "$0.25"},
        "Pasta": {"Pasta": "$1.00", "Tomato Sauce": "$0.50", "Garlic": "$0.20", "Herbs": "$0.10"}
    }
    st.write(f"**Cost Analysis for {selected_item}:**")
    cost_data = pd.DataFrame(ingredient_costs[selected_item].items(), columns=["Ingredient", "Cost"])
    st.table(cost_data)


# Function for displaying competitors module
def display_competitors_module():
    st.header("Competitor Analytics")
    conn = get_snowflake_connection()

    # Query competitor data
    competitor_data = pd.read_sql("SELECT * FROM KOMBUIS_PROTOTYPE1.PUBLIC.COMPETITOR_TAKEALYTICS", conn)
    conn.close()
    competitor_data.columns = competitor_data.columns.str.lower()

    # Filter by competitor name
    name_selection = st.selectbox("Select Competitor Name", options=competitor_data['name'].unique())
    selected_data = competitor_data[competitor_data['name'] == name_selection]

    # Display competitor details
    if not selected_data.empty:

        # Extract unique postcodes for map display
        postcodes = selected_data['postcode'].unique()
        display_uk_postcode_map_with_multiple_pins(postcodes)

        st.write("### Competitor Details")
        st.write(f"**City:** {selected_data['city'].iloc[0]}")
        st.write(f"**Ratings:** {selected_data['ratings'].iloc[0]}")
        st.write(f"**Hygiene:** {selected_data['hygiene'].iloc[0]}")
        st.write(f"**Social Score:** {selected_data['social'].iloc[0]}")
        st.write("**Food Types (DE):**", selected_data['venue_food_types_de'].iloc[0])
        st.write("**Food Types (JE):**", selected_data['venue_food_types_je'].iloc[0])
        st.dataframe(selected_data)
        
    else:
        st.write("No competitor data found for the selected name.")

# Function for displaying global markets and news module
def display_global_markets_module():
    st.header("Global Markets & Industry News")
    st.write("Stay updated with the latest global market trends, insights, and industry news.")

    # Sources list with concise format
    sources = {
        "Bloomberg UK": "https://www.bloomberg.com/uk",
        "Reuters": "https://www.reuters.com/",
        "Statista": "https://www.statista.com/",
        "The Caterer - Restaurant News": "https://www.thecaterer.com/news/restaurant",
        "Restaurant Online": "https://www.restaurantonline.co.uk/",
        "Code Hospitality": "https://www.codehospitality.co.uk/"
    }
    
    # Display sources in a concise list with links
    st.subheader("Top Sources")
    for name, link in sources.items():
        st.markdown(f"- **{name}**: [Visit]({link})")

    # Ingredient-based news section
    st.subheader("Latest News by Ingredient")
    ingredient = st.text_input("Enter an ingredient to find the latest news:", placeholder="e.g., 'tomato'")

    if ingredient:
        # Using NewsAPI to search for latest news related to the ingredient
        url = f"https://newsapi.org/v2/everything?q={ingredient}&apiKey=83455d79471f4feea24ae1f4ead76902"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors

            news_data = response.json()
            articles = news_data.get("articles", [])

            if articles:
                st.write(f"### Latest News on {ingredient.capitalize()}:")
                for article in articles[:5]:  # Display top 3 articles
                    st.markdown(f"- **{article['title']}**: [{article['source']['name']}]({article['url']})")
            else:
                st.write(f"No recent news articles found for '{ingredient}'.")
        except requests.exceptions.RequestException as e:
            st.write("Error retrieving news data.")
            st.write(e)


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

