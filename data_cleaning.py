import pandas as pd


class DataCleaning:
    def __init__(self):
        pass

    def clean_data_general(self, data_frame):
        data_frame = data_frame.drop_duplicates()
        data_frame.columns = [col.lower() for col in data_frame.columns]
        # Drop rows with any null values
        data_frame = data_frame.dropna()
        # data_frame = data_frame.fillna("Unknown")
        return data_frame

    def clean_user_data(self, data_frame):
        # Clean general data first
        data_frame = self.clean_data_general(data_frame)
        data_frame["date_of_birth"] = pd.to_datetime(
            data_frame["date_of_birth"], errors="coerce", format="%Y-%m-%d"
        )
        data_frame = data_frame.dropna(subset=["date_of_birth"])
        data_frame["date_of_birth"] = data_frame["date_of_birth"].dt.date

        # data_frame = self.handle_null_values(data_frame)

        return data_frame

    def clean_card_data(self, data_frame):
        """
        Cleans card data.
        :param data_frame: The pandas DataFrame containing card data.
        :return: A cleaned pandas DataFrame.
        """
        data_frame = self.clean_data_general(data_frame)

        # Remove rows where expiry_date is not in the format 'MM/YY'
        valid_expiry_date_format = r'^\d{2}/\d{2}$'
        data_frame = data_frame[data_frame['expiry_date'].str.match(valid_expiry_date_format, na=False)]

        return data_frame
    
    def clean_store_data(self, df):
        # Remove duplicates
        df = df.drop_duplicates()

        # Filter rows where country_code length is less than or equal to 2
        df = df[df["country_code"].str.len() <= 2]

        # Filter rows where continent is either Europe or America
        df = df[df["continent"].isin(["Europe", "America"])]

        return df



    def convert_product_weights(self, products_df):
        def convert_weight(weight):
            if pd.isna(weight):
                return None

            # Removes all characters except numbers, decimal points, and known units
            cleaned_weight = "".join(
                char for char in weight if char.isdigit() or char in ".gmlkKGML"
            )

            # Splits numeric part and unit
            numeric_part = "".join(
                char for char in cleaned_weight if char.isdigit() or char == "."
            )
            unit_part = "".join(char for char in cleaned_weight if char.isalpha())

            try:
                numeric_weight = float(numeric_part)
                if unit_part.lower() in ["g", "ml"]:
                    return f"{numeric_weight / 1000} kg"  # Convers grams or ml to kg and append 'kg'
                elif unit_part.lower() == "kg":
                    return f"{numeric_weight} kg"  # Append 'kg'
                else:
                    return None  # Unknown unit
            except ValueError:
                return None  # Conversion to float failed

        products_df["weight"] = products_df["weight"].apply(convert_weight)
        return products_df

    def clean_products_data(self, products_df):
        cleaned_df = products_df.dropna()
        return cleaned_df

    def clean_orders_data(self, data_frame):
        """
        Cleans the orders data.
        :param data_frame: DataFrame containing orders data.
        :return: Cleaned DataFrame.
        """
        # Removes specified columns
        columns_to_remove = ["first_name", "last_name", "1"]
        for col in columns_to_remove:
            if col in data_frame.columns:
                data_frame = data_frame.drop(columns=col)

        return data_frame