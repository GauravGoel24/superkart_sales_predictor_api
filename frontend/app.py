
import streamlit as st
import pandas as pd
import requests

# --------------------------------------------------
# Application Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="SuperKart Sales Predictor",
    page_icon="🛒",
    layout="wide"
)

# Backend API URL
BACKEND_URL = "http://backend:5000"

# Model input features
FEATURE_COLUMNS = [
    "Product_Weight",
    "Product_Sugar_Content",
    "Product_Allocated_Area",
    "Product_Type",
    "Product_MRP",
    "Store_Id",
    "Store_Establishment_Year",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type",
    "Product_Category_Code",
    "Store_Age"
]

# --------------------------------------------------
# Application Header
# --------------------------------------------------

st.title("SuperKart Sales Prediction")

st.subheader("AI-Powered Retail Sales Forecasting")

st.write(
    "Predict product-store sales revenue using a trained "
    "Machine Learning model."
)

st.divider()

# --------------------------------------------------
# Sidebar Navigation
# --------------------------------------------------

st.sidebar.title("Navigation")

prediction_type = st.sidebar.radio(
    "Select Prediction Type",
    ["Single Prediction", "Batch Prediction"]
)

st.sidebar.divider()

st.sidebar.info(
    "SuperKart Sales Predictor uses a trained "
    "Machine Learning regression model."
)

# ==================================================
# SINGLE PREDICTION
# ==================================================

if prediction_type == "Single Prediction":

    st.subheader("Single Sales Prediction")

    st.write(
        "Enter the product and store information "
        "to predict the expected sales revenue."
    )

    with st.form("single_prediction_form"):

        col1, col2 = st.columns(2)

        # Product Information
        with col1:

            st.markdown("#### Product Information")

            product_weight = st.number_input(
                "Product Weight",
                min_value=0.0,
                value=12.5
            )

            product_sugar_content = st.text_input(
                "Product Sugar Content"
            )

            product_allocated_area = st.number_input(
                "Product Allocated Area",
                min_value=0.0,
                value=0.05
            )

            product_type = st.text_input(
                "Product Type"
            )

            product_mrp = st.number_input(
                "Product MRP",
                min_value=0.0,
                value=150.0
            )

            product_category_code = st.text_input(
                "Product Category Code"
            )

        # Store Information
        with col2:

            st.markdown("#### Store Information")

            store_id = st.text_input(
                "Store ID"
            )

            store_establishment_year = st.number_input(
                "Store Establishment Year",
                min_value=1900,
                max_value=2100,
                value=2005
            )

            store_size = st.text_input(
                "Store Size"
            )

            store_location_city_type = st.text_input(
                "Store Location City Type"
            )

            store_type = st.text_input(
                "Store Type"
            )

            store_age = st.number_input(
                "Store Age",
                min_value=0,
                value=21
            )

        submit_button = st.form_submit_button(
            "Predict Sales Revenue",
            use_container_width=True
        )

    # Submit prediction request
    if submit_button:

        input_data = {
            "Product_Weight": product_weight,
            "Product_Sugar_Content": product_sugar_content,
            "Product_Allocated_Area": product_allocated_area,
            "Product_Type": product_type,
            "Product_MRP": product_mrp,
            "Store_Id": store_id,
            "Store_Establishment_Year": store_establishment_year,
            "Store_Size": store_size,
            "Store_Location_City_Type": store_location_city_type,
            "Store_Type": store_type,
            "Product_Category_Code": product_category_code,
            "Store_Age": store_age
        }

        # Validate mandatory text fields
        mandatory_fields = [
            "Product_Sugar_Content",
            "Product_Type",
            "Store_Id",
            "Store_Size",
            "Store_Location_City_Type",
            "Store_Type",
            "Product_Category_Code"
        ]

        missing_fields = [
            field for field in mandatory_fields
            if not str(input_data[field]).strip()
        ]

        if missing_fields:

            st.warning(
                "Please enter the following fields: "
                + ", ".join(missing_fields)
            )

        else:

            try:

                with st.spinner("Generating sales prediction..."):

                    response = requests.post(
                        f"{BACKEND_URL}/v1/predict",
                        json=input_data,
                        timeout=60
                    )

                if response.status_code == 200:

                    result = response.json()

                    st.success(
                        "Prediction generated successfully!"
                    )

                    st.metric(
                        label="Predicted Sales Revenue",
                        value=f"{float(result['Predicted Sales Revenue']):,.2f}"
                    )

                else:

                    st.error(
                        f"Backend API Error: {response.text}"
                    )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"Unable to connect to the backend: {e}"
                )

# ==================================================
# BATCH PREDICTION
# ==================================================

else:

    st.subheader("Batch Sales Prediction")

    st.write(
        "Upload a CSV file containing multiple product-store "
        "records to generate predictions in a single request."
    )

    st.info(
        "The CSV file must contain all 12 input features "
        "with the exact column names used during model training."
    )

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            input_df = pd.read_csv(uploaded_file)

            st.markdown("#### Uploaded Data Preview")

            st.dataframe(
                input_df.head(10),
                use_container_width=True
            )

            st.write(
                f"Total records uploaded: **{len(input_df)}**"
            )

            missing_columns = [
                col for col in FEATURE_COLUMNS
                if col not in input_df.columns
            ]

            if missing_columns:

                st.error(
                    "Missing columns in uploaded CSV: "
                    + ", ".join(missing_columns)
                )

            elif input_df.empty:

                st.warning(
                    "The uploaded CSV file contains no records."
                )

            else:

                if st.button(
                    "Generate Batch Predictions",
                    use_container_width=True
                ):

                    try:

                        with st.spinner(
                            "Generating predictions for uploaded records..."
                        ):

                            uploaded_file.seek(0)

                            files = {
                                "file": (
                                    uploaded_file.name,
                                    uploaded_file.getvalue(),
                                    "text/csv"
                                )
                            }

                            response = requests.post(
                                f"{BACKEND_URL}/v1/predictbatch",
                                files=files,
                                timeout=300
                            )

                        if response.status_code == 200:

                            predictions = response.json()

                            result_df = pd.DataFrame(
                                list(predictions.items()),
                                columns=[
                                    "Record Number",
                                    "Predicted Sales Revenue"
                                ]
                            )

                            st.success(
                                "Batch predictions generated successfully!"
                            )

                            col1, col2 = st.columns(2)

                            with col1:
                                st.metric(
                                    "Total Records Processed",
                                    len(result_df)
                                )

                            with col2:
                                st.metric(
                                    "Average Predicted Sales",
                                    f"{result_df['Predicted Sales Revenue'].mean():,.2f}"
                                )

                            st.markdown("#### Prediction Results")

                            st.dataframe(
                                result_df,
                                use_container_width=True
                            )

                            # Download prediction results
                            csv_data = result_df.to_csv(
                                index=False
                            ).encode("utf-8")

                            st.download_button(
                                label="Download Predictions CSV",
                                data=csv_data,
                                file_name="superkart_sales_predictions.csv",
                                mime="text/csv",
                                use_container_width=True
                            )

                        else:

                            st.error(
                                f"Backend API Error: {response.text}"
                            )

                    except requests.exceptions.RequestException as e:

                        st.error(
                            f"Unable to connect to the backend: {e}"
                        )

        except Exception as e:

            st.error(
                f"Unable to read the uploaded CSV file: {e}"
            )

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "SuperKart Sales Prediction | Machine Learning Model Deployment"
)
