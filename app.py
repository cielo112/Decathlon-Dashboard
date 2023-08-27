import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load data
path = r'sample_df.zip'
df_clean = pd.read_csv(path, compression='zip')

# Configure the dashboard to be desktop friendly
st.set_page_config(layout="wide")


# Title and introduction
st.title("Decathlon Sales Dashboard")
st.write("Explore sales data with interactive plots")


# Create two columns for filter header
col1, col2 = st.columns(2)

with col1:
    # Header for Filters
    st.header("Filter Data")

# Create two columns for filters
col1, col2 = st.columns(2)

with col1:

    selected_business_unit = st.selectbox("Select Store Branch", df_clean['but_name_business_unit'].unique(), key='1')
    apply_filter = st.checkbox('Apply Filter to Selected Plots', key='2')

    filtered_df = df_clean[df_clean['but_name_business_unit'] == selected_business_unit]

    # Create Filter for the Month
    selected_month = st.selectbox('Select Month', df_clean['month_name'].unique(), key='10')
    apply_filter_month = st.checkbox('Apply Filter to All Plots', key='11')

    filt_month_df = df_clean[df_clean['month_name'] == selected_month]

# Create two columns for graphs
col1, col2 = st.columns(2)
with col1:
    # Top 5 Models based on Sales
    st.header("Top 5 Models based on Sales")

    # Create a filter to get only the data from physical stores
    physical_store_filter = df_clean['but_name_business_unit'] != 'Decathlon.ph'
    df_ps = df_clean[physical_store_filter]

    # Create a special filter for the physical stores for the month and business unit filter
    filtered_df = df_ps[df_ps['but_name_business_unit'] == selected_business_unit]
    filt_month_df_ps = df_ps[df_ps['month_name'] == selected_month]

    # If block for the branch filter
    if apply_filter:
        filtered_df['Sales'] = filtered_df['f_qty_item'] * filtered_df['f_to_tax_in']
        sales_grouped_by_model = filtered_df.groupby('mdl_num_model_r3')['Sales'].sum()
        top_5_models_in_sales = sales_grouped_by_model.sort_values(ascending=False)[:5]    
    else:
        df_ps['Sales'] = df_ps['f_qty_item'] * df_ps['f_to_tax_in']
        sales_grouped_by_model = df_ps.groupby('mdl_num_model_r3')['Sales'].sum()
        top_5_models_in_sales = sales_grouped_by_model.sort_values(ascending=False)[:5]
    
    # If block for the month filter
    if apply_filter_month:
        filt_month_df['Sales'] = filt_month_df['f_qty_item'] * filt_month_df['f_to_tax_in']
        sales_grouped_by_model = filt_month_df.groupby('mdl_num_model_r3')['Sales'].sum()
        top_5_models_in_sales = sales_grouped_by_model.sort_values(ascending=False)[:5]    
    else:
        df_ps['Sales'] = df_ps['f_qty_item'] * df_ps['f_to_tax_in']
        sales_grouped_by_model = df_ps.groupby('mdl_num_model_r3')['Sales'].sum()
        top_5_models_in_sales = sales_grouped_by_model.sort_values(ascending=False)[:5]
    
    # If block for the month and branch filter in case both are selected
    if apply_filter_month and apply_filter:
        # Apply the business filter first
        filtered_df = df_ps[df_ps['but_name_business_unit'] == selected_business_unit]
        filtered_df['Sales'] = filtered_df['f_qty_item'] * filtered_df['f_to_tax_in']

        # And then apply the month filter
        filt_month_df_ps = filtered_df[filtered_df['month_name'] == selected_month]
        filt_month_df_ps['Sales'] = filt_month_df_ps['f_qty_item'] * filt_month_df_ps['f_to_tax_in']

        sales_grouped_by_model = filt_month_df_ps.groupby('mdl_num_model_r3')['Sales'].sum()
        top_5_models_in_sales = sales_grouped_by_model.sort_values(ascending=False)[:5]
    else:
        df_ps['Sales'] = df_ps['f_qty_item'] * df_ps['f_to_tax_in']
        sales_grouped_by_model = df_ps.groupby('mdl_num_model_r3')['Sales'].sum()
        top_5_models_in_sales = sales_grouped_by_model.sort_values(ascending=False)[:5]


    fig, ax = plt.subplots(figsize=(10, 5))

    # Calculate total sales for percentage contribution calculation
    total_sales = df_clean['f_to_tax_in'].sum()

    # Check if the filtered DataFrame is not empty before performing calculations
    if not top_5_models_in_sales.empty:
        sns.barplot(x=top_5_models_in_sales.index, y=top_5_models_in_sales.values,
                    order=top_5_models_in_sales.sort_values(ascending=False).index, ax=ax)
        ax.set_ylabel('Sales (Php)')

        ax2 = ax.twinx()
        sns.barplot(x=top_5_models_in_sales.index, y=top_5_models_in_sales.values * 100 / total_sales,
                    order=top_5_models_in_sales.sort_values(ascending=False).index, ax=ax2)
        ax2.set_ylabel('Percentage in Total Sales (%)')
    else:
        # If the filtered DataFrame is empty, provide an informative message
        ax.text(0.5, 0.5, "No data available", horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=14, color='gray')

    ax.set_xlabel('Model Number')
    plt.title('Top 5 Models in Sales (Jun-Dec 2019)')
    plt.show()
    plt.tight_layout()
    st.pyplot(plt)

with col2:
    # Number of Transactions at Different Times of Day
    st.header('Number of Transactions at Different Times of Day')

    if apply_filter:
        num_trans_per_time = filtered_df.groupby('Time of Day')['the_transaction_id'].nunique()
    else:
        num_trans_per_time = df_clean.groupby('Time of Day')['the_transaction_id'].nunique()

    desired_order = ['5 AM-6 AM', '6 AM-7 AM', '7 AM-8 AM', '8 AM-9 AM', '9 AM-10 AM',
                    '10 AM-11 AM', '11 AM-12 PM', '12 PM-1 PM', '1 PM-2 PM', '2 PM-3 PM',
                    '3 PM-4 PM', '4 PM-5 PM', '5 PM-6 PM', '6 PM-7 PM', '7 PM-8 PM',
                    '8 PM-9 PM', '9 PM-10 PM', '10 PM-11 PM', '11 PM-12 AM']

    fig, ax  = plt.subplots(figsize=(10,5))
    sns.barplot(
        x = num_trans_per_time.index,
        y = num_trans_per_time.values,
        order = desired_order
    )
    plt.title('Number of Transactions at Different Times of Day')
    plt.xlabel('Time of Day')
    plt.ylabel('Number of Transactions')
    plt.xticks(rotation=45)
    plt.show()
    plt.tight_layout()
    st.pyplot(plt)

st.markdown('<hr style="border: 1px solid #ccc;">', unsafe_allow_html=True)



# Make a separate section for the Per Branch Data
st.title("Data per Store Branch")

# Create two columns for filter header
col1, col2 = st.columns(2)

with col1:
    # Header for Filters
    st.header("Filter Data")

# Create two columns for the filter
col1, col2 = st.columns(2)
with col1:
    # Create Filter for the Month
    selected_month = st.selectbox('Select Month', df_clean['month_name'].unique(), key='12')
    apply_filter_month_branch = st.checkbox('Apply Filter to All Plots', key='13')

    filt_month_df = df_clean[df_clean['month_name'] == selected_month]

# Create two columns for graphs
col1, col2 = st.columns(2)
with col1:
    # Number of Transactions
    st.header("Number of Transactions")


    if apply_filter_month_branch:
        # Make a filter to show transactions made only by members
        member_filter = filt_month_df['ctm_customer_id'] != 'Non Members'
        members_only_df = filt_month_df[member_filter]
        num_trans_grouped_by_branch = members_only_df.groupby('but_name_business_unit')['the_transaction_id'].nunique()

    else:
        # Make a filter to show transactions made only by members
        member_filter = df_clean['ctm_customer_id'] != 'Non Members'
        members_only_df = df_clean[member_filter]
        num_trans_grouped_by_branch = members_only_df.groupby('but_name_business_unit')['the_transaction_id'].nunique()

    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(
        x = num_trans_grouped_by_branch.index,
        y = num_trans_grouped_by_branch.values,
        order = num_trans_grouped_by_branch.sort_values(ascending=False).index,
    )
    plt.title('Number of Transactions')
    plt.xlabel('Store Branch')
    plt.ylabel('Number of Transactions')
    plt.show()
    st.pyplot(plt)

with col2:
    # Average Basket Value per Business Unit
    st.header("Average Basket Value")

    if apply_filter_month_branch:
        basket_value_per_store = filt_month_df.groupby(['but_name_business_unit', 'the_transaction_id'])['Sales'].sum()
        ave_basket_value_per_store = basket_value_per_store.groupby('but_name_business_unit').mean()

    else:
        basket_value_per_store = df_clean.groupby(['but_name_business_unit', 'the_transaction_id'])['Sales'].sum()
        ave_basket_value_per_store = basket_value_per_store.groupby('but_name_business_unit').mean()

    fig, ax = plt.subplots(figsize=(10,4.88))
    sns.barplot(
        x = ave_basket_value_per_store.index,
        y = ave_basket_value_per_store.values,
        order = ave_basket_value_per_store.sort_values(ascending=False).index,
    )
    plt.title('Average Basket Value')
    plt.xlabel('Store Branch')
    plt.ylabel('Basket Value (Php)')
    plt.show()
    st.pyplot(plt)

# Create two columns for graphs
col1, col2 = st.columns(2)
with col1:
    # Average Basket Size per Business Unit
    st.header("Average Basket Size")


    if apply_filter_month_branch:
        basket_size_per_store = filt_month_df.groupby(['but_name_business_unit', 'the_transaction_id'])['f_qty_item'].sum()
        ave_basket_size_per_store = basket_size_per_store.groupby('but_name_business_unit').mean()

    else:
        basket_size_per_store = df_clean.groupby(['but_name_business_unit', 'the_transaction_id'])['f_qty_item'].sum()
        ave_basket_size_per_store = basket_size_per_store.groupby('but_name_business_unit').mean()

    fig, ax = plt.subplots(figsize=(10,4.9))
    sns.barplot(
        x = ave_basket_size_per_store.index,
        y = ave_basket_size_per_store.values,
        order = ave_basket_size_per_store.sort_values(ascending=False).index
    )
    plt.title('Average Basket Size')
    plt.xlabel('Store Branch')
    plt.ylabel('Basket Size')
    plt.show()
    st.pyplot(plt)

with col2:
    # Total Sales per Branch
    st.header("Total Sales")


    if apply_filter_month_branch:
        total_sales_per_store = filt_month_df.groupby('but_name_business_unit')['Sales'].sum()
    else:
        total_sales_per_store = df_clean.groupby('but_name_business_unit')['Sales'].sum()

    fig, axs = plt.subplots(figsize=(10,5))
    sns.barplot(
        x = total_sales_per_store.index,
        y = total_sales_per_store.values,
        order = total_sales_per_store.sort_values(ascending=False).index
    )
    plt.title('Total Sales (Jun-Dec 2019)')
    plt.xlabel('Store Branch')
    plt.ylabel('Total Sales (Php)')
    plt.show()
    st.pyplot(plt)

