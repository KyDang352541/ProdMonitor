import streamlit as st
import pandas as pd

# Đọc dữ liệu (giả sử bạn upload file Excel)
uploaded_file = st.file_uploader("Upload báo cáo Excel", type=["xlsx"])
if uploaded_file:
    df_tasks = pd.read_excel(uploaded_file, sheet_name='Tasks')
    df_summary = pd.read_excel(uploaded_file, sheet_name='Summary', index_col=0)

    st.title("📋 V-tail Production Report")

    # Tổng hợp thông tin
    st.subheader("🔍 Tổng quan")
    st.write("**Tổng giá bán:**", f"${df_summary.loc['Total selling price', 'Value']}")
    st.write("**Giờ lao động:**", df_summary.loc['Labour hours', 'Value'])
    st.write("**Đơn giá lao động:**", f"${df_summary.loc['Labour price', 'Value']}")
    st.write("**Đã chi:**", f"${df_summary.loc['Spent', 'Value']}")

    # Tính toán chênh lệch
    total_cost = df_summary.loc['Labour hours', 'Value'] * df_summary.loc['Labour price', 'Value']
    total_spent = total_cost + df_summary.loc['Spent', 'Value']
    profit = df_summary.loc['Total selling price', 'Value'] - total_spent
    st.metric("💰 Lợi nhuận", f"${profit:,.2f}")

    # Hiển thị công việc theo nhóm
    st.subheader("🛠️ Tiến độ công việc")
    for task_type in df_tasks["Type"].unique():
        st.markdown(f"### 🔹 {task_type}")
        df_filtered = df_tasks[df_tasks["Type"] == task_type]
        st.dataframe(df_filtered[['No', 'Job', 'Status']], use_container_width=True)

    # Cho phép chỉnh trạng thái
    st.subheader("✏️ Cập nhật trạng thái công việc")
    selected_row = st.selectbox("Chọn công việc:", df_tasks['Job'])
    new_status = st.selectbox("Cập nhật trạng thái:", ["Done", "Inprocess", "No"])
    if st.button("Cập nhật"):
        df_tasks.loc[df_tasks['Job'] == selected_row, 'Status'] = new_status
        st.success("Đã cập nhật trạng thái!")

    # (Tuỳ chọn) Cho phép tải xuống báo cáo
    # (Bạn có thể dùng pandas + openpyxl hoặc reportlab/pdfkit cho bước này)
