import streamlit as st
import zipfile
import io
from app import get_data


def runtime():
    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
    
    st.title('CRT Planner')
    df1, df2, excel_file = get_data()
    csv_overview = convert_df(df1)
    csv_month_planner = convert_df(df2)

    zip_data = io.BytesIO()
    with zipfile.ZipFile(zip_data, 'w') as zf:
        zf.writestr('crt_planner_overview.csv', csv_overview)
        zf.writestr('crt_planner_month.csv', csv_month_planner)

    zip_data.seek(0)

    with st.container():
        st.download_button(
        label="Download data as CSV",
        data=zip_data,
        file_name='crt_planner.zip',
        mime='application/zip',
    )
        
    with open(excel_file, "rb") as file:
        st.download_button(
                    label="Download Excel file",
                    data=file,
                    file_name=excel_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    

runtime()